import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
import enum


class ReportFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ScheduledReport(Base, TimestampMixin):
    __tablename__ = "scheduled_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("dashboards.id"), nullable=True)
    saved_query_id = Column(UUID(as_uuid=True), ForeignKey("saved_queries.id"), nullable=True)
    frequency = Column(SQLEnum(ReportFrequency), nullable=False)
    recipients = Column(JSON, nullable=True)  # List of emails
    format = Column(String(20), default="pdf", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_run_at = Column(TimestampMixin.created_at.type, nullable=True)
    next_run_at = Column(TimestampMixin.created_at.type, nullable=True)

    organization = relationship("Organization", back_populates="scheduled_reports")
    user = relationship("User")
    dashboard = relationship("Dashboard")
    saved_query = relationship("SavedQuery")
