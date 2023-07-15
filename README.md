# Lego Bot
![Tests](https://github.com/RabaDaba1/lego-bot/actions/workflows/tests.yml/badge.svg)

Lego-Bot is a project mainly build for lego investors to help them make more accurate predictions. It uses Pandas, Beautiful Soup, Seaborn and SQLite libraries. The program scrapes Lego set listings from a website (OLX.pl) and checks their prices or whether they have been sold every day.

## Getting Started

To get started with Lego-Bot with all the dependencies, you just need to install it like a library:
```python
pip install path_to_lego_bot_folder
```

## Usage

Example of Lego Bot usage is in `tutorial.ipynb`

### The `Set` object
Most important object of this library. It is the highest layer that allows for very simple communication with database, scrapers etc. Set object 
```python
Set(set_id: int, scrape_and_update_database=True)
```
`set_id: int` is a number of a lego set, 4-5 digit integer

`scrape_and_update_database` object will autmoatically scrape offers and update database with them when created

### Adding a new set to the database
Set that is not in database is automatically added when new `Set` object is created. You can also add it manually by calling `Set.add_set(set_id)`

### Deleting a set from the database
Call `Set.delete_set(set_id)`

### How offer is represented in the database
**Columns**:
- offer_id (OLX offer id): int
- url: str
- set_id (lego set number): int
- date_added: datetime
- date_sold: datetime
- title: str
- description: str
- price: float
- is_negotiable: bool
- is_active: bool

## Contributing

If you would like to contribute to Lego-Bot, please fork the repository and submit a pull request.

## License

Lego-Bot is licensed under the MIT License. See `LICENSE` for more information.
