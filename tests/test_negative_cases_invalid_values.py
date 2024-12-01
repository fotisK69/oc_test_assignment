import conftest as conf
import pytest
import requests


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
    url = f"{conf.BASE_URL}/configs"
    if crud_op == 'post':
        response = requests.post(url, json=data)
    else:
        url = f"{conf.BASE_URL}/configs/{conf_id}"
        response = requests.put(url, json=data)

    conf.assert_response(response, outcome, status_code)
