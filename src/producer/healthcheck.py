import logging
import requests

class HealthCheck:
    def __init__(self,publisher, website_urls = []):
        self.website_urls = website_urls
        self.publisher = publisher
        self.topic =  "services-web-health"

    def run(self):
        for website_url in self.website_urls:
            logging.info('[HealthCheck.run] Checking page {}'.format(website_url))
            response = requests.get(website_url)
            payload = dict()
            payload["url"] = website_url
            payload["time_in_ms"] = response.elapsed.total_seconds() * 1000
            payload["http_status_code"] = response.status_code
            self.publish(payload)
    
    def publish(self, payload):
        logging.info("[HealthCheck.publish] Publishing payload for {}".format(payload["url"]))
        self.publisher.send(self.topic, payload)