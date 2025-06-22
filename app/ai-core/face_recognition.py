import insightface
import numpy as np
import cv2
import os

# Pastikan model diunduh sekali saja (saat startup)
# Model akan disimpan di ~/.insightface/models/
if not os.path.exists(os.path.expanduser("~/.insightface")):
    os.makedirs(os.path.expanduser("~/.insightface"))

# Inisialisasi model
# Anda bisa menggunakan 'cpu' atau 'cuda:0' jika punya GPU
fa = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])
fa.prepare(ctx_id=0, det_size=(640, 640))

def get_face_embedding(image_data):
    """Menerima data gambar (bytes) dan mengembalikan embedding wajah."""
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    faces = fa.get(img)
    if not faces:
        return None
    # Ambil embedding dari wajah pertama yang terdeteksi
    return faces[0].embedding

def compare_faces(embedding1, embedding2):
    """Membandingkan dua embedding wajah dan mengembalikan hasilnya."""
    if embedding1 is None or embedding2 is None:
        return {"match": False, "similarity": 0.0, "error": "Could not detect face in one or both images."}

    # Menghitung cosine similarity
    similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    
    # Threshold untuk menentukan apakah wajah cocok (bisa disesuaikan)
    match_threshold = 0.5 
    
    return {
        "match": bool(similarity > match_threshold),
        "similarity": float(similarity)
    } 