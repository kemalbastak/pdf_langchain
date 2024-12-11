from fastapi import UploadFile, HTTPException, Form, Depends
from pydantic import BaseModel, field_validator, computed_field
import magic
from uuid import uuid4, UUID
from apps.core.settings import settings
from datetime import datetime


class FileUpload(BaseModel):
    file: UploadFile

    @field_validator('file')
    @classmethod
    def validate_file(cls, file):
        # Read file content
        file_content = file.file.read()
        # Reset file pointer after reading
        file.file.seek(0)

        # Validate file size
        max_size_bytes = settings.FILE_MAX_SIZE_MB * 1024 * 1024  # Convert MB to bytes
        if len(file_content) > max_size_bytes:
            raise HTTPException(status_code=413,
                                detail=f"File size exceeds the limit of {settings.FILE_MAX_SIZE_MB} MB.")

        # Validate MIME type
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(file_content[:1000])
        if mime_type != "application/pdf":
            raise HTTPException(status_code=422, detail="Uploaded file is not a valid PDF.")

        return file

    @computed_field
    def file_uid(self) -> UUID:
        return uuid4()

    @computed_field
    @property
    def path(self) -> str:
        return f"{datetime.now().strftime('%Y/%m/%d')}/{str(self.file_uid)}.pdf"
