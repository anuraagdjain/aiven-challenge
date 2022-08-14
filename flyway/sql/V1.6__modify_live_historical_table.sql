ALTER TABLE web_health.live ALTER COLUMN response_time TYPE NUMERIC(6,2);

ALTER TABLE web_health.historical ALTER COLUMN response_time TYPE NUMERIC(6,2);