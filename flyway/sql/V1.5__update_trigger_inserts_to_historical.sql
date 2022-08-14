CREATE TRIGGER on_update_insert_to_historical_trigger
  AFTER UPDATE
  ON web_health.live
  FOR EACH ROW
  EXECUTE PROCEDURE insert_to_historical();
