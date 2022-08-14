import responses
import pytest
from unittest.mock import MagicMock, patch
from src.producer.healthcheck import HealthCheck


@pytest.fixture
@patch('kafka.KafkaProducer', MagicMock())
@patch('src.producer.publisher.MessagePublisher')
def message_publisher(messagePublisher):
    return messagePublisher

@pytest.fixture
@pytest.mark.usefixtures("message_publisher")
def healthcheck_instance(message_publisher):
    website_urls = ["https://google.com","https://aiven.io"]
    return HealthCheck(message_publisher, website_urls)

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
@pytest.mark.usefixtures("message_publisher")
class TestHealthCheck:
    @responses.activate
    def test_publishes_on_broker(self, healthcheck_instance, message_publisher):
        healthcheck_instance.run()
        
        assert message_publisher.send.called
        assert message_publisher.send.call_count == 2


    @responses.activate
    def test_payload_has_expected_data(self, healthcheck_instance, message_publisher):
        responses.add(responses.Response(
        method="GET",
        url="https://google.com",
        status=404
        ))

        responses.add(responses.Response(
        method="GET",
        url="https://aiven.io",
        status=502))

        healthcheck_instance.run()

        call_args = message_publisher.send.call_args_list

        first_call = call_args[0].args
        second_call = call_args[1].args
        
        assert first_call[0] == 'services-web-health'
        assert first_call[1]["url"] == "https://google.com"
        assert first_call[1]["http_status_code"] == 404
        
        assert second_call[0] == 'services-web-health'
        assert second_call[1]["url"] == "https://aiven.io"
        assert second_call[1]["http_status_code"] == 502

