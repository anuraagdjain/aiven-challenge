CREATE TABLE IF NOT EXISTS web_health.historical (
	web_url text NOT NULL,
	response_time INTEGER NOT NULL,
	status_code SMALLINT NOT NULL, 
	last_checked_at TIMESTAMP NOT NULL
);

