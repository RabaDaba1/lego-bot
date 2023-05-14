from bs4 import BeautifulSoup
import requests

class OfferScraper:
    """
    A class for scraping data from a single offer

    Attributes:
    -----------
    url: str
        URL of the offer
    offer: BeautifulSoup
        BeautifulSoup object of the offer
    
    Methods:
    --------
    scrape_date() -> str
        Scrapes the date of the offer
    scrape_price() -> str
        Scrapes the price of the offer
    scrape_title() -> str
        Scrapes the title of the offer
    scrape_description() -> str
        Scrapes the description of the offer
    is_active() -> bool
        Checks if the offer is active
    scrape_negotiable() -> bool
        Scrapes if the offer is negotiable

    Decorators:
    -----------
    catch_exceptions(func)
        Decorator to catch exceptions while scraping
    """
    url: str
    offer: BeautifulSoup

    def __init__(self, url: str):
        self.url = url
        self.offer = BeautifulSoup(requests.get(url).text, 'lxml')

    def catch_exceptions(func):
        """Decorator to catch exceptions while scraping"""
        def wrapper(self):
            try:
                return func(self)
            except:
                print('Error while executing' + func.__name__)
                raise Exception('Error while executing' + func.__name__)
        return wrapper
    
    @catch_exceptions
    def scrape_date(self):
        return self.offer.select_one('span[data-cy="ad-posted-at"]').text

    @catch_exceptions
    def scrape_price(self):
        return self.offer.find('h3', class_='css-ddweki er34gjf0').text

    @catch_exceptions
    def scrape_title(self):
        return self.offer.find('h1').text
    
    @catch_exceptions
    def scrape_description(self):
        return self.offer.find('div', class_='css-bgzo2k er34gjf0').text

    @catch_exceptions
    def is_active(self) -> bool:
        return True if self.offer.find('h1') else False
    
    @catch_exceptions
    def scrape_negotiable(self) -> bool:
        is_negotiable_el = self.offer.find(attrs = { 'data-testid': "negotiable-label" })

        return True if is_negotiable_el else False
    

class SetScraper:
    """
    A class for scraping all offers for a single LEGO set

    Attributes:
    -----------
    set_id: int
        LEGO set number
    url: str
        URL of the first page with offers
    used: bool
        If True, scrapes only used sets, otherwise scrapes only new sets
    
    Methods:
    --------
    get_all_sets() -> list
        Scrapes all OLX offers for a set
    get_sets(page: int) -> list
        Scrapes offers from a single page
    """

    def __init__(self, set_id: int, used = False):
        self.set_id = set_id
        self.url = f'https://www.olx.pl/oferty/q-lego-{set_id}/'
        self.used = used
    
    def get_all_sets(self) -> list:
        offer_page = BeautifulSoup(requests.get(self.url).text, 'lxml')
        page_count = int(offer_page.select_one('ul.pagination-list > li:last-of-type').text)

        offer_links = []
        for i in range(1, page_count + 1):
            offer_links += self.get_sets(i)

        # Delete duplicates (some offer adverts are on multiple pages)
        offer_links = list(dict.fromkeys(offer_links))

        return offer_links
    
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