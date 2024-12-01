import conftest as conf
import pytest
import requests


@pytest.mark.parametrize("conf_id, status_code, outcome, message", [
    (0, 404, "resource '0' of type 'Mission'' does not exist",
     'Get satellite configuration API Response - Satellite Not Found:'),
    (10, 404, "resource '10' of type 'Mission'' does not exist",
     'Get satellite configuration API Response - Satellite Not Found:'),
])
@pytest.mark.db_lookup_ranges_validation
# This test scenario is verifying that for non-existing ids the correct error message and status code is shown
def test_db_lookup(conf_id: int, status_code: int, outcome: str, message: str):

    response = requests.get(url=f"{conf.BASE_URL}/configs/{conf_id}")
    conf.assert_response(response, outcome, status_code)


@pytest.mark.parametrize("data, message, status_code", [
    ({"name": "MySat7", "type": "SAR", "cospar_id": "2020-194CD"}, '', 200),
    ({"name": "MySat8", "type": "OPTICAL", "cospar_id": "2020-195CD"}, '', 200),
    ({"name": "MySat9", "type": "TELECOM", "cospar_id": "2020-196CD"}, '', 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-197CD"}, '', 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-198CD"}, '', 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-199CD"}, '', 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-200CD"}, '', 200),
    ({"name": "MySat10", "type": "TELECOM", "cospar_id": "2020-201CD"},
     'invalid request due to mission config database is full', 400)
])
@pytest.mark.max_data_entries
# This test scenario verifies the req. "The service can store a maximum of `10` configurations at a time".
# By default, the DB has 3 entries already.
def test_max_data_entries(data: dict, message, status_code: int):
    entries = conf.read_get('all')
    conf.logger.info(f'->DB has {entries} Satellite Configuration right now.')

    url = f"{conf.BASE_URL}/configs"

    response = requests.post(url, json=data)
    conf.assert_response(response, message, status_code)

    entries = conf.read_get('all')
    conf.logger.info(f'->DB has {entries} Satellite Configuration.')

    assert entries <= conf.MAX_DB_CONF


@pytest.mark.parametrize("data_size, message, status_code", [
    (1, '', 200),
    (3, 'invalid request due to json: cannot unmarshal array into Go value of type '
        'missionconfig.CreateMissionConfig', 400),
    (10, 'invalid request due to json: cannot unmarshal array into Go value of type '
         'missionconfig.CreateMissionConfig', 400)
])
@pytest.mark.post_with_multiple_data
# Boundary Test: Test for multiple configuration data in one post create.
def test_post_with_multiple_data(data_size: int, message: str, status_code: int):
    conf.clean_db_default()
    url = f"{conf.BASE_URL}/configs"
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
    conf.assert_response(response, message, status_code)
