# Emag-price-scraper

## Setup

Run:

```bash
pip install -r config/requirements.txt
```

Log into your mysql user and run:

```bash
source config/create_tables.sql
```

Replace the data in [database.example.ini](config/database.example.ini) with your own and rename the file to `database.ini`. Set your session key (random string) in [pages.example.ini](config/pages.example.ini) and rename the file to `pages.ini`.

Run the application with:

```bash
PYTHONPATH="src;." /path/to/python src/main.py
```
