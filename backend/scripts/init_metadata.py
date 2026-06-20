
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import engine
from app.db.base import Base
from app.models import (
    User,
    Organization,
    DatabaseConnection,
    QueryHistory,
    SavedQuery,
    AuditLog,
    UserPreferences,
    APIKey,
    Dashboard,
    DashboardWidget,
    ScheduledReport
)


def main():
    print("Creating metadata tables...")
    Base.metadata.create_all(bind=engine)
    print("Metadata tables created successfully!")


if __name__ == "__main__":
    main()

