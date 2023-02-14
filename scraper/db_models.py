from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PetListing(Base):
    """
    A pet listing.
    """
    __tablename__ = "pet_listings"
    id = Column(Integer, primary_key=True)
    title_hash = Column(String, unique=True)
    title = Column(String)
    price = Column(String)
    link = Column(String)
    breed = Column(String)
    age = Column(String)
    gender = Column(String)
    location = Column(String)
