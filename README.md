# Lego-Bot

Lego-Bot is a Python project that uses Pandas, Beautiful Soup, and SQLite libraries. It is mainly build for lego investors to help them make more accurate predictions. The program scrapes Lego set listings from a website and checks their prices or whether they have been sold every day. Once it has collected enough data about a particular set, it predicts its price. 

## Getting Started

To get started with Lego-Bot, you will need to install Python 3 and the following libraries:

- Pandas
- Beautiful Soup

You can install these libraries using pip:
```python
pip install pandas bs4
```

## Usage

### Adding a new set to the database
Call `Set.add_set(set_id)` in `main.ipynb`

### Deleting a set from the database
Call `Set.delete_set(set_id)` in `main.ipynb`

### Getting all offers for a set and updating the database with them
1. Create a new `Set` object with the `set_id` of the set you want to get offers for
2. Call the `update_db()` method on the `Set` object
3. Done! The set is now in the database

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
