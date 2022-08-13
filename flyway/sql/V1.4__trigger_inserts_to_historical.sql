CREATE OR REPLACE FUNCTION insert_to_historical()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	 INSERT INTO web_health.historical SELECT NEW.*;
	RETURN NEW;
END;
$$;

CREATE TRIGGER historical_insert_trigger
  AFTER INSERT
  ON web_health.live
  FOR EACH ROW
  EXECUTE PROCEDURE insert_to_historical();
