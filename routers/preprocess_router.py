from fastapi import APIRouter, UploadFile, File, Form
import pandas as pd
import os
from services.preprocessing_service import handle_missing_values, encode_categorical, remove_outliers

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(file_path)
    return {"message": "File uploaded successfully", "columns": list(df.columns), "path": file_path}

@router.post("/apply")
async def apply_preprocessing(
    file_path: str = Form(...),
    technique: str = Form(...)
):
    df = pd.read_csv(file_path)

    if technique == "missing_values":
        df = handle_missing_values(df)
    elif technique == "encode":
        df = encode_categorical(df)
    elif technique == "outliers":
        df = remove_outliers(df)

    df.to_csv(file_path, index=False)
    return {"message": f"{technique} applied successfully!", "path": file_path}
