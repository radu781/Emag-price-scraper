# Emag-price-scraper

## About

Web application created using Python and the Flask library in order to scrape data on a Romanian shopping website, [emag](https://www.emag.ro/). Scraped data include: product name, image, price, link. A user is able to track certain items, see the price changes over time and be notified via email when their price changes.

## Api reference

| Type  |  Endpoint   | Mandatory arguments |                                                                                Optional arguments                                                                                 |
| :---: | :---------: | :-----------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|  GET  | /api/search |      q: query       | search-count: limit results to this value<br>price-min: minimum price for products<br>price-max: maximum price for products<br>refresh-items[*](#notes): scrape and insert into database |

### Notes

- refresh-items: can only be applied if the user has the permission to refresh the searches (flag 1 in database)

## Setup

Run:

```bash
pip install -r config/requirements.txt
```

Log into your mysql user and run:

```bash
source config/create_tables.sql
```

Replace the data in [data.example.ini](config/data.example.ini) with your own and rename the file to `data.ini`:

- database host, schema, username, password (port should be 3306 for mysql)
- session key for flask pages
- email details for sending emails (leave empty to disable this feature)

Run the application with:

- command line

```bash
PYTHONPATH="src;." /path/to/python src/main.py
```

- or use the Visual Studio Code configuration
