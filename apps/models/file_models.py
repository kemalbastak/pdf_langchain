from apps.utils.db import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class PDFUpload(TimeStampMixin):
    path: Mapped[str] = mapped_column(String(500))
    file: Mapped[str] = mapped_column(String(500))



