import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class SavedQuery(Base, TimestampMixin):
    __tablename__ = "saved_queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    natural_language_query = Column(Text, nullable=False)
    generated_sql = Column(Text, nullable=False)
    tags = Column(JSON, nullable=True)  # Use JSON for better compatibility
    is_favorite = Column(Boolean, default=False, nullable=False)

    organization = relationship("Organization", back_populates="saved_queries")
    user = relationship("User", back_populates="saved_queries")
