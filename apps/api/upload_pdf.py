from fastapi import APIRouter, File, Depends, HTTPException
from apps.celery.parser import handle_parse_pdf
from apps.models import PDFUpload
from apps.schemas.file import FileUpload
from apps.minio.minio_client import minio_client
from apps.services.pdf import get_pdf_service, PDFService
from apps.es.elasticsearch_logger import logger

pdf_router = APIRouter(prefix='/v1', tags=["PDF"])

@pdf_router.post("/pdf")
async def upload_file(service: PDFService = Depends(get_pdf_service), file: FileUpload = File(...)):
    logger.info(f"Received file upload request for file: {file.file.filename}")

    try:
        # Upload the file to MinIO
        file_path = file.path
        pdf_upload = PDFUpload(path=file_path, file=file.file.filename)
        created_pdf = await service.create_pdf(pdf_upload)
        logger.info(f"PDF record created in database with ID: {created_pdf.id}")

        # Upload the file to MinIO storage
        uploaded_file_name = minio_client.upload_object(file_path, file.file)
        logger.info(f"File uploaded to MinIO with filename: {uploaded_file_name}")

        # Handle PDF parsing using Celery task
        chunk = handle_parse_pdf(uploaded_file_name)
        logger.info(f"PDF parsed successfully. Chunk data: {chunk}")

        # Store the chunked PDF data in the database
        pdf_chunk = await service.create_chunked_pdf(str(created_pdf.id), chunk)
        logger.info(f"Chunked PDF data created for PDF ID: {created_pdf.id}")

        return {"pdf_id": f"{created_pdf.id}"}

    except Exception as e:
        logger.error(f"Error processing file upload for {file.file.filename}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
