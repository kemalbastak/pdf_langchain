from apps.utils.db import TimeStampMixin
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from langchain_core.messages.ai import AIMessage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .file_models import PDFUpload


class GeminiAIMessage(TimeStampMixin):
    __tablename__ = 'ai_message'
    content: Mapped[str] = mapped_column(String)
    additional_kwargs: Mapped[dict] = mapped_column(JSON)
    response_metadata: Mapped[dict] = mapped_column(JSON)
    usage_metadata: Mapped[dict] = mapped_column(JSON)

    pdf_upload_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('pdf_upload.id'))
    pdf_upload: Mapped["PDFUpload"] = relationship("PDFUpload", back_populates="ai_messages")

    user_message: Mapped[str] = mapped_column(String)

    def from_response(self, response: AIMessage, **kwargs) -> "GeminiAIMessage":
        self.content = response.content
        self.additional_kwargs = response.additional_kwargs
        self.response_metadata = response.response_metadata
        self.usage_metadata = response.usage_metadata
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self