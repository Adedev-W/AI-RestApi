from fastapi import APIRouter, UploadFile, File, Request, HTTPException, Form
from app.ai_core.face_spoofing_d import predict as predict_spoof
from app.ai_core.face_recognition import get_face_embedding, compare_faces
from app.core.limiter import limiter
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", 5)) * 1024 * 1024
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/jpg"]
DEMO_RATE_LIMIT = os.getenv("DEMO_RATE_LIMIT", "20/minute")

router = APIRouter(prefix="/demo", tags=["Demo"])

@router.post("/predict_face_spoofing")
@limiter.limit(DEMO_RATE_LIMIT)
async def demo_predict_face_spoofing(request: Request, file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    size = await file.seek(0, 2)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large.")
    await file.seek(0)
    image_data = await file.read()
    return predict_spoof(image_data)

@router.post("/verify_identity")
@limiter.limit(DEMO_RATE_LIMIT)
async def demo_verify_identity(
    request: Request,
    val_image: UploadFile = File(...),
    main_image: Optional[UploadFile] = File(None)
):
    # Validasi kedua file
    for file in [val_image, main_image]:
        if file and file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}")
    
    val_image_data = await val_image.read()

    spoof_result = predict_spoof(val_image_data)
    if spoof_result["label"] != "real":
        return {"error": "Verification failed: Validation image is a spoof.", **spoof_result}

    if not main_image:
        raise HTTPException(status_code=400, detail="main_image is required for verification.")
        
    main_image_data = await main_image.read()
    
    embedding1 = get_face_embedding(main_image_data)
    embedding2 = get_face_embedding(val_image_data)
    
    comparison_result = compare_faces(embedding1, embedding2)
    return {**spoof_result, **comparison_result} 