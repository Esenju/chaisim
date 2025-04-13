import socket
import subprocess
from threading import Thread

class BookSimBridge:
    def __init__(self, topology="mesh4x4"):
        self.booksim_proc = subprocess.Popen(
            ["./booksim", f"../configs/{topology}.cfg"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        self.nodes = {}
        
        # Socket server for Gem5 communication
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", 5000))
        self.server.listen(4)  # One per chiplet
        
    def add_node(self, node_id, port):
        self.nodes[node_id] = port
        Thread(target=self._handle_node, args=(node_id,)).start()
        
    def _handle_node(self, node_id):
        conn, _ = self.server.accept()
        while True:
            data = conn.recv(1024)  # Receive Gem5 packet
            self.booksim_proc.stdin.write(f"inject {node_id} {data}\n")
            self.booksim_proc.stdin.flush()
            
            # Wait for Booksim ejection
            while True:
                line = self.booksim_proc.stdout.readline()
                if f"eject {node_id}" in line:
                    conn.send(line.split()[-1])  # Forward to Gem5
                    break