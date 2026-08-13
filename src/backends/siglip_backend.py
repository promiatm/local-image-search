import torch
from transformers import AutoModel, AutoProcessor

MODEL_NAME = "google/siglip-base-patch16-224"

class SiglipBackend:
    def __init__(self):
        self.device = ("cuda" if torch.cuda.is_available() else "cpu")

        self.processor = AutoProcessor.from_pretrained(MODEL_NAME)

        self.model = AutoModel.from_pretrained(MODEL_NAME).to(self.device)

        self.model.eval()

if __name__ == "__main__":
    backend = SiglipBackend()

    print(f"Loaded {MODEL_NAME}")
    print(f"Device: {backend.device}")