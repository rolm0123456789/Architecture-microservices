# FROM python:3.11-slim-buster

# WORKDIR /app

# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 5000

# ENV FLASK_APP=__init__.py

# ENV FLASK_APP=app:create_app

# WORKDIR /app/customer-service

# CMD ["flask", "run", "--host=0.0.0.0"]
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY . .

# Ensure entrypoint.sh uses Unix line endings and has execute permissions
RUN apt-get update && apt-get install -y dos2unix \
    && dos2unix ./entrypoint.sh \
    && pip install --no-cache-dir -r ./customer-service/requirements.txt \
    && chmod +x ./entrypoint.sh \
    && apt-get remove -y dos2unix && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["./entrypoint.sh"]
