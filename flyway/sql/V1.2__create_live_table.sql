CREATE TABLE IF NOT EXISTS web_health.live (
	web_url text PRIMARY KEY,
	response_time INTEGER NOT NULL,
	status_code SMALLINT NOT NULL, 
	last_checked_at TIMESTAMP NOT NULL
);

