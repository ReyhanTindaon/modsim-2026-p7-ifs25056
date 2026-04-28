from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base


class Description(Base):
    __tablename__ = "descriptions"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    request_id = Column(Integer, ForeignKey("product_requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
