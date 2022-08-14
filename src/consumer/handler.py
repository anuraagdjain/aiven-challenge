import logging
from cloudevents.http import  from_json, CloudEvent

class MessageHandler:
    def __init__(self, db):
        self.db = db

    def is_valid(self, payload: CloudEvent) -> bool:
        if not (["url","time_in_ms","http_status_code"] == list(payload.data.keys())):
            logging.debug('[MessageHandler.is_valid] Received data is invalid - {}'.format(payload.data.keys()))
            return False
       
        if not ("time" in payload):
            logging.debug('[MessageHandler.is_valid] Missing time in cloudevents obj - {}'.format(payload))
            return False
       
        if not (
                isinstance(payload.data["url"], str) 
                and isinstance(payload.data["time_in_ms"], (int, float))
                and isinstance(payload.data["http_status_code"], int)
                and isinstance(payload["time"], str)
            ):
            logging.debug('[MessageHandler.is_valid] Received message is invalid - {}'.format(payload))
            return False
        
        logging.debug('[MessageHandler.is_valid] validation successful')
        
        return True
    
    def handle(self, message):
        payload = from_json(message)

        if not self.is_valid(payload):
            raise ValueError("Received payload is invalid", message)
        
        logging.info('[MessageHandler.handle] - Incoming message - url: {}'.format(payload.data["url"]))
        
        db_data = dict()
        db_data["web_url"] = payload.data["url"]
        db_data["response_time"] = payload.data["time_in_ms"]
        db_data["http_status_code"] = payload.data["http_status_code"]
        db_data["last_checked_at"] = payload["time"]
        
        self.db.save_live_web_health(db_data)