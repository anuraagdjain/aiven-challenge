# Aiven Challenge

## Kafka

1. Create the Kafka service on aiven and download the certs (service.cert, service.key, ca.pem)
2. Copy the downloaded files into `src/certs` folder

## Run DB Migrations

1. Start the Aiven Postgres service or Postgres DB server on your local
2. Run `make run-migrations DB_HOST=<host> DB_PORT=<port> DB_NAME=<db_name> DB_USER=<user> DB_PASSWORD=<password>`

## Run tests

1. `python3 -m pytest tests/**/*.py`
