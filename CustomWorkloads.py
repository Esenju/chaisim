class ImageSensor:
    def __init__(self, width, height, roi_ratio):
        self.width = width
        self.height = height
        self.roi_ratio = roi_ratio  # % of pixels retained
        
    def generate_frame(self):
        # Synthetic ROI data (e.g., center crop)
        roi_w = int(self.width * self.roi_ratio)
        roi_h = int(self.height * self.roi_ratio)
        return np.random.rand(roi_h, roi_w, 3)

class SobelDSP:
    def __init__(self, precision=8):
        self.precision = precision
        
    def process(self, frame):
        # Simulate edge detection + quantization
        edges = np.sqrt(np.square(np.gradient(frame)[0]) + np.square(np.gradient(frame)[1]))
        return edges.astype(f"uint{self.precision}")

class SparsityNPU:
    def __init__(self, model, sparsity):
        self.sparsity = sparsity  % of zeros
        
    def infer(self, x):
        # Simulate sparsity
        mask = np.random.rand(*x.shape) > self.sparsity
        return x * mask