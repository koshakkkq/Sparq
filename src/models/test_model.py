from sqlalchemy.orm import Mapped

from .base_model import Base


class TestModel(Base):
    __tablename__ = "test_table"

    value: Mapped[str]
