from datetime import datetime
import pytest
from src.consumer.handler import MessageHandler
from unittest.mock import MagicMock
from cloudevents.http import CloudEvent, to_json

@pytest.fixture
def mock_db():
    return MagicMock()

class TestMessageHandler:

    @pytest.mark.usefixtures("mock_db")
    def test_creates_payload_to_persists_in_database(self, mock_db):
        data = {
            "url":"https://aiven.io",
            "time_in_ms": 129.92,
            "http_status_code": 200
        }
        event = CloudEvent({
            "type": "com.localhost.healthcheck",
            "source":"healthchecker"
        }, data)

        handler = MessageHandler(mock_db)
        handler.handle(to_json(event))
        
        db_call_arg = mock_db.save_live_web_health.call_args_list[0].args[0]

        assert mock_db.save_live_web_health.called
        assert mock_db.save_live_web_health.call_count == 1

        assert list(db_call_arg.keys()) == ["web_url","response_time","http_status_code","last_checked_at"]

        assert db_call_arg["web_url"] == data["url"]
        assert db_call_arg["response_time"] == data["time_in_ms"]
        assert db_call_arg["http_status_code"] == data["http_status_code"]
        assert isinstance(db_call_arg["last_checked_at"], str)