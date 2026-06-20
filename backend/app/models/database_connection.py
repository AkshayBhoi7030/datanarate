import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
import enum


class DatabaseType(str, enum.Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLSERVER = "sqlserver"
    SQLITE = "sqlite"


class DatabaseConnection(Base, TimestampMixin):
    __tablename__ = "database_connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    db_type = Column(SQLEnum(DatabaseType), nullable=False)
    host = Column(String(255), nullable=False)
    port = Column(String(10), nullable=False)
    database = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    encrypted_password = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    organization = relationship("Organization", back_populates="database_connections")
    user = relationship("User", back_populates="database_connections")
    query_history = relationship("QueryHistory", back_populates="database_connection", cascade="all, delete-orphan")
