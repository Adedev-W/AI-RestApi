from .model_fs import model, processor, device
import io
from torch.nn.functional import softmax
from PIL import Image
import torch

def predict(image_data):
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    # Preprocessing dan prediksi
    inputs = processor(images=image, return_tensors="pt").to(device)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        label = model.config.id2label[idx]
        probs = softmax(logits, dim=1)
        confidence = probs[0][idx].item()
    return {"label": label, "confidence": confidence}


# Kode asli:
# def predict(image_data):
#     image = Image.open(io.BytesIO(image_data)).convert("RGB")
#     # Preprocessing dan prediksi
#     inputs = processor(images=image, return_tensors="pt").to(device)
#     inputs = {k: v.to(device) for k, v in inputs.items()}
#     with torch.no_grad():
#         outputs = model(**inputs)
#         logits = outputs.logits
#         idx = logits.argmax(-1).item()
#         label = model.config.id2label[idx]
#         probs = torch.nn.functional.softmax(logits, dim=1)
#         confidence = probs[0][idx].item()
#     return {"label": label, "confidence": confidence}
