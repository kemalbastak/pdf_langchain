from apps.utils.db import TimeStampMixin
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .chat_models import GeminiAIMessage

class PDFUpload(TimeStampMixin):
    __tablename__ = 'pdf_upload'

    path: Mapped[str] = mapped_column(String(500), index=True, unique=True)
    file: Mapped[str] = mapped_column(String(500))

    # Relationships
    pdf_contents: Mapped[list["PDFContent"]] = relationship('PDFContent', back_populates='pdf_upload')
    ai_messages: Mapped[list["GeminiAIMessage"]] = relationship('GeminiAIMessage', back_populates='pdf_upload')


class PDFContent(TimeStampMixin):
    __tablename__ = 'pdf_content'

    page_content: Mapped[str] = mapped_column(String)  # Store page content as String
    pdf_metadata: Mapped[dict] = mapped_column(JSON)  # Store metadata as JSON

    pdf_upload_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('pdf_upload.id'))
    pdf_upload: Mapped[PDFUpload] = relationship("PDFUpload", back_populates="pdf_contents")

    content_order: Mapped[int] = mapped_column(Integer)


