import json
import pytest
import requests

# Constants and configuration
TIMEOUT = 5000  # 5 seconds
DEFAULT_WAIT_TIME = 5  # 5 seconds for responses

# API base URL
BASE_URL = "http://127.0.0.1:1234"
DEFAULT_DB_CONF = 3
MAX_CONF = 10


# Read DB entry with given id (which is unique).
# Read all the entries with 'all' instead of number for get_id.
def read_db(get_id):
    count = 0
    print('\nRead entry...')
    if get_id == 'all':
        url = f"{BASE_URL}/configs"
    else:
        url = f"{BASE_URL}/configs/{get_id}"

    response = requests.get(url)

    if response.status_code == 200:
        print(f"Post Read successfully (status code): {response.status_code}")
        json_response = response.json()
        print(f"-> Response JSON: {json.dumps(json_response, indent=4)}")
        count = len(json_response['data'])
    else:
        print(f"Failed to read post. Status code: {response.status_code}")
    return count


# Delete the last entry of the DB.
def clean_db():
    entries = read_db('all')
    print(f'->DB has {entries} Satellite Configuration right now.')
    if entries > DEFAULT_DB_CONF:
        url = f"{BASE_URL}/configs"
        response = requests.get(url)
        json_obj = response.json()

        print(f'clean_db->{json_obj['data'][-1]}')
        i = json_obj['data'][-1]
        url = f"{BASE_URL}/configs/{i['id']}"
        response = requests.delete(url)
        assert response.status_code == 200


# Assert function for checking expected status code and possible message with the received once.
def assert_response(response, message, expected_code):
    json_response = response.json()
    if response.status_code != 200:
        print(json_response['errors'][0]['message'])
    else:
        if message != '':
            print(json_response['data']['message'])
    assert response.status_code == expected_code, (f"Expected {expected_code}, but got {response.status_code} " 
                                                   f"with {json_response['errors'][0]['message']}")


@pytest.mark.parametrize("data, conf_id, message, crud_op, status_code", [
    ({"name": "MySat1", "type": "SAR", "cospar_id": "2020-199CD"}, 0,
     'Mission config created successfully', 'create', 200),
    ({}, 1, '', 'read', 200),
    ({"name": "MySat2", "type": "TELECOM", "cospar_id": "2020-195CD"}, 4,
     'Mission config updated successfully', 'update', 200),
    ({}, 4, 'Mission config deleted successfully', 'delete', 200),
])
@pytest.mark.basic_crud_ops
# This test scenario verifies the basic crud operations with valid values in the configuration fields with
# correct message and statuscode.
def test_basic_crud_ops(data: dict, conf_id: int, crud_op: str, message: str, status_code: int):
    url = f"{BASE_URL}/configs/{conf_id}"

    if crud_op == 'create':
        url = f"{BASE_URL}/configs"
        response = requests.post(url, json=data)
    elif crud_op == 'read':
        response = requests.get(url)
    elif crud_op == 'update':
        response = requests.put(url, json=data)
    else:
        response = requests.delete(url)

    assert_response(response, message, status_code)


@pytest.mark.parametrize("crud_op, conf_id, data, status_code, message", [
    ('post', 0, {"name": "MySat1", "type": "SAR", "cospar_id": "2020-199CD"}, 200, ''),
    ('post', 0, {"name": "MySat2", "type": "OPTICAL", "cospar_id": "2020-198CD"}, 200, ''),
    ('post', 0, {"name": "MySat3", "type": "TELECOM", "cospar_id": "2020-195CD"}, 200, ''),
    ('put', 1, {"name": "MySat", "type": "OPTICAL", "cospar_id": "2020-199CD"}, 200, ''),
    ('put', 2, {"name": "MySatUPD", "type": "OPTICAL", "cospar_id": "2020-198CD"}, 200, ''),
    ('put', 3, {"name": "MySat3", "type": "TELECOM", "cospar_id": "2020-205CD"}, 200,
     'invalid request due to mission config database is full'),
])
@pytest.mark.data_validation_create_update_pass
# This test scenario verifies the valid value entry of type and cospar_id field with correct status code.
def test_data_validation_create_update_pass(crud_op: str, conf_id: int, data: dict, status_code: int, message: str):
    url = f"{BASE_URL}/configs"
    if crud_op == 'post':
        response = requests.post(url, json=data)
    else:
        url = f"{BASE_URL}/configs/{conf_id}"
        response = requests.put(url, json=data)

    assert_response(response, message, status_code)

    if crud_op == 'post':
        clean_db()


@pytest.mark.parametrize("crud_op, conf_id, data, outcome, status_code", [
    ('post', 0, {"name": "MySat4", "type": "OPTICAL", "cospar_id": "2023-999dd"},
     'invalid request due to invalid COSPAR ID', 400),
    ('post', 0, {"name": "MySat5", "type": "FIRE", "cospar_id": "2024-001XX"},
     'invalid request due to invalid payload type', 400),
    ('post', 0, {"name": "MySat6", "type": "SAR", "cospar_id": "2025-123"},
     'invalid request due to invalid COSPAR ID', 400),
    ('post', 0, {"name": "MySat7", "type": "SAR", "cospar_id": "2025-ABC"},
     'invalid request due to invalid COSPAR ID', 400),
    ('post', 0, {"name": "MySat8", "type": "SAR", "cospar_id": "2025-123456"},
     'invalid request due to invalid COSPAR ID', 400),
    ('post', 0, {"name": "MySat9", "type": "SAR", "cospar_id": "2025-12345"},
     'invalid request due to invalid COSPAR ID', 400),
    ('post', 0, {"name": "MySat9", "type": "optical", "cospar_id": "2025-123AB"},
     'invalid request due to invalid COSPAR ID', 400),
    ('put', 4, {"name": "MySat8", "type": "SAR", "cospar_id": "2026-ZZZ123"},
     'invalid request due to invalid COSPAR ID', 400),
    ('put', 4, {"name": "MySat9", "type": "SAR", "cospar_id": "2027-EF321"},
     'invalid request due to invalid COSPAR ID', 400),
    ('put', 4, {"name": "MySat10", "type": "SAR", "cospar_id": "202-123EF"},
     'invalid request due to invalid COSPAR ID', 400),
    ('put', 4, {"name": "MySat10", "type": "SAR", "cospar_id": "202/123EF"},
     'invalid request due to invalid COSPAR ID', 400)
])
@pytest.mark.data_validation_create_update_fail
# This test scenario verifies the invalid value entry of type and cospar_id field with correct error message and code.
def test_data_validation_create_update_fail(crud_op: str, conf_id: int, data: dict, outcome: str, status_code: int):
    url = f"{BASE_URL}/configs"
    if crud_op == 'post':
        response = requests.post(url, json=data)
    else:
        url = f"{BASE_URL}/configs/{conf_id}"
        response = requests.put(url, json=data)

    assert_response(response, outcome, status_code)


@pytest.mark.parametrize("conf_id, status_code, outcome, message", [
    (1, 200, '', 'Get satellite configuration API Response - Satellite Found:'),
    (0, 404, "resource '0' of type 'Mission'' does not exist",
     'Get satellite configuration API Response - Satellite Not Found:'),
    (10, 404, "resource '10' of type 'Mission'' does not exist",
     'Get satellite configuration API Response - Satellite Not Found:'),
])
@pytest.mark.db_lookup_ranges_validation
# This test scenario is verifying that for non-existing ids the correct error message and status code is shown
def test_db_lookup(conf_id: int, status_code: int, outcome: str, message: str):
    response = requests.get(url=f"{BASE_URL}/configs/{conf_id}")
    assert_response(response, outcome, status_code)


@pytest.mark.parametrize("data, status_code", [
    ({"name": "MySat7", "type": "SAR", "cospar_id": "2020-194CD"}, 200),
    ({"name": "MySat8", "type": "OPTICAL", "cospar_id": "2020-195CD"}, 200),
    ({"name": "MySat9", "type": "TELECOM", "cospar_id": "2020-196CD"}, 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-197CD"}, 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-198CD"}, 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-199CD"}, 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-200CD"}, 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-201CD"}, 400)
])
@pytest.mark.max_data_entries
# This test scenario verifies the req. "The service can store a maximum of `10` configurations at a time".
# By default, the DB has 3 entries already.
def test_max_data_entries(data: dict, status_code: int):
    entries = read_db('all')
    print(f'->DB has {entries} Satellite Configuration right now.')

    url = f"{BASE_URL}/configs"

    response = requests.post(url, json=data)
    assert_response(response, '', status_code)

    entries = read_db('all')
    print(f'->DB has {entries} Satellite Configuration.')

    assert entries <= MAX_CONF


@pytest.mark.parametrize("data_size, status_code", [
    (1, 200),
    (3, 400),
    (10, 400)
])
@pytest.mark.post_with_multiple_data
# Boundary Test: Test for multiple configuration data in one post create.
def test_post_with_multiple_data(data_size: int, status_code: int):
    clean_db()
    url = f"{BASE_URL}/configs"
    if data_size > 1:
        data = [{
            "name": "MySat0",
            "type": "SAR",
            "cospar_id": "2020-190CD"
        }]
        # Create multiple configuration data
        for i in range(1, data_size, 1):
            tmp = [{
                "name": f"MySat{i}",
                "type": "SAR",
                "cospar_id": f"2020-19{i}CD"
            }]
            data = data + tmp
    else:
        data = {"name": "MySat0", "type": "SAR", "cospar_id": "2020-190CD"}
    print(f'=> {data}')

    # Send the data in one post create
    response = requests.post(url, json=data)
    assert_response(response, '', status_code)


@pytest.mark.parametrize("fields, message, status_code", [
    ({}, 'invalid request due to cospar ID is required', 400),
    ({"name": "MySpot0"}, 'invalid request due to cospar ID is required', 400),
    ({"type": "OPTIC"}, 'invalid request due to cospar ID is required', 400),
    ({"cospar_id": "1969-190AA"}, 'invalid request due to name is required', 400),
    ({"name": "MySpot0", "cospar_id": "1969-190AA"}, 'invalid request due to payload type is required', 400),
    ({"type": "OPTIC", "cospar_id": "1969-190AA"}, 'invalid request due to name is required', 400),
    ({"name": " ", "type": "SAR", "cospar_id": "1969-190AA"}, '', 400), # corner case due to space string
    ({"name": "MySpot0", "type": " ", "cospar_id": "1969-190AA"}, '', 400)  # corner case due to space string
])
@pytest.mark.missing_mandatory_fields
# Error injection: Test for empty or missing fields of configuration data in post create.
# All fields are mandatory and can't be missing or have empty string.
def test_missing_mandatory_fields_post(fields: dict, message: str, status_code: int):
    url = f"{BASE_URL}/configs"
    data = {} | fields
    print(f'=> {data}')

    # Send the data in one post create
    response = requests.post(url, json=data)
    assert_response(response, message, status_code)


@pytest.mark.parametrize("fields, status_code", [
    ({"NAmE": "MySpot0", "type": "SAR", "cospar_id": "1969-190AA"}, 200),
    ({"name": "MySpot0", "typ": "SAR", "cospar_id": "1969-190AA"}, 400),
    ({"name": "MySpot0", "type": "SAR", "copar_id": "1969-190AA"}, 400),
    ({"name": "MySpot0", "Jerry": "SAR", "Tom": "1969-190AA"}, 400),
    ({"name": "MySpot0", "typ": "SAR", "cospar_id": "1969-190AA", "type": "OPTICAL"}, 400),])
@pytest.mark.field_name_validation
# Error injection: Test for invalid field names of configuration data in post create.
def test_field_name_validation(fields: dict, status_code: int):
    clean_db()
    url = f"{BASE_URL}/configs"
    data = {} | fields
    print(f'=> {data}')

    # Send the data in one post create
    response = requests.post(url, json=data)
    assert_response(response, 'A', status_code)
