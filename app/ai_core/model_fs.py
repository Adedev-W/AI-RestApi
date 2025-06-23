# Load model directly
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch

processor = AutoImageProcessor.from_pretrained(
    "nguyenkhoa/dinov2_Liveness_detection_v2.2.3", use_fast=True
)
model = AutoModelForImageClassification.from_pretrained(
    "nguyenkhoa/dinov2_Liveness_detection_v2.2.3"
)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
model.to(device)
model.eval()
