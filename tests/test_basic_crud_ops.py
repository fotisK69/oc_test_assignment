import conftest as conf
import pytest
import requests


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
    url = f"{conf.BASE_URL}/configs/{conf_id}"

    if crud_op == 'create':
        url = f"{conf.BASE_URL}/configs"
        response = requests.post(url, json=data)
    elif crud_op == 'read':
        response = requests.get(url)
    elif crud_op == 'update':
        response = requests.put(url, json=data)
    else:
        response = requests.delete(url)

    conf.assert_response(response, message, status_code)


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
    url = f"{conf.BASE_URL}/configs"
    if crud_op == 'post':
        response = requests.post(url, json=data)
    else:
        url = f"{conf.BASE_URL}/configs/{conf_id}"
        response = requests.put(url, json=data)

    conf.assert_response(response, message, status_code)

    if crud_op == 'post':
        conf.clean_db_default()
