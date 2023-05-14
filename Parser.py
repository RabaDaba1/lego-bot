import datetime
import re


def parse_price(price: str) -> float:
    """Method to parse offer's price from string to float"""

    price = price.replace(" ", "")
    price = price.replace("zł", "")
    price = price.replace(",", ".")

    return float(price)

def parse_title(title: str) -> str:
    """Method to parse offer's title"""

    title = title.replace("\n", "")
    title = title.replace("\t", "")
    title = title.strip()

    return title

def parse_description(description: str) -> str:
    """Method to parse offer's description"""

    description = description.replace("\n", " ")
    description = description.replace("\t", " ")
    description = description.strip()

    return description

def get_set_id(title: str) -> int:
    """Method to parse LEGO set number from title"""

    set_id = re.search(r"\b\d{4,5}\b", title).group()
    return int(set_id) or 0

def parse_id(url: str) -> str:
    """Method to parse offer's ID from URL"""
    return '-'.join(url[:-5].split('-')[-2:])

def parse_date(date: str) -> str:
    """Method to parse offer's date"""
    date.strip()

    # Date can be in 2 formats:
    # 1. Dzisiaj o 07:53
    # 2. 10 maja 2023
    if date.startswith('Dzisiaj'):
        date = datetime.date.today()
    else:
        months = {
            'stycznia': 1,
            'lutego': 2,
            'marca': 3,
            'kwietnia': 4,
            'maja': 5,
            'czerwca': 6,
            'lipca': 7,
            'sierpnia': 8,
            'września': 9,
            'października': 10,
            'listopada': 11,
            'grudnia': 12
        }

        date = date.split(' ')
        date[1] = months[date[1]]

        date = datetime.date(int(date[2]), int(date[1]), int(date[0]))

    return date