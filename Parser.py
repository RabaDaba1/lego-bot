import re

# Method to parse offer's price
def parse_price(price: str) -> float:
    price = price.replace(" ", "")
    price = price.replace("zł", "")
    price = price.replace(",", ".")

    return float(price)

# Method to parse offer's title
def parse_title(title: str) -> str:
    title = title.replace("\n", "")
    title = title.replace("\t", "")
    title = title.strip()

    return title

# Method to parse offer's description
def parse_description(description: str) -> str:
    description = description.replace("\n", " ")
    description = description.replace("\t", " ")
    description = description.strip()

    return description

# Method to parse offer's set id from title
def get_set_id(title: str) -> int:
    set_id = re.search(r"\b\d{4,5}\b", title).group()
    return int(set_id) or 0