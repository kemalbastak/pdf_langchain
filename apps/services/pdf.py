from apps.core.database import DBSessionDep, get_db_session, sessionmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from langchain_core.documents import Document
from fastapi import Depends, HTTPException
from apps.models import PDFUpload
from apps.models.file_models import PDFContent
from apps.utils.exceptions import NotFoundError
from apps.utils.nlp import clean_text


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

    async def create_chunked_pdf(self, pdf_upload_id: str, documents: list[Document]):
        pdf_list = []
        pdf_list = [PDFContent(pdf_upload_id=pdf_upload_id,
                               page_content=clean_text(document.page_content),
                               pdf_metadata=document.metadata,
                               content_order=index) for index, document in enumerate(documents, start=1)]

        self._session.add_all(pdf_list)
        await self._session.commit()
        pdf_upload = await self.get_by_id(pdf_upload_id)

        return pdf_upload

    async def get_by_id(self, pdf_upload_id: str) -> PDFUpload:
        """
        Retrieves a PDFUpload record by its ID.

        :param pdf_upload_id: The ID of the PDFUpload instance to be retrieved.
        :return: The retrieved PDFUpload instance.
        :raises HTTPException: If the PDFUpload is not found.
        """
        query = (
            select(PDFUpload)
            .options(selectinload(PDFUpload.pdf_contents))  # Eagerly load relationships
            .where(PDFUpload.id == pdf_upload_id)
        )
        pdf_upload = (await self._session.execute(query)).scalar_one_or_none()

        if not pdf_upload:
            raise NotFoundError()

        return pdf_upload


# Dependency to get a PDFService instance with an async session
def get_pdf_service(session: DBSessionDep) -> PDFService:
    pdf_service = PDFService(session)
    return pdf_service
