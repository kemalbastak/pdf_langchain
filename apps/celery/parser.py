from apps.utils.pdf_parser import PDFParser
from .worker import celery_app


@celery_app.task(name="apps.celery.parser.handle_parse_pdf")
def handle_parse_pdf(file_path: str):
    parser = PDFParser(file_path)
    chunks = parser.chunked_docs

    return chunks

