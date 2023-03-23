import json
import pytest

filename = '/home/svenkatesan/pythonProject/tests/data/testdata.json'

import logging

LOGGER = logging.getLogger(__name__)



@pytest.fixture
def json_config(request):
    with open('/home/svenkatesan/pythonProject/tests/data/testdata.json') as json_data:
        data = json.load(json_data)
        return data

@pytest.mark.skip
def test_config_has_foo_set_to_bar(caplog, json_config):
    caplog.set_level(logging.INFO)
    logging.getLogger().info("####### json_config {}".format(json_config))
    assert json_config['foo'] == 'bar'



import pytest
import logging

test_prevelence = logging.getLogger('test_prevelence')
test_publish = logging.getLogger('test_publish')

@pytest.mark.skip
@pytest.fixture(scope='session')
def session_thing():
    test_prevelence.debug('constructing session thing')
    yield
    test_prevelence.debug('destroying session thing')

@pytest.mark.skip
@pytest.fixture
def testcase_thing():
    test_prevelence.debug('constructing testcase thing')
    yield
    test_prevelence.debug('destroying testcase thing')

@pytest.mark.skip
def test_one(session_thing, testcase_thing):
    test_prevelence.info('one executes')
    test_prevelence.warning('this test does nothing aside from logging')
    test_prevelence.info('extra log, rarely read')

@pytest.mark.skip
def test_two(session_thing, testcase_thing):
    test_publish.info('two executes')
    test_publish.warning('neither does this')
    test_publish.info('extra log, not enabled by default')

