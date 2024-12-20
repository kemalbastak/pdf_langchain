from apps.utils.pdf_parser import PDFParser


def handle_parse_pdf(file_path: str):
    parser = PDFParser(file_path)
    chunks = parser.chunked_docs
    return chunks
