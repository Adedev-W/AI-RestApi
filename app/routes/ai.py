from fastapi import APIRouter, Depends, UploadFile, File, Request, HTTPException, Form
from pydantic import BaseModel
from app.core.jwt_utils import get_current_user
from app.models.user import User
from app.ai_core.face_spoofing_d import predict as predict_spoof
from app.ai_core.face_recognition import get_face_embedding, compare_faces
from app.core.vector_db import milvus_service
from app.core.limiter import limiter
from typing import Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", 5)) * 1024 * 1024 # 5 MB
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/jpg"]

router = APIRouter(prefix="/ai", tags=["AI"])

class PredictionResponse(BaseModel):
    label: str
    confidence: float

class FaceComparisonResponse(BaseModel):
    match: bool
    similarity: float
    error: str = None

class FaceVerificationResponse(BaseModel):
    spoof_check_passed: bool
    spoof_label: str
    spoof_confidence: float
    face_match_passed: bool = None
    face_similarity: float = None
    embedding_saved: bool = False
    error: str = None

@router.post("/predict_face_spoofing", response_model=PredictionResponse)
@limiter.limit(os.getenv("RATE_LIMIT", "5/minute"))
async def predict_face_spoofing(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint aman untuk prediksi Face Spoofing.
    Menerima file gambar dan mengembalikan label (real/spoof) beserta confidence.
    """
    # 1. Validasi Tipe File
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed types are: {', '.join(ALLOWED_MIME_TYPES)}")

    # 2. Validasi Ukuran File
    size = await file.seek(0, 2)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large. Maximum size is {MAX_FILE_SIZE / 1024 / 1024} MB.")
    await file.seek(0)
    
    image_data = await file.read()
    prediction_result = predict_spoof(image_data)
    return prediction_result

@router.post("/compare_faces", response_model=FaceComparisonResponse)
@limiter.limit(os.getenv("RATE_LIMIT", "5/minute"))
async def compare_faces_endpoint(
    request: Request,
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint aman untuk membandingkan dua wajah dari dua gambar.
    """
    for file in [file1, file2]:
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}")
        size = await file.seek(0, 2)
        if size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File too large: {file.filename}")
        await file.seek(0)

    image_data1 = await file1.read()
    image_data2 = await file2.read()

    embedding1 = get_face_embedding(image_data1)
    embedding2 = get_face_embedding(image_data2)

    result = compare_faces(embedding1, embedding2)
    return result 

@router.post("/verify_identity", response_model=FaceVerificationResponse)
@limiter.limit(os.getenv("RATE_LIMIT", "5/minute"))
async def verify_identity(
    request: Request,
    val_image: UploadFile = File(...),
    main_image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    saved: bool = Form(False),
    name: Optional[str] = Form(None)
):
    """
    Verifikasi identitas: bandingkan dengan galeri Milvus jika 'name' ada,
    jika tidak, bandingkan dengan 'main_image'.
    """
    # Validasi val_image
    if val_image.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid file type: {val_image.filename}")
    size = await val_image.seek(0, 2)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large: {val_image.filename}")
    await val_image.seek(0)

    val_image_data = await val_image.read()

    # Langkah 1: Cek Spoofing pada val_image
    spoof_result = predict_spoof(val_image_data)
    if spoof_result["label"] != "real":
        return {
            "spoof_check_passed": False,
            "spoof_label": spoof_result["label"],
            "spoof_confidence": spoof_result["confidence"],
            "error": "Verification failed: Validation image is a spoof."
        }

    # Langkah 2: Ekstrak embedding dari val_image
    val_embedding = get_face_embedding(val_image_data)
    if val_embedding is None:
        return {"spoof_check_passed": True, "spoof_label": spoof_result["label"], "spoof_confidence": spoof_result["confidence"], "error": "Could not detect face in validation image."}

    # Langkah 3: Tentukan strategi perbandingan
    comparison_result = {}
    if name and milvus_service.has_embeddings(name):
        comparison_result = milvus_service.search_and_compare(name, val_embedding)
    else:
        if main_image is None:
            raise HTTPException(status_code=400, detail="main_image is required for initial verification.")
        # ... (validasi main_image) ...
        main_image_data = await main_image.read()
        main_embedding = get_face_embedding(main_image_data)
        comparison_result = compare_faces(main_embedding, val_embedding)

    # Langkah 4: Simpan embedding jika cocok
    embedding_was_saved = False
    if comparison_result.get("match") and saved and name:
        try:
            milvus_service.insert_embedding(name, val_embedding)
            embedding_was_saved = True
        except Exception as e:
            print(f"Failed to save embedding to Milvus: {e}")
    
    return {
        "spoof_check_passed": True,
        "spoof_label": spoof_result["label"],
        "spoof_confidence": spoof_result["confidence"],
        "face_match_passed": comparison_result.get("match"),
        "face_similarity": comparison_result.get("similarity"),
        "embedding_saved": embedding_was_saved,
        "error": comparison_result.get("error")
    }
