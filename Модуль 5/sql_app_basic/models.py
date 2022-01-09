from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base



class User_DB(Base):
    __tablename__ = "phonebook"

    user_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    phone_number = Column(String)
    age = Column(Integer)