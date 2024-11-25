import pytest
import requests
import socket


# Constants and configuration
TIMEOUT = 5000  # 5 seconds
DEFAULT_WAIT_TIME = 5  # 30 seconds for responses
# API base URL
BASE_URL = "http://127.0.0.1:1234"
DEFAULT_DB_CONF = 3
MAX_DB_CONF = 10


def read_get(get_id):
    count = 0
    print('Read entry...')
    if get_id == 'all':
        url = f"{BASE_URL}/configs"
    else:
        url = f"{BASE_URL}/configs/{get_id}"

    response = requests.get(url)

    if response.status_code == 200:
        print(f"Post Read successfully (status code): {response.status_code}")
        print(f"-> Response JSON: {response.json()}")
        json_obj = response.json()
        count = len(json_obj['data'])
    else:
        print(f"Failed to read post. Status code: {response.status_code}")
    return count


def clean_db_default():
    entries = read_get('all')
    print(f'DB entries: {entries}')
    while entries > DEFAULT_DB_CONF:
        url = f"{BASE_URL}/configs"
        response = requests.get(url)
        json_obj = response.json()

        print(f'->{json_obj['data'][-1]}')
        i = json_obj['data'][-1]
        url = f"{BASE_URL}/configs/{i['id']}"
        response = requests.delete(url)
        assert response.status_code == 200

        entries = read_get('all')


# Check that the binary server on port `1234` is up
def check_port_up(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    print(result)
    assert result == 0


@pytest.fixture
# Check that the binary server on port `1234` is up
def close_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    assert result == 0
    sock.close()


@pytest.hookimpl(tryfirst=True)
# Fixture for login, reusable across tests
def pytest_sessionstart():
    # Check that server is up at port 1234
    check_port_up(1234)
    # Start with 3 Satellite Configuration
    entries = read_get('all')
    assert entries == DEFAULT_DB_CONF, f"Expected {DEFAULT_DB_CONF}, but got {entries}"
    print(f'DB entries (default): {DEFAULT_DB_CONF}')


@pytest.hookimpl(trylast=True)
# Fixture for login, reusable across tests
def pytest_sessionfinish():
    # Cleanup test data in DB Satellite Configuration Service
    entries = read_get('all')
    print(f'DB entries (after test): {entries}')
    clean_db_default()
    entries = read_get('all')
    assert entries == DEFAULT_DB_CONF, f"Expected {DEFAULT_DB_CONF}, but got {entries}"
    print(f'DB entries (after cleanup): {entries}')
