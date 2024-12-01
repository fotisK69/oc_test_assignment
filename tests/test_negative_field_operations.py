import conftest as conf
import pytest
import requests


@pytest.mark.parametrize("fields, message, status_code", [
    ({}, 'invalid request due to cospar ID is required', 400),
    ({"name": "MySpot0"}, 'invalid request due to cospar ID is required', 400),
    ({"type": "OPTIC"}, 'invalid request due to cospar ID is required', 400),
    ({"cospar_id": "1969-190AA"}, 'invalid request due to name is required', 400),
    ({"name": "MySpot0", "cospar_id": "1969-190AA"}, 'invalid request due to payload type is required', 400),
    ({"type": "OPTIC", "cospar_id": "1969-190AA"}, 'invalid request due to name is required', 400),
    ({"name": " ", "type": "SAR", "cospar_id": "1969-190AA"}, '', 400),  # corner case due to space string
    ({"name": "MySpot0", "type": " ", "cospar_id": "1969-190AA"}, '', 400)  # corner case due to space string
])
@pytest.mark.missing_mandatory_fields
# Error injection: Test for empty or missing fields of configuration data in post create.
# All fields are mandatory and can't be missing or have empty string.
def test_missing_mandatory_fields_post(fields: dict, message: str, status_code: int):
    url = f"{conf.BASE_URL}/configs"
    data = {} | fields
    conf.logger.info(f'=> {data}')

    # Send the data in one post create
    response = requests.post(url, json=data)
    conf.assert_response(response, message, status_code)


@pytest.mark.parametrize("fields, status_code", [
    ({"NAmE": "MySpot0", "type": "SAR", "cospar_id": "1969-190AA"}, 200),
    ({"name": "MySpot0", "typ": "SAR", "cospar_id": "1969-190AA"}, 400),
    ({"name": "MySpot0", "type": "SAR", "copar_id": "1969-190AA"}, 400),
    ({"name": "MySpot0", "Jerry": "SAR", "Tom": "1969-190AA"}, 400),
    ({"name": "MySpot0", "typ": "SAR", "cospar_id": "1969-190AA", "type": "OPTICAL"}, 400),])
@pytest.mark.field_name_validation
# Error injection: Test for invalid field names of configuration data in post create.
def test_field_name_validation(fields: dict, status_code: int):
    conf.clean_db_default()
    url = f"{conf.BASE_URL}/configs"
    data = {} | fields
    conf.logger.info(f'=> {data}')

    # Send the data in one post create
    response = requests.post(url, json=data)
    conf.assert_response(response, 'A', status_code)
