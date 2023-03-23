import pytest
import os
import pymongo

@pytest.fixture
def input_total():
    print("Setup input_total")
    yield
    print("Cleanup input_total")


@pytest.fixture
def intpt_test():
    number = 200
    return number


def pytest_logger_config(logger_config):
    logger_config.add_loggers(['test_prevelence', 'test_publish'], stdout_level='info')
    logger_config.set_log_option_default('test_prevelence,test_publish')

def pytest_logger_logdirlink(config):
    return os.path.join(os.path.dirname(__file__), 'mylogs')


