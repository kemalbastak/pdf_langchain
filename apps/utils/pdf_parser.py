from tempfile import NamedTemporaryFile

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, S3FileLoader
from io import BytesIO, StringIO

from apps.core import settings
from apps.minio.minio_client import minio_client
import boto3

class PDFParser:
    def __init__(self, file_path: str, chunk_size=1500, chunk_overlap=200):
        """
        Initialize the PDFParser class.

        :param pdf_path: PDF data in bytes.
        :param chunk_size: The maximum size of each chunk (in number of characters).
        :param chunk_overlap: The overlap between chunks.
        """
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Load the PDF


        self.documents = self.load_pdf()

        # Text splitter to chunk the documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        self.chunked_docs = self.text_splitter.split_documents(self.documents)


    def get_chunked_documents(self):
        """
        Returns the chunked documents.
        """
        return self.chunked_docs

    def load_pdf(self):
        file_obj = minio_client.read_object(self.file_path)
        with NamedTemporaryFile(suffix=".pdf") as tmp_file:
            tmp_file.write(file_obj.read())
            tmp_file_path = tmp_file.name
            loader = PyMuPDFLoader(tmp_file_path)
            docs = loader.load()
        return docs