# Lego Bot
![Tests](https://github.com/RabaDaba1/lego-bot/actions/workflows/tests.yml/badge.svg)

Lego-Bot is a project mainly build for lego investors to help them make more accurate predictions. It uses Pandas, Beautiful Soup, and SQLite libraries. The program scrapes Lego set listings from a website (OLX.pl) and checks their prices or whether they have been sold every day. Once it has collected enough data about a particular set, it predicts its price so you can check if specific set is worth investing in. 

## Getting Started

To get started with Lego-Bot with all the dependencies, you just need to install it like a library:
```python
pip install .
```

## Usage

### Example of Lego Bot usage is in tutorial.ipynb

### Adding a new set to the database
Call `Set.add_set(set_id)`

### Deleting a set from the database
Call `Set.delete_set(set_id)`

### Getting all offers for a set and updating the database with them
1. Create a new `Set` object with the `set_id` of the set you want to get offers for
2. Wait for `Set` object to scrape data from offers
3. Call the `update_db()` method on the `Set` object
4. Done! The set is now in the database

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
