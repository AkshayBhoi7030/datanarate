import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class QueryHistory(Base, TimestampMixin):
    __tablename__ = "query_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    database_connection_id = Column(UUID(as_uuid=True), ForeignKey("database_connections.id"), nullable=False, index=True)
    natural_language_query = Column(Text, nullable=False)
    generated_sql = Column(Text, nullable=False)
    execution_time_ms = Column(Integer, nullable=True)
    row_count = Column(Integer, nullable=True)
    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)

    organization = relationship("Organization", back_populates="query_history")
    user = relationship("User", back_populates="query_history")
    database_connection = relationship("DatabaseConnection", back_populates="query_history")
