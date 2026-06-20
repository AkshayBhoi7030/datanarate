import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    users = relationship("User", back_populates="organization")
    database_connections = relationship("DatabaseConnection", back_populates="organization")
    query_history = relationship("QueryHistory", back_populates="organization")
    saved_queries = relationship("SavedQuery", back_populates="organization")
    audit_logs = relationship("AuditLog", back_populates="organization")
    dashboards = relationship("Dashboard", back_populates="organization")
    scheduled_reports = relationship("ScheduledReport", back_populates="organization")
