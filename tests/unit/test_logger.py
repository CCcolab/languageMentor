import pytest
from src.utils.logger import LOG

class TestLogger:
    def test_logger_info(self, caplog):
        test_message = "Test log message"
        LOG.info(test_message)
        assert test_message in caplog.text 