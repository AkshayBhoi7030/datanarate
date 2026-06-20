import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
import enum


class AuditAction(str, enum.Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTER = "register"
    CREATE_CONNECTION = "create_connection"
    UPDATE_CONNECTION = "update_connection"
    DELETE_CONNECTION = "delete_connection"
    EXECUTE_QUERY = "execute_query"
    SAVE_QUERY = "save_query"
    DELETE_QUERY = "delete_query"
    UPDATE_PROFILE = "update_profile"
    CREATE_DASHBOARD = "create_dashboard"
    UPDATE_DASHBOARD = "update_dashboard"
    DELETE_DASHBOARD = "delete_dashboard"
    CREATE_REPORT = "create_report"
    EXECUTE_REPORT = "execute_report"


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    action = Column(SQLEnum(AuditAction), nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    details = Column(Text, nullable=True)

    organization = relationship("Organization", back_populates="audit_logs")
    user = relationship("User", back_populates="audit_logs")
