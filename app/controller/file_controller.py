from fastapi import APIRouter, UploadFile, File, Form, Depends
from ..service.FileService import FileService
from ..service.AuthService import has_any_role

router = APIRouter(prefix="/files", tags=["File APIS"])

file_service = FileService()

@router.post("/upload-file")
def upload_file(
    file: UploadFile = File(...),
    user_name: str = Form(...),
    bike_name: str = Form(...),
    _auth: dict = Depends(has_any_role(["ROLE_ADMIN"]))
):
    return file_service.upload_file(file, user_name, bike_name)


