from scraper.db_client import DBClient
import tempfile
import pytest
from sqlalchemy.exc import IntegrityError


def test_can_create_db_client():
    """
    Test that the DBClient can be created.
    """
    temp_dir = tempfile.TemporaryDirectory()
    db_client = DBClient(f"sqlite:///{temp_dir.name}/data.db")
    assert db_client is not None


@pytest.fixture(scope="function")
def db_client():
    """
    Create a temporary database for the tests.
    """
    temp_dir = tempfile.TemporaryDirectory()
    with temp_dir:
        yield DBClient(f"sqlite:///{temp_dir.name}/data.db")


def test_can_create_listing_in_db(db_client):
    """
    Test that a listing can be created in the database.
    """
    db_client.create_listing(
        title="Test Listing",
        price="£100",
        breed="ragdoll",
        age="1 year",
        location="London",
        link="https://pets4homes.co.uk",
    )

    listing = db_client.get_listing_by_title("Test Listing")
    assert listing is not None
    assert listing.title == "Test Listing"
    assert listing.price == "£100"
    assert listing.breed == "ragdoll"
    assert listing.age == "1 year"
    assert listing.location == "London"
    assert listing.link == "https://pets4homes.co.uk"


def test_can_get_listing_by_title(db_client):
    """
    Test that a listing can be retrieved by its title.
    """
    db_client.create_listing(
        title="Another Test Listing",
        price="£100",
        breed="ragdoll",
        age="1 year",
        location="London",
        link="https://pets4homes.co.uk",
    )

    listing = db_client.get_listing_by_title("Another Test Listing")
    assert listing is not None
    assert listing.title == "Another Test Listing"
    assert listing.price == "£100"
    assert listing.breed == "ragdoll"
    assert listing.age == "1 year"
    assert listing.location == "London"
    assert listing.link == "https://pets4homes.co.uk"


def test_will_fail_if_not_unique_title(db_client):
    """
    Test that a listing cannot be created if the title is not unique.
    """
    db_client.create_listing(
        title="Test Listing",
        price="£100",
        breed="ragdoll",
        age="1 year",
        location="London",
        link="https://pets4homes.co.uk",
    )

    # This will raise an IntegrityError because the title is not unique.
    with pytest.raises(IntegrityError):
        db_client.create_listing(
            title="Test Listing",
            price="£100",
            breed="ragdoll",
            age="1 year",
            location="London",
            link="https://pets4homes.co.uk",
        )


def test_checking_if_listing_exists(db_client):
    """
    Test that the check_listing_exists method works.
    """
    db_client.create_listing(
        title="Test Listing",
        price="£100",
        breed="ragdoll",
        age="1 year",
        location="London",
        link="https://pets4homes.co.uk",
    )

    assert db_client.check_listing_exists("Test Listing") is True
    assert db_client.check_listing_exists("Non Existent Listing") is False
