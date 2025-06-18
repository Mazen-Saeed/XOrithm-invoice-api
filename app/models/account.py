from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base

class Account(Base):
    __tablename__ = "accounts"

    # Primary key(auto incrementing)
    id = Column(Integer, primary_key=True, index=True)

    # name of user
    name = Column(String, nullable=False)

    # email of user
    email= Column(String, unique=True, nullable=False)

    # invoices created by the user
    invoices = relationship("Invoice", back_populates="account", cascade="all, delete")
