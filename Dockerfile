FROM python:3.11-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=__init__.py

ENV FLASK_APP=app:create_app

WORKDIR /app/customer-service

CMD ["flask", "run", "--host=0.0.0.0"]