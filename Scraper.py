from bs4 import BeautifulSoup
import requests

# Class for scraping single offer details
class OfferScraper:
    url: str
    offer: BeautifulSoup

    # Constructor
    def __init__(self, url: str):
        self.url = url
        self.offer = BeautifulSoup(requests.get(url).text, 'lxml')

    # Method to scrape price
    def scrape_price(self):
        return self.offer.find('h3', class_='css-ddweki er34gjf0').text

    # Method to scrape title
    def scrape_title(self):
        return self.offer.find('h1').text
    
    # Method to scrape description
    def scrape_description(self):
        return self.offer.find('div', class_='css-bgzo2k er34gjf0').text

    # Method to check if offer is active
    def is_active(self) -> bool:
        return True if self.offer.find('h1') else False
    
    # Method to check if offer is negotiable
    def scrape_negotiable(self) -> bool:
        is_negotiable_el = self.offer.find(attrs = { 'data-testid': "negotiable-label" })

        return True if is_negotiable_el else False
    

# Class for scraping all offers for given set
class SetScraper:
    def __init__(self, set_id: int, used = False):
        self.set_id = set_id
        self.url = f'https://www.olx.pl/oferty/q-lego-{set_id}/'
        self.used = used
    
    # Method for scraping all offers
    def get_all_sets(self) -> list:
        offer_page = BeautifulSoup(requests.get(self.url).text, 'lxml')
        page_count = int(offer_page.select_one('ul.pagination-list > li:last-of-type').text)

        offer_links = []
        for i in range(1, page_count + 1):
            offer_links += self.get_sets(i)

        # Delete duplicates (some offer adverts are on multiple pages)
        offer_links = list(dict.fromkeys(offer_links))

        return offer_links
    
    # Method for scraping offers from single page
    def get_sets(self, page: int) -> list:
        offer_page_url = self.url + f'?page={page}'
        offer_page = BeautifulSoup(requests.get(offer_page_url).text, 'lxml')

        offers = offer_page.select('div[data-cy=l-card]')

        if self.used:
            offers = [offer for offer in offers if offer.select_one('span[title=Używane]')]
        else:
            offers = [offer for offer in offers if offer.select_one('span[title=Nowe]')]

        offer_links = ['https://www.olx.pl' + offer.a['href'] for offer in offers]

        return offer_links