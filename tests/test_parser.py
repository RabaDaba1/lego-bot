import pytest
import datetime
from lego_bot_rabadaba1 import Parser


@pytest.mark.parametrize("price, expected", [
    ("0,1 zł", 0.1),
    ("1 zł", 1),
    ("123,45 zł", 123.45),
    ("123 456.78 zł", 123456.78)
])
def test_price_parser(price: str, expected: float):
    assert Parser.parse_price(price) == expected


@pytest.mark.parametrize("title, expected", [
    ("LEGO 1234", "LEGO 1234"),
    ("LEGO 1234\n", "LEGO 1234"),
    ("LEGO 1234\t", "LEGO 1234"),
    ("LEGO 1234\n\t", "LEGO 1234"),
    ("\n\tLEGO 1234", "LEGO 1234"),
    ("   LEGO 1234 ", "LEGO 1234"),
])
def test_title_and_description_parser(title: str, expected: str):
    assert Parser.parse_title(title) == expected
    assert Parser.parse_description(title) == expected


@pytest.mark.parametrize("id, expected", [
    ("1234", 1234),
    (" 1234 ", 1234),
    ("1234\n", 1234),
    ("LEGO 12345", 12345),
    ("LEGO 12345 Ahsoka Tano", 12345),
    ("LEGO 123 4567 Darth Vader", 4567),
    ("LEGO 123456 Obi-Wan Kenobi", None),
    ("LEGO 1234Star Wars", None),
])
def test_set_id_parser(id: str, expected: int or None):
    assert Parser.parse_set_id(id) == expected

def test_set_id_parser_exception():
    with pytest.raises(Exception):
        Parser.parse_set_id("LEGO 1234 4567")


def test_offer_id_parser():
    assert Parser.parse_offer_id("https://www.olx.pl/d/oferta/lego-40539-brickheadz-ahsoka-tano-star-wars-nowe-klocki-nowy-zestaw-CID88-IDPGlrI.html") == "CID88-IDPGlrI"
    
@pytest.mark.parametrize("date, expected", [
    ("Dzisiaj o 07:53", datetime.date.today()),
    ("10 maja 2023", datetime.date(2023, 5, 10))
])
def test_date_parser(date: str, expected: datetime.date):
    assert Parser.parse_date(date) == expected
    

def test_remove_accents():
    assert Parser.remove_accents("ąćęłńóśźż") == "acelnoszz"