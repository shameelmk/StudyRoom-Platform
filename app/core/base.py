from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Declarative base for SQLAlchemy models.
    Separated into its own module to avoid circular imports between
    `app.core.db` and `app.models`.
    """
    pass
