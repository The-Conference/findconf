# conf-parsers

## Running:
[Not compatible with Windows](https://github.com/scrapy-plugins/scrapy-playwright#lack-of-native-support-for-windows), use WSL instead.

Run single spider: `scrapy crawl %spider_name%`\
Run all spiders: `python run.py`

### Data path:
    1. Sipder (scraping) -> ConferenceLoader
    2. ItemLoader (formatting, cleaning) -> ConferenceItem
    3. Pipelines (post processing) -> DB