from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column


class ImagesModel(Base):
    name: Mapped[str] = mapped_column(unique=True)
