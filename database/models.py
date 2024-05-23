import uuid

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID

from database.connection import Base, engine


class Rectangles(Base):
    __tablename__ = "rectangles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
    x3 = Column(Float)
    y3 = Column(Float)
    x4 = Column(Float)
    y4 = Column(Float)


Base.metadata.create_all(engine)
