FROM python:3.11-alpine
  ENV PYTHONDONTWRITEBYTECODE 1
  ENV PYTHONUNBUFFERED 1
  RUN apk update && apk add bash
  RUN mkdir /app /start
  WORKDIR /app
  RUN pip install --upgrade pip
  COPY ./app/requirements.txt ./
  RUN pip install -r requirements.txt
  COPY ./app /app
  COPY ./run.sh /start/
  RUN chmod +x /start/*