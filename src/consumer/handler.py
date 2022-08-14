import logging
from cloudevents.http import  from_json

class MessageHandler:
    def __init__(self, db):
        self.db = db
    
    def handle(self, message):
        payload = from_json(message)
        
        logging.info('[MessageHandler.handle] - Incoming message - url: {}'.format(payload.data["url"]))
        
        db_data = dict()
        db_data["web_url"] = payload.data["url"]
        db_data["response_time"] = payload.data["time_in_ms"]
        db_data["http_status_code"] = payload.data["http_status_code"]
        db_data["last_checked_at"] = payload["time"]
        
        self.db.save_live_web_health(db_data)