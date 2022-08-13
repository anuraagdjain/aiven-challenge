from src.producer.healthcheck import HealthCheck
import responses
import pytest

@pytest.fixture
def healthcheck_instance():
    website_urls = ["https://google.com","https://aiven.io"]
    return HealthCheck(website_urls)

@pytest.fixture
def setup_mock_response():
    responses.add(responses.Response(
        method="GET",
        url="https://google.com",
        status=404
        ))

    responses.add(responses.Response(
        method="GET",
        url="https://aiven.io",
        status=502))
    

@pytest.mark.usefixtures("healthcheck_instance")
@pytest.mark.usefixtures("setup_mock_response")
class TestHealthCheck:
    @responses.activate
    def test_run_returns_payload_in_expected_format(self, healthcheck_instance):
        

        result = healthcheck_instance.run()
        
        assert isinstance(result, list)
        for data in result:
            assert ["url","time_in_ms","http_status_code"] == list(data.keys())
            assert isinstance(data["url"], str)
            assert isinstance(data["http_status_code"], int)
            assert isinstance(data["time_in_ms"], float)


    @responses.activate
    def test_payload_has_expected_data(self, healthcheck_instance):
        responses.add(responses.Response(
        method="GET",
        url="https://google.com",
        status=404
        ))

        responses.add(responses.Response(
        method="GET",
        url="https://aiven.io",
        status=502))

        result = healthcheck_instance.run()
        
        assert result[0]["url"] == "https://google.com"
        assert result[0]["http_status_code"] == 404
        assert result[1]["url"] == "https://aiven.io"
        assert result[1]["http_status_code"] == 502

