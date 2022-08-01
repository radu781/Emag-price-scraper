# Emag-price-scraper

## About

Web application created using Python and the Flask library in order to scrape data on a Romanian shopping website, [emag](https://www.emag.ro/). Scraped data include: product name, image, price, link. A user is able to track certain items, see the price changes over time and be notified via email when their price changes.

## Api reference

| Type  |   Endpoint    |                   Usage                    |                              Mandatory arguments                               |                                                     Optional arguments                                                      |
| :---: | :-----------: | :----------------------------------------: | :----------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: |
|  GET  |  /api/search  |       search the supported websites        |                                    q: query                                    | search-count: limit results to this value<br>price-min: minimum price for products<br>price-max: maximum price for products |
| POST  |  /api/track   | track or untrack price progress on an item | set: itemId to set tracking for<br>*or*<br>unset: itemId to unset tracking for |                                                              -                                                              |
| POST  |  /api/login   |             login into a user              |                           user-name<br>user-password                           |                                                              -                                                              |
| POST  | /api/register |            register a new user             |              user-name<br>user-password<br>user-password-confirm               |                                                              -                                                              |
| POST  |  /api/logout  |         logout of the current user         |                                       -                                        |                                                              -                                                              |
|  GET  |   /api/mine   |     get the current user's item tracks     |                                       -                                        |                                                              -                                                              |
|  GET  |   /api/item   |   get statistics about an item's prices    |                          id: item to see details for                           |                                                              -                                                              |

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
