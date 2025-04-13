ChAI-Sim is an open-source simulation framework that enables researchers and Engineers to explore the interplay between chiplet interconnect configurations and AI workloads in edge computing systems.

Key Features
Modular Chiplet Modeling
Pre-configured chiplets (sensor, DSP, NPU, memory) with customizable clock speeds, cache hierarchies, and data filtering (ROI, sparsity, quantization).
Support for user-defined chiplets (e.g., Custom accelerators). 

Interconnect Configurator 
Topologies: Mesh, ring, crossbar, hierarchical
Protocols: packet-switched, circuit-switched, adaptive routing
Parameters: link bandwidth, latency, buffer sizes, error rates

AI Workload Library 
Pre-integrated models(ResNet, Yolo, Bert-Tiny) and datasets (COCO, ImageNet).
Custom workload support via PyTorch/TensorFlow Lite integration

Cross-layer Metrics
End-to-end latency, energy-per-inference, interconnect utilization, and accuracy drop.
Thermal/power profiling (via McPAT/DSENT integration).

Test Run flow:
# Terminal 1: Start Booksim
cd booksim/
./booksim ../configs/mesh4x4.cfg

# Terminal 2: Run Gem5 with bridge
gem5.opt configs/chiplet_system.py

