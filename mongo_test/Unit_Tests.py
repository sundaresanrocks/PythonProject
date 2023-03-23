import unittest
import pytest
import logging
import requests
import json
import os
import inspect
from ddt import ddt, idata, data, unpack

LOG_LEVEL = logging.INFO #DEBUG, INFO, WARNING, ERROR, CRITICAL
common_formatter = logging.Formatter('%(asctime)s [%(levelname)-7s][ln-%(lineno)-3d]: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')

# root_path is parent folder of Scripts folder (one level up)
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def setup_logger(log_file, level=logging.INFO, name='', formatter=common_formatter):
    """Function setup as many loggers as you want."""
    handler = logging.FileHandler(log_file, mode='w')#default mode is append
    # Or use a rotating file handler
    # handler = RotatingFileHandler(log_file,maxBytes=1023, backupCount=5)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# default debug logger
debug_log_filename = root_path + os.sep + 'Logs' + os.sep + 'debug.log'
log = setup_logger(debug_log_filename, LOG_LEVEL,'log')


api_formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
api_outputs_filename = root_path + os.sep + 'Logs' + os.sep + 'api_outputs.log'
log_api = setup_logger(api_outputs_filename, LOG_LEVEL,'log_api',formatter = api_formatter)


def pretty_print_request(request):
    """
    Pay attention at the formatting used in this function because it is programmed to be pretty printed and may differ from the actual request.
    """
    log_api.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body)
        )

# pretty print Restful response to API log
# argument is response object
def pretty_print_response(response):
    log_api.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '<-----------Response-----------',
        'Status code:' + str(response.status_code),
        '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
        response.text
        ))

# argument is response object
# display body in json format explicitly with expected indent. Actually most of the time it is not very necessary because body is formatted in pretty print way.
def pretty_print_response_json(response):
    """ pretty print response in json format.
        If failing to parse body in json format, print in text.
    """
    try:
        resp_data = response.json()
        resp_body = json.dumps(resp_data,indent=3)
    # if .json() fails, ValueError is raised.
    except ValueError:
        resp_body = response.text
    log_api.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '<-----------Response-----------',
        'Status code:' + str(response.status_code),
        '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
        resp_body
        ))

@ddt
class MyTestCase(unittest.TestCase):
    """
    Test Restful HTTP API examples.
    """
    def get(self, url, auth=None, params=None, verify=False):
        """
        common request get function with below features, which you only need to take care of url:
            - print request and response in API log file
            - Take care of request exception and non-200 response codes and return None, so you only need to care normal json response.
            - arguments are the same as requests.get

        verify: False - Disable SSL certificate verification
        """
        try:
            if auth == None:
                if params is not None:
                    resp = requests.get(url, params=params, verify=verify)
                else:
                    resp = requests.get(url, verify=verify)
            else:
                resp = requests.get(url, auth=auth, verify=verify)
                if params is not None:
                    resp = requests.get(url, auth=auth, verify=verify)
                else:
                    resp = requests.get(url, auth=auth, params=params, verify=verify)
        except Exception as ex:
            log.error('requests.get() failed with exception:', str(ex))
            return None

        # pretty request and response into API log file
        pretty_print_request(resp.request)
        pretty_print_response_json(resp)

        # This return caller function's name, not this function post.
        caller_func_name = inspect.stack()[1][3]
        if resp.status_code != 200:
            log.error('%s failed with response code %s.' % (caller_func_name, resp.status_code))
        return resp.status_code, resp.json()

    def post(self, url, data, headers={}, verify=False, amend_headers=False):
        """
        common request post function with below features, which you only need to take care of url and body tests:
            - append common headers
            - print request and response in API log file
            - Take care of request exception and non-200 response codes and return None, so you only need to care normal json response.
            - arguments are the same as requests.post, except amend_headers.

        verify: False - Disable SSL certificate verification
        """

        # append common headers if none
        headers_new = headers
        if amend_headers == True:
            if 'Content-Type' not in headers_new:
                headers_new['Content-Type'] = r'application/json'
            if 'User-Agent' not in headers_new:
                headers_new['User-Agent'] = 'Python Requests'

        # send post request
        print(url)
        print(data)
        resp = requests.post(url, data=data, headers=headers_new, verify=verify)

        # pretty request and response into API log file
        # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging.
        pretty_print_request(resp.request)
        pretty_print_response_json(resp)

        # This return caller function's name, not this function post.
        caller_func_name = inspect.stack()[1][3]
        if resp.status_code != 200:
            print("Test")
            log.error('%s failed with response code %s.' % (caller_func_name, resp.status_code))

        return resp.status_code, resp.json()

    @classmethod
    def setUpClass(self):
        #log.debug('To load tests tests.')
        # post with headers, json body
        self.host = 'http://httpbin.org'
        self.username = 'user1'
        self.password = 'password'
        self.host1 = 'https://reqres.in'

    def Setup(self):
        pass

    def tearDown(self):
        pass

    # def test_get_list_users(self):
    #     # InsecureRequestWarning: Unverified HTTPS request is being made.
    #     # Adding certificate verification is strongly advised.
    #     # See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning)
    #     # Note : This is taken care by  verify=True parameter from in the get request
    #
    #     # Query parameter/string
    #     parameters = {'page': 2}
    #
    #     # Form Get Request
    #     url = f'{self.host1}/api/users'
    #
    #     # Send GET request
    #     status_code, response = self.get(url, params=parameters, verify=True)
    #     print(status_code)
    #     print(response)
    #
    #     # Assert response status code & response
    #     self.assertIsNotNone(response['tests'])
    #     self.assertEqual(status_code, 200)
    #     log.info('Test %s passed.' % inspect.stack()[-1][3])
    #
    # def test_get_single_used_by_id(self):
    #     # InsecureRequestWarning: Unverified HTTPS request is being made.
    #     # Adding certificate verification is strongly advised.
    #     # See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning)
    #     # Note : This is taken care by  verify=True parameter from in the get request
    #
    #     # Query parameter/string
    #     user_id = 2
    #     parameters = {'id': user_id}
    #
    #     # Form Get Request
    #     url = f'{self.host1}/api/users'
    #
    #     # Send GET request
    #     status_code, response = self.get(url, params=parameters, verify=True)
    #     print(status_code)
    #     print(response)
    #
    #     # Assert response status code & response
    #     print(response['tests'])
    #     self.assertEqual(response['tests']['id'], user_id)
    #     self.assertEqual(status_code, 200)
    #     log.info('Test %s passed.' % inspect.stack()[-1][3])
    #
    # def test_get_single_used_by_id_not_valid(self):
    #     # InsecureRequestWarning: Unverified HTTPS request is being made.
    #     # Adding certificate verification is strongly advised.
    #     # See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning)
    #     # Note : This is taken care by  verify=True parameter from in the get request
    #
    #     # Query parameter/string
    #     user_id = 23
    #     parameters = {'id': user_id}
    #
    #     # Form Get Request
    #     url = f'{self.host1}/api/users'
    #
    #     # Send GET request
    #     status_code, response = self.get(url, params=parameters, verify=True)
    #     print(status_code)
    #     print(response)
    #
    #     # Assert response status code & response
    #     self.assertEqual({}, {})
    #     self.assertEqual(status_code, 404)
    #     log.info('Test %s passed.' % inspect.stack()[-1][3])
    #
    # def test_post_successful_registration(self):
    #     payload_successful_registration = {"email": "eve.holt@reqres.in", "password": "pistol"}
    #
    #     # convert dict to json by json.dumps() for body tests.
    #     # It is risky to use str(payload) to convert because json format must use double quotes ("")
    #     url = self.host1 + '/api/register'
    #     status_code, response = self.post(url, data=payload_successful_registration, verify=True)
    #     print(status_code)
    #     print(response)
    #     # post with normal tests
    #
    #     # Assert response status code & response
    #     self.assertIn("id" ,response)
    #     self.assertIn("token", response)
    #     self.assertEqual(status_code, 200)
    #     log.info('Test %s passed.' % inspect.stack()[-1][3])
    #
    # def test_post_unsuccessful_registration(self):
    #     # Negative tests scenario, payload missing Password parameter
    #     payload_unsuccessful = {"email": "eve.holt@reqres.in"}
    #     # convert dict to json by json.dumps() for body tests.
    #     # It is risky to use str(payload) to convert because json format must use double quotes ("")
    #     url = self.host1 + '/api/register'
    #     status_code, response = self.post(url, data=json.dumps(payload_unsuccessful, indent=4), verify=True)
    #     print(status_code)
    #     print(response)
    #
    #     # Assert response status code & response
    #     self.assertEqual({'error': 'Missing email or username'},response)
    #     self.assertEqual(status_code, 400)
    #     log.info('Test %s passed.' % inspect.stack()[-1][3])

    @data(("eve.holt@reqres.in",         'pistol'),
          ("michael.lawson@reqres.in",   'password'),
          ("lindsay.ferguson@reqres.in", 'tests'),
          ("tobias.funke@reqres.in",     'tests'),
          ("invalid_email@request.in",     'tests'))
    @unpack
    def test_multiple_user_login(self, email, password):
        payload_successful_registration = {"email": email, "password": password}

        # convert dict to json by json.dumps() for body tests.
        # It is risky to use str(payload) to convert because json format must use double quotes ("")
        url = self.host1 + '/api/register'
        status_code, response = self.post(url, data=payload_successful_registration, verify=True)
        print(status_code)
        print(response)
        # post with normal tests

        # Assert response status code & response
        self.assertIn("id", response)
        self.assertIn("token", response)
        self.assertEqual(status_code, 200)
        log.info('Test %s passed.' % inspect.stack()[-1][3])

    # @pytest.mark.skip
    # def test_get_auth_http(self):
    #     log.info('Calling %s.' % inspect.stack()[0][3])
    #     # Get URL form
    #     url = self.host + f'/basic-auth/{self.username}/{self.password}'
    #
    #     # Send Request
    #     status_code, response = self.get(url, auth=(self.username, self.password))
    #
    #     # Assert for status response code and response body
    #     """ Expected json response
    #     {
    #     "authenticated": true,
    #     "user": "user1"
    #     }
    #     """
    #     self.assertIsNotNone(response)
    #     self.assertEqual(status_code, 200)
    #     self.assertTrue(response["authenticated"])
    #     log.info('Test %s passed.' % inspect.stack()[-1][3])
    #
    # @pytest.mark.skip
    # def test_post_headers_body_json(self):
    #     # Payload
    #     payload = {'key1': 1, 'key2': 'value2'}
    #     # No need to specify common headers as it is taken cared of by common self.post() function.
    #     # headers = {'Content-Type': 'application/json' }
    #
    #     # convert dict to json by json.dumps() for body tests.
    #     # It is risky to use str(payload) to convert because json format must use double quotes ("")
    #     url = self.host + '/post'
    #     resp = self.post(url, data=json.dumps(payload, indent=4))
    #     print(resp)
    #     '''
    #     log.info('Test %s passed.' % inspect.stack()[0][3])
    #     """ Request HTTP body:
    #     {   "key1": 1,
    #         "key2": "value2"
    #     }
    #     """
    #     '''
    #     # post with normal tests
    #
    # @pytest.mark.xfail
    # def test_post_normal_body(self):
    #     # Payload tests
    #     payload = {'key1': 1, 'key2': 'value2'}
    #
    #     # Url method
    #     url = 'http://httpbin.org/post'
    #
    #     # Send Request
    #     resp = self.post(url, data=payload, amend_headers=False)
    #     assert resp != None
    #     log.info('Test %s passed.' % inspect.stack()[0][3])
    #     """ Request HTTP body:
    #     key1=1&key2=value2
    #     """
    #
    #
    #
    # @pytest.mark.parametrize("a,b,c", [(1, 1, 2), (2, 2, 4), (3, 3, 6)])
    # def test_parametrization(self, a, b, c):
    #     assert a + b == c
    #
    # def tearDown(self):
    #     pass

if __name__ == '__main__':
    unittest.main()
