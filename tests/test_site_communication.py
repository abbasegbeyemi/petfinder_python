import pytest
from scraper.utils import get_scraper

BASE_URL = "https://pets4homes.co.uk"


@pytest.fixture(scope="session")
def session():
    """
    Create a session for the scraper.
    """
    return get_scraper()


def test_connect_to_site(session):
    """
    Test that the scraper can connect to the site.
    """
    session = get_scraper()
    response = session.get(BASE_URL)
    assert response.status_code == 200
