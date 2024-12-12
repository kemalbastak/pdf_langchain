from apps.core.database import DBSessionDep, get_db_session, sessionmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from langchain_core.documents import Document
from fastapi import Depends, HTTPException
from apps.models import GeminiAIMessage, PDFUpload
from apps.utils.exceptions import NotFoundError
from apps.es.elasticsearch_logger import logger

class ChatService:
    def __init__(self, session: AsyncSession):
        self._session = session
        logger.info("ChatService initialized with a session.")

    async def create_chat(self, db_data: GeminiAIMessage) -> GeminiAIMessage:
        """
        Creates a Chat record in the database.

        :param db_data: The AIMessage instance to be saved.
        :return: The saved AIMessage instance.
        """
        logger.info(f"Creating a new chat with data: {db_data}")
        try:
            self._session.add(db_data)
            await self._session.commit()
            await self._session.refresh(db_data)
            logger.info(f"Chat created successfully with ID: {db_data.id}")
            return db_data
        except Exception as e:
            logger.error(f"Error occurred while creating chat: {e}")
            raise HTTPException(status_code=500, detail="Failed to create chat.")

    async def get_by_pdf_id(self, pdf_upload_id: str) -> PDFUpload:
        logger.info(f"Fetching PDF upload with ID: {pdf_upload_id}")
        try:
            query = (
                select(PDFUpload)
                .options(selectinload(PDFUpload.pdf_contents))
                .where(PDFUpload.id == pdf_upload_id)
            )
            pdf_upload = (await self._session.execute(query)).scalar_one_or_none()

            if not pdf_upload:
                logger.warning(f"PDF upload with ID {pdf_upload_id} not found.")
                raise NotFoundError()

            logger.info(f"PDF upload with ID {pdf_upload_id} found.")
            return pdf_upload
        except NotFoundError:
            logger.error(f"PDF upload with ID {pdf_upload_id} was not found.")
            raise
        except Exception as e:
            logger.error(f"Error occurred while fetching PDF upload: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch PDF upload.")

# Dependency to get a ChatService instance with an async session
def get_chat_service(session: DBSessionDep) -> ChatService:
    chat_service = ChatService(session)
    return chat_service
