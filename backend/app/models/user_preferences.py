import uuid
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class UserPreferences(Base, TimestampMixin):
    __tablename__ = "user_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    theme = Column(String, default="light", nullable=False)
    dashboard_settings = Column(JSON, default=dict, nullable=False)
    saved_filters = Column(JSON, default=list, nullable=False)
    preferred_chart_type = Column(String, default="bar", nullable=False)

    user = relationship("User", back_populates="preferences")
