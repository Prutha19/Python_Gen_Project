import os
import shutil
import json
from fastapi import UploadFile
from pathlib import Path
from sqlalchemy.orm import Session
from PyPDF2 import PdfReader
from ..database import get_db_session
from ..models.FileUpload import FileUpload


class FileService:
    def __init__(self, upload_dir: str = "files"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

    def upload_file(self, file: UploadFile, user_name: str, bike_name: str) -> dict:
        file_path = self.upload_dir / bike_name / file.filename
        file_path.parent.mkdir(exist_ok=True)

        self._save_file_to_disk(file_path, file)
        metadata_path = self._create_metadata(file_path)
        self._save_file_record(user_name, str(file_path), bike_name)

        return {
            "message": "File uploaded successfully",
            "file_path": str(file_path),
            "metadata_path": metadata_path,
        }

    def _save_file_to_disk(self, file_path: Path, file: UploadFile) -> None:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    def _save_file_record(
        self, user_name: str, file_location: str, bike_name: str
    ) -> None:
        db: Session = get_db_session()
        try:
            file_upload = FileUpload(
                user_name=user_name, file_location=file_location, bike_name=bike_name
            )
            db.add(file_upload)
            db.commit()
            db.refresh(file_upload)
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def _create_metadata(self, file_path: Path) -> str:
        metadata = {}
        if file_path.suffix.lower() == ".pdf":
            text = self._extract_pdf_text(file_path)
            metadata = self._parse_text_to_dict(text)
        else:
            metadata = {"filename": file_path.name, "path": str(file_path)}

        metadata_path = file_path.with_suffix(".json")
        with open(metadata_path, "w", encoding="utf-8") as json_file:
            json.dump(metadata, json_file, ensure_ascii=False, indent=2)

        return str(metadata_path)

    def _extract_pdf_text(self, file_path: Path) -> str:
        reader = PdfReader(str(file_path))
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
        return "\n".join(text_parts)

    def _parse_text_to_dict(self, text: str) -> dict:
        result = {}
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        free_text = []
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()
            elif "=" in line:
                key, value = line.split("=", 1)
                result[key.strip()] = value.strip()
            else:
                free_text.append(line)

        if not result:
            result["content"] = "\n".join(free_text)
        elif free_text:
            if "content" in result:
                result["content"] += "\n" + "\n".join(free_text)
            else:
                result["content"] = "\n".join(free_text)

        return result
