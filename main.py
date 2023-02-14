from bs4 import BeautifulSoup
import sys
from scraper.utils import BREEDS, BASE_URL, get_scraper, scrape_page
from scraper.enums import AdvertiserType, Distance, AgeRange
from time import sleep
import random
from scraper.db_client import DBClient


def main(breed: str):
    db_client = DBClient()
    scraper = get_scraper()
    location = "wolverhampton"

    print(f"Scraping {' '.join(breed.split('-'))} kittens in {location}...")

    # Define the url parameters
    params = {
        "distance": Distance.FIFTY_MILES.value,
        "dateOfBirth": [AgeRange.KITTEN.value, AgeRange.JUVENILE.value],
        "advertiserType": [AdvertiserType.BREEDER.value, AdvertiserType.RESCUE_CHARITY.value]
    }

    url = f"{BASE_URL}/sale/kittens/{breed}/{location}/"

    # Go to the page
    response = scraper.get(url, params=params)

    soup = BeautifulSoup(response.text, "html.parser")

    # Print the numeber of listings available
    search_response = soup.find(
        "div", attrs={"data-component": "ListingsHeader"}).find("h2")

    print(f"Number of listings found: {search_response.text}")

    # The first word in search_response is the number of listings
    listings_count = int(search_response.text.split()[0])

    if not listings_count:
        return

    # Get the pages links
    pages = soup.find(
        "div", attrs={"data-testid": "pagination-pages-desktop"}).find_all("a")

    # Loop through the pages and scrape the data
    index = 0
    for page in pages:
        listings_count = scrape_page(
            scraper, db_client, f'{BASE_URL}{page.get("href")}', index)

        index += listings_count

        # Sleep for a random amount of time to avoid being blocked
        sleep(random.randint(1, 3))

    print("Finished scraping")


if __name__ == "__main__":
    # Get the command line arguments
    breed = sys.argv[1]
    print(breed)
    main(breed=breed)
