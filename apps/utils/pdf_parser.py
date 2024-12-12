from tempfile import NamedTemporaryFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from apps.minio.minio_client import minio_client
from apps.es.elasticsearch_logger import logger


class PDFParser:
    def __init__(self, file_path: str, chunk_size=100, chunk_overlap=10):
        """
        Initialize the PDFParser class.

        :param file_path: Path to the PDF file.
        :param chunk_size: The maximum size of each chunk (in number of characters).
        :param chunk_overlap: The overlap between chunks.
        """
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        logger.info(
            f"Initializing PDFParser with file_path: {self.file_path}, chunk_size: {self.chunk_size}, chunk_overlap: {self.chunk_overlap}")

        try:
            # Load the PDF
            self.documents = self.load_pdf()

            # Text splitter to chunk the documents
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            )
            logger.info("Text splitter initialized.")

            self.chunked_docs = self.text_splitter.split_documents(self.documents)
            logger.info(f"PDF split into {len(self.chunked_docs)} chunks.")

        except Exception as e:
            logger.error(f"Error initializing PDFParser: {e}")
            raise

    def get_chunked_documents(self):
        """
        Returns the chunked documents.
        """
        logger.info(f"Fetching {len(self.chunked_docs)} chunked documents.")
        return self.chunked_docs

    def load_pdf(self):
        """
        Loads the PDF from MinIO and returns the documents.
        """
        logger.info(f"Loading PDF from MinIO: {self.file_path}")

        try:
            file_obj = minio_client.read_object(self.file_path)
            with NamedTemporaryFile(suffix=".pdf") as tmp_file:
                tmp_file.write(file_obj.read())
                tmp_file_path = tmp_file.name
                logger.info(f"PDF saved to temporary file: {tmp_file_path}")

                loader = PyMuPDFLoader(tmp_file_path)
                docs = loader.load()
                logger.info(f"Loaded {len(docs)} documents from the PDF.")
            return docs

        except Exception as e:
            logger.error(f"Error loading PDF {self.file_path} from MinIO: {e}")
            raise
