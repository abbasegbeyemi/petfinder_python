import cloudscraper
from bs4 import BeautifulSoup
import cloudscraper
from scraper.db_client import DBClient


BREEDS = ["ragdoll", "maine-coon"]
BASE_URL = "https://pets4homes.co.uk"


def get_scraper() -> cloudscraper.Session:
    scraper = cloudscraper.create_scraper()
    # Add a custom user-agent
    scraper.headers.update(
        {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})

    return scraper


def scrape_page(session: cloudscraper.Session, db_client: DBClient, url: str, current_index=0):
    """
    Scrape a page and print the results.
    """
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the search results div
    search_results = soup.find("div", attrs={"data-testid": "search-results"})

    if not search_results:
        print("No search results found")
        return 0

    # Get the div that contains the header for all adverts
    all_adverts_header = search_results.find(
        "div", attrs={"data-testid": "listings-list-feed-title-all"}
    )

    # Find all the listings in the search results, however we want to skip boosted listings
    listings = all_adverts_header.find_next_siblings(
        "div", attrs={"data-component": "ListingTile"})

    # Loop through the listings and get the information required
    for listing in listings:
        # Get the title of the listing
        title = listing.find("h2", attrs={"data-testid": "advert-title"}).text

        # Get the price of the listing
        price = listing.find(
            "span", attrs={"data-testid": "listing-price"}).text

        # Get the link to the listing
        link = listing.find(
            "a").get("href")

        # Get the age and breed of the listing
        listing_attributes = listing.find(
            "div", attrs={"data-component": "ListingTileAttributes"}).find_all("span")

        breed = listing_attributes[0].text
        age = " ".join(listing_attributes[1].text.split(" ")[1:])

        # Get the gender if available
        try:
            gender = listing_attributes[2].text
        except IndexError:
            gender = "Unknown"

        # Get the location of the listing
        location = listing.find(
            "span", attrs={"data-component": "ListingLocation"}).text

        # Check if the listing already exists in the database
        if db_client.check_listing_exists(title):
            print("Listing already exists")
            continue

        # Insert the listing into the database
        db_client.create_listing(
            title=title, price=price, link=f"{BASE_URL}{link}", breed=breed, age=age, gender=gender, location=location)

        # Print the results
        print(f"----- Listing {current_index + 1} -----")
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Link: {link}")
        print(f"Breed: {breed}")
        print(f"Age: {age}")
        print(f"Gender: {gender}")
        print(f"Location: {location}")

        current_index += 1

    return len(listings)
