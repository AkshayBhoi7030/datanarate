import uuid
from sqlalchemy import Column, String, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class APIKey(Base, TimestampMixin):
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    rate_limit = Column(Integer, default=1000, nullable=False)  # Requests per hour
    last_used_at = Column(TimestampMixin.created_at.type, nullable=True)

    organization = relationship("Organization")
    user = relationship("User", back_populates="api_keys")
