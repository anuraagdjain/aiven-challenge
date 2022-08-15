start-db:
	@docker run --rm -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=root postgres:14-alpine

run-migrations:
	@docker run --rm --platform linux/amd64 -v "/$$(pwd)/flyway/sql:/flyway/sql" -v "/$$(pwd)/flyway/conf:/flyway/conf" flyway/flyway:9.0-alpine -url="jdbc:postgresql://${DB_HOST}:${DB_PORT}/${DB_NAME}" -user=${DB_USER} -password=${DB_PASSWORD} migrate	

start-consumer:
	@python3 src/consumer/main.py

start-producer:
	@python3 src/producer/main.py		

run-tests:
	@python3 -m pytest tests/**/*.py

lint-fix:
	@python3 -m autopep8 --in-place --aggressive --aggressive src/**/**.py	