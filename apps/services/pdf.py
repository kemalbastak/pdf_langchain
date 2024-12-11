from apps.core.database import DBSessionDep
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.documents import Document

from apps.models import PDFUpload


class PDFService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_pdf(self, db_data: PDFUpload) -> PDFUpload:
        """
        Creates a PDF record in the database.

        :param db_data: The PDFUpload instance to be saved.
        :return: The saved PDFUpload instance.
        """
        self._session.add(db_data)  # Add the PDF record to the session
        await self._session.commit()  # Commit the transaction
        await self._session.refresh(db_data)  # Refresh the instance with database data
        return db_data

    async def create_chunked_pdf(self, documents: list[Document]):
        ...


# Dependency to get a PDFService instance with an async session
def get_pdf_service(session: DBSessionDep) -> PDFService:
    pdf_service = PDFService(session)
    return pdf_service
