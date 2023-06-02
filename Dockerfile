FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
RUN playwright install webkit --with-deps
COPY scrapy.cfg run.py ./
COPY conf_parsers/ ./conf_parsers/
CMD ["/bin/sh"]