# conf-parsers
* CRUD operations use PostgreSQL dialect (specifically, ON CONFLICT DO NOTHING).

## Running:
[Not compatible with Windows](https://github.com/scrapy-plugins/scrapy-playwright#lack-of-native-support-for-windows), use WSL instead.

Run single spider: `scrapy crawl %spider_name%`

Run all spiders: `python run.py`

## Development:
Install: `pip install pip-tools && pip-sync requirements-dev.txt`

Enable dev db: `export DB_URL="sqlite:///my_db.sqlite3"`

Tests: `python -m unittest discover`

Coverage: `coverage run -m unittest discover && coverage report`

Build docs: `pdoc conf_parsers !conf_parsers.spiders !conf_parsers.tests --docformat google -o ./docs`

### Data flow:
    1. Sipder (scraping) -> items.ConferenceLoader
    2. ItemLoader (formatting, cleaning) -> items.ConferenceItem
    3. Pipelines (post processing) -> models.ConferenceItemDB
    4. Model(applying default values) -> DB