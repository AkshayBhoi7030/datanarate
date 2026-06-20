from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.core.logging import logger


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def get_user(self, user_id):
        logger.debug(f"Fetching user: {user_id}")
        return self.repository.get(user_id)

    def get_user_by_email(self, email):
        logger.debug(f"Fetching user by email: {email}")
        return self.repository.get_by_email(email)
