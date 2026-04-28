from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime, timezone
from app.extensions import Base


class ProductRequest(Base):
    __tablename__ = "product_requests"

    id = Column(Integer, primary_key=True)
    product_name = Column(Text, nullable=False)
    features = Column(Text, nullable=False)   # disimpan sebagai JSON string
    platform = Column(Text, nullable=False)
    tone = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
