import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Dashboard(Base, TimestampMixin):
    __tablename__ = "dashboards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    layout = Column(JSON, nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)
    is_favorite = Column(Boolean, default=False, nullable=False)

    organization = relationship("Organization", back_populates="dashboards")
    user = relationship("User")
    widgets = relationship("DashboardWidget", back_populates="dashboard", cascade="all, delete-orphan")


class DashboardWidget(Base, TimestampMixin):
    __tablename__ = "dashboard_widgets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("dashboards.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    widget_type = Column(String(50), nullable=False)  # chart, table, kpi
    saved_query_id = Column(UUID(as_uuid=True), ForeignKey("saved_queries.id"), nullable=True)
    config = Column(JSON, nullable=True)
    position = Column(JSON, nullable=True)

    dashboard = relationship("Dashboard", back_populates="widgets")
