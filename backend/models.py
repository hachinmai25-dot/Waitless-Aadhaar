from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    aadhaar = Column(String)


class Center(Base):
    __tablename__ = "centers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    queue = Column(Integer)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    center_id = Column(Integer)
    slot = Column(String)
