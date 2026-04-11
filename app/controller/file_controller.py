from fastapi import APIRouter, UploadFile, File, Form
from ..service.FileService import FileService

router = APIRouter(prefix="/files", tags=["File APIS"])

file_service = FileService()



@router.post("/upload-file")
def upload_file(
    file: UploadFile = File(...),
    user_name: str = Form(...),
    bike_name: str = Form(...)
):
    return file_service.upload_file(file, user_name, bike_name)

