from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .db_models import Base, PetListing
import hashlib


class DBClient:
    """
    This class is responsible for connecting to the database and executing
    queries. It will create sn sqlite database
    """

    def __init__(self, url="sqlite:///./data.db"):
        self.engine = create_engine(url, echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create the tables
        Base.metadata.create_all(self.engine)

    def __hash_title(self, title: str):
        """
        Hash the title of the listing.
        """
        sha256 = hashlib.sha256()
        sha256.update(title.encode('utf-8'))
        return sha256.hexdigest()

    def create_listing(self, title: str, price: str, breed: str, age: str, link: str, location: str, gender: str = "Unknown"):
        """
        Create a listing in the database.
        """
        new_listing = PetListing(
            title=title,
            title_hash=self.__hash_title(title),
            price=price,
            breed=breed,
            age=age,
            link=link,
            gender=gender,
            location=location,
        )

        self.session.add(new_listing)
        self.session.commit()

    def get_listing_by_title(self, title: str):
        """
        Get a listing by its title, but use the title hash to speed up the query.
        """
        return (
            self.session.query(PetListing)
            .filter_by(title_hash=self.__hash_title(title))
            .first()
        )

    def check_listing_exists(self, title: str):
        """
        Check if a listing exists by its title.
        """
        return self.get_listing_by_title(title) is not None
