from fastapi import APIRouter
from apps.core import settings
from apps.models import GeminiAIMessage
from apps.schemas.llm import ChatMessage, GeminiResponse
from fastapi import Depends, HTTPException
from uuid import UUID
from apps.services.chat import ChatService, get_chat_service
from apps.utils.llm import GeminiChat
from apps.es.elasticsearch_logger import logger

chat_router = APIRouter(prefix=settings.API_V1_STR, tags=["Chat"])

@chat_router.post("/chat/{pdf_id}/", response_model=GeminiResponse)
async def chat_pdf(pdf_id: UUID, message: ChatMessage, service: ChatService = Depends(get_chat_service)):
    logger.info(f"Received chat request for PDF with ID: {pdf_id} and user message: {message.message}")

    # Retrieve the PDF data
    pdf_text = await service.get_by_pdf_id(str(pdf_id))
    logger.info(f"Successfully retrieved PDF content for PDF ID: {pdf_id}")

    # Construct content for the AI response
    content = ' '.join([content.page_content for content in pdf_text.pdf_contents])
    logger.info(f"Content extracted from PDF, length: {len(content)} characters")

    # Generate AI response
    ai_response = GeminiChat().construct_prompt(content, message.message).get_response()
    logger.info(f"AI response generated: {ai_response.content}")

    # Log AI response model data for debugging (optional, could be verbose)
    logger.debug(f"AI response model dump: {ai_response.model_dump()}")

    # Create and save the chat record in the database
    instance = GeminiAIMessage().from_response(ai_response, pdf_upload_id=str(pdf_id), user_message=message.message)
    created_response = await service.create_chat(instance)
    logger.info(f"Successfully created chat message in the database for PDF ID: {pdf_id}")

    return GeminiResponse(response=ai_response.content)


