FROM python:latest
  ENV PYTHONDONTWRITEBYTECODE 1
  ENV PYTHONUNBUFFERED 1
  RUN mkdir /app
  WORKDIR /app
  RUN pip install --upgrade pip
  COPY package.txt .
  RUN pip install -r package.txt
  COPY ./app /app