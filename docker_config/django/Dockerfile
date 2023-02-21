FROM python:3.10-buster
  ENV PYTHONDONTWRITEBYTECODE 1
  ENV PYTHONUNBUFFERED 1
  RUN mkdir /app
  WORKDIR /app
  RUN pip install --upgrade pip
  COPY ./app/requirements.txt .
  RUN pip install -r requirements.txt
  COPY ./app /app