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
