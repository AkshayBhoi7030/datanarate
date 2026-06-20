from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class DataNarrateException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None,
        error_code: Optional[str] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


class NotFoundException(DataNarrateException):
    def __init__(self, detail: Any = "Resource not found", error_code: str = "NOT_FOUND"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code,
        )


class BadRequestException(DataNarrateException):
    def __init__(self, detail: Any = "Bad request", error_code: str = "BAD_REQUEST"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code,
        )


class UnauthorizedException(DataNarrateException):
    def __init__(self, detail: Any = "Unauthorized", error_code: str = "UNAUTHORIZED"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
        )


class ForbiddenException(DataNarrateException):
    def __init__(self, detail: Any = "Forbidden", error_code: str = "FORBIDDEN"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code,
        )


class ConflictException(DataNarrateException):
    def __init__(self, detail: Any = "Conflict", error_code: str = "CONFLICT"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code,
        )


class InternalServerErrorException(DataNarrateException):
    def __init__(self, detail: Any = "Internal server error", error_code: str = "INTERNAL_SERVER_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code,
        )


class UnsafeSQLException(DataNarrateException):
    def __init__(self, detail: Any = "Unsafe SQL query detected", error_code: str = "UNSAFE_SQL"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code,
        )
