import pytest
import coloredlogs
import logging
import requests
import socket


# Constants and configuration
TIMEOUT = 5000  # 5 seconds
DEFAULT_WAIT_TIME = 5  # 30 seconds for responses

# API base URL
BASE_URL = "http://127.0.0.1:1234"
DEFAULT_DB_CONF = 3
MAX_DB_CONF = 10

# logging object
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def configure_colored_logging():
    coloredlogs.install(
        level='DEBUG',
        fmt='%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)s)',
        level_styles={
            'debug': {'color': 'cyan'},
            'info': {'color': 'green'},
            'warning': {'color': 'yellow'},
            'error': {'color': 'red'},
            'critical': {'color': 'magenta'},
        }
    )


def read_get(get_id):
    count = 0
    logger.info('Read entry...')
    if get_id == 'all':
        url = f"{BASE_URL}/configs"
    else:
        url = f"{BASE_URL}/configs/{get_id}"

    response = requests.get(url)

    if response.status_code == 200:
        logger.info(f"Post Read successfully (status code): {response.status_code}")
        logger.info(f"-> Response JSON: {response.json()}")
        json_obj = response.json()
        count = len(json_obj['data'])
    else:
        logger.error(f"Failed to read post. Status code: {response.status_code}")
    return count


def clean_db_default():
    entries = read_get('all')
    logger.info(f'DB entries: {entries}')
    while entries > DEFAULT_DB_CONF:
        url = f"{BASE_URL}/configs"
        response = requests.get(url)
        json_obj = response.json()

        logger.info(f'->{json_obj['data'][-1]}')
        i = json_obj['data'][-1]
        url = f"{BASE_URL}/configs/{i['id']}"
        response = requests.delete(url)
        assert response.status_code == 200

        entries = read_get('all')


# Check that the binary server on port `1234` is up
def check_port_up(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    logger.debug(result)
    assert result == 0, f'Server should listen on port {port}, but not found'


# Assert function for checking expected status code and possible message with the received once.
def assert_response(response, message, expected_code):
    json_response = response.json()
    # Received status code except of 200 OK
    if response.status_code != 200:
        logger.info(json_response['errors'][0]['message'])
    else:
        # Received any other status code check if message should be printed
        if message != '':
            logger.debug(json_response['data']['message'])
    assert response.status_code == expected_code, (f"Expected {expected_code}, but got {response.status_code} " 
                                                   f"with {json_response['errors'][0]['message']}")


@pytest.hookimpl(tryfirst=True)
# Fixture for login, reusable across tests
def pytest_sessionstart():
    # Start with 3 Satellite Configuration
    entries = read_get('all')
    assert entries == DEFAULT_DB_CONF, f"Expected {DEFAULT_DB_CONF}, but got {entries}"
    logger.info(f'DB entries (default): {DEFAULT_DB_CONF}')


@pytest.hookimpl(trylast=True)
# Fixture for login, reusable across tests
def pytest_sessionfinish():
    # Cleanup test data in DB Satellite Configuration Service
    entries = read_get('all')
    logger.info(f'DB entries (after test): {entries}')
    clean_db_default()
    entries = read_get('all')
    assert entries == DEFAULT_DB_CONF, f"Expected {DEFAULT_DB_CONF}, but got {entries}"
    logger.info(f'DB entries (after cleanup): {entries}')
