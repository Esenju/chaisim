import m5
from m5.objects import *
from m5.util import addToPath
from CustomWorkloads import ImageSensor, SobelDSP, SparsityNPU

# Add Booksim bridge integration
addToPath("../src/")
from gem5_booksim_bridge import BookSimBridge

# Define chiplets as separate systems
class SensorChiplet(System):
    def __init__(self):
        super().__init__()
        self.clk_domain = SrcClockDomain(clock="2GHz")
        self.mem_mode = "timing"
        self.workload = ImageSensor(width=1920, height=1080, roi_ratio=0.4)
        
        # Local cache
        self.cache = SimpleCache(size="128kB")
        self.cpu = TimingSimpleCPU()
        self.cpu.icache_port = self.cache.cpu_side
        self.cpu.dcache_port = self.cache.cpu_side
        self.membus = SystemXBar()
        self.cache.mem_side = self.membus.cpu_side_ports

class DSPChiplet(System):
    def __init__(self):
        super().__init__()
        self.clk_domain = SrcClockDomain(clock="1.5GHz")
        self.workload = SobelDSP(precision=8)
        self.cpu = MinorCPU()  # For pipelined execution
        self.membus = SystemXBar()
        self.cpu.icache_port = self.membus.cpu_side_ports
        self.cpu.dcache_port = self.membus.cpu_side_ports

class NPUChiplet(System):
    def __init__(self):
        super().__init__()
        self.clk_domain = SrcClockDomain(clock="2.5GHz")
        self.workload = SparsityNPU(model="resnet18", sparsity=0.7)
        self.accel = Accelerator()  # Custom NPU model
        self.membus = SystemXBar()
        self.accel.port = self.membus.cpu_side_ports

class MemoryChiplet(System):
    def __init__(self):
        super().__init__()
        self.mem_ctrl = RubyMemoryControl()
        self.mem_ranges = [AddrRange("4GB")]

# Build full system
def build():
    system = System()
    
    # Instantiate chiplets
    system.sensor = SensorChiplet()
    system.dsp = DSPChiplet()
    system.npu = NPUChiplet()
    system.mem = MemoryChiplet()
    
    # Connect chiplets to Booksim bridge
    system.booksim = BookSimBridge(topology="mesh4x4")
    
    # Map chiplets to Booksim nodes
    system.booksim.add_node(0, system.sensor.membus.mem_side_ports)
    system.booksim.add_node(1, system.dsp.membus.mem_side_ports)
    system.booksim.add_node(2, system.npu.membus.mem_side_ports)
    system.booksim.add_node(3, system.mem.mem_ctrl.port)
    
    return system

# Instantiate and run
if __name__ == "__m5_main__":
    system = build()
    root = Root(full_system=False, system=system)
    m5.instantiate()
    print("Starting simulation...")
    exit_event = m5.simulate()
    print(f"Simulation exited: {exit_event.getCause()}")