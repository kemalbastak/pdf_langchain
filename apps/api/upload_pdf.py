from fastapi import APIRouter

from apps.celery.parser import handle_parse_pdf
from apps.core.database import DBSessionDep, get_db_session
from apps.models import PDFUpload
from apps.schemas.file import FileUpload, HTTPException
from fastapi import File, Depends
from apps.minio.minio_client import minio_client
from apps.services.pdf import get_pdf_service, PDFService
from sqlalchemy.ext.asyncio import AsyncSession

pdf_router = APIRouter(prefix='/v1')


@pdf_router.post("/pdf/")
async def upload_file(service: PDFService = Depends(get_pdf_service), file: FileUpload = File(...)):
    # Upload the file to MinIO
    file_path = file.path
    pdf_upload = PDFUpload(path=file_path, file=file.file.filename)
    created_pdf = await service.create_pdf(pdf_upload)
    uploaded_file_name = minio_client.upload_object(file_path, file.file)
    handle_parse_pdf.delay(uploaded_file_name)
    return {"pdf_id": f"{created_pdf.id}"}
