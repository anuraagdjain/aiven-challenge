# Aiven Challenge

The project is written in python. There is a health-checker which makes requests to the provided websites and publishes the status_code, response_time onto the message broker on a specific topic, in this case it's Kafka. The consumer listens onto the same topic. It validates the message it has received and saves that information into a live table in the database.

The database consists of `live` and `historical` table. As the name suggests, the `live` table has the most recent information of the website. There are two triggers on `live` table which on INSERT / UPDATE actions will insert the information into `historical` table. The historical information can be useful to understand at what times in the past the website was not reacheable or had a status code other than 200. It can also be used to understand if there was a significant delay in response from the server.

Below image explains the thought process behind the development of the codebase.

![AnuraagJain-Aiven-Challenge](https://i.imgur.com/IAJmHAD.png)

## Pre-requisites

1. [Pipenv](https://pipenv.pypa.io/en/latest/)
2. Python3
3. Postgres server
4. Kafka service
5. Docker (For flyway migrations)

## How to run

1. First create the `.env` file with the contents from `.env.test` . Replace them with actual values.
2. Activate the shell using `pipenv shell`.
3. Install the necessary dependencies `pipenv install`.
4. Run the database migrations `make run-migrations DB_HOST=<host> DB_PORT=<port> DB_NAME=<db_name> DB_USER=<user> DB_PASSWORD=<password>`. You can either use Aiven's Postgres or your local postgres server.
5. Start the consumer - `make start-consumer`.
6. Start the producer - `make start-producer`.

## Kafka

1. Create the Kafka service on aiven.io and download the certs (service.cert, service.key, ca.pem)
2. Copy the downloaded files into `src/certs` folder

## Run tests

1.  `python3 -m pytest tests/**/*.py`

## References

- https://www.psycopg.org/docs/usage.html

- https://github.com/cloudevents/sdk-python

- https://aiven.io/blog/teach-yourself-apache-kafka-and-python-with-a-jupyter-notebook

- https://docs.python.org/3/library/threading.html

- https://github.com/getsentry/responses

- https://www.postgresql.org/docs/current/plpgsql-trigger.html

- https://flywaydb.org/documentation/configuration/configfile.html
