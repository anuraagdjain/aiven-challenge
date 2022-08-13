import requests

class HealthCheck:
    def __init__(self, website_urls = []):
        self.website_urls = website_urls
    def run(self):
        result = []
        for website_url in self.website_urls:
            response = requests.get(website_url)
            payload = dict()
            payload["url"] = website_url
            payload["time_in_ms"] = response.elapsed.total_seconds() * 1000
            payload["http_status_code"] = response.status_code
            result.append(payload)
        return result