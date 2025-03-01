from .database import Base
from sqlalchemy import Column, BigInteger, DateTime, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(BigInteger, nullable=False, primary_key=True,
                autoincrement=True, unique=True)
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    published = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, nullable=False, primary_key=True,
                autoincrement=True, unique=True)
    user_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False, index=True)
    active = Column(Boolean, nullable=False, server_default="True")
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), nullable=True)
