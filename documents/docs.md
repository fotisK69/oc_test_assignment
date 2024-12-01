# Satellite Configuration Service - API Documentation

The Satellite Configuration Service API allows users to manage configurations for various satellite missions. 
This documentation provides an overview of the available endpoints, request and response formats, and example usage.

## Endpoints

### GET /configs

**Description:** Retrieves a list of all satellite configurations.

* **Method:** GET
* **URL:** /configs
* **Response:** A JSON array containing all satellite configuration objects.

**Example Response:**
```JSON: {
    "meta": null,
    "data": [
        {
            "id": 1,
            "name": "Satellite1",
            "type": "OPTICAL",
            "cospar_id": "2024-003ZZ"
        },
        {
            "id": 2,
            "name": "Satellite2",
            "type": "OPTICAL",
            "cospar_id": "2023-001BC"
        },
        {
            "id": 3,
            "name": "Satellite3",
            "type": "SAR",
            "cospar_id": "2050-002ZZ"
        }
    ],
    "errors": null
}

```

----

### GET /configs/{id}

**Description:** Retrieves the configuration for a specific satellite by its unique mission id.

* **Method:** GET
* **URL:** /configs/{id}
    * `id` is a unique integer identifier for the mission.
* **Response:** JSON object containing the satellite configuration details.


**Example Request:** 

`GET /configs/1`

**Example Response:**

```json
{
  "id": 1,
  "name": "Optic Satellite One",
  "type": "OPTICAL",
  "cospar_id": "2024-003ZZ"
}

```

----

### POST /configs

**Description:** Creates a new satellite configuration. The service can store a maximum of `6` configurations at a time. If this limit is exceeded, an error will be returned.

* **Method:** POST
* **URL:** /configs
* **Request Body:** JSON object with the following required fields:

    * **cospar_id (string):** COSPAR identifier, must follow the pattern `YYYY-###XX`, where `YYYY` is the launch year, `###` is a three-digit mission code, and `XX` is a two-letter (CAPS only) identifier. This pattern applies for both creation and update requests.
    * **name (string):** Name of the mission.
    * **payload_type (string):** Type of payload (e.g., "OPTICAL", "SAR", "TELECOM") (CAPS only).

**All fields are mandatory**

**Example Request Body:**

```json
{
  "cospar_id": "2024-003ZZ",
  "name": "New Satellite Mission",
  "payload_type": "OPTICAL"
}
```

**Response:** JSON object with a confirmation message.

**Example Response:**

```json
{
  "message": "Mission config created successfully."
}
```

----

### DELETE /configs/{id}

**Description:** Deletes a satellite configuration specified by its mission id.

* **Method:** DELETE
* **URL:** /configs/{id}
    * `id` is a unique integer identifier for the mission.
* **Response:** Confirmation message indicating successful deletion.


**Example Request:** 

`DELETE /configs/1`

**Example Response:**

```json
{
  "message": "Mission config deleted successfully."
}
```

----

### PUT /configs/{id}

**Description:** Updates an existing satellite configuration based on id.

* **Method:** PUT
* **URL:** /configs/{id}
    * `id` is a unique integer identifier for the mission.
* **Request Body:** JSON object with any updatable fields:
    * **cospar_id (string, optional)**: COSPAR identifier, must follow the pattern `YYYY-###XX`, where `YYYY` is the launch year, `###` is a three-digit mission code, and `XX` is a two-letter identifier. This pattern applies for both creation and update requests.
    * **name (string, optional)**: Name of the mission.
    * **payload_type (string, optional)**: Type of payload (e.g., "OPTICAL", "SAR", "TELECOM").

**All fields are mandatory**


**Example Request:**

```json
{
  "cospar_id": "2025-005XY",
  "name": "Updated Satellite Mission",
  "payload_type": "SAR"
}
```

**Response:** JSON object with a confirmation message.

**Example Response:**

```json
{
  "message": "Mission config updated successfully."
}
```

## ERROR Handling and responses (chapter is missing)

### Error messages during post and put operations
#### Invalid data values for fields cospar_id and type:
* invalid request due to invalid COSPAR ID
* invalid request due to invalid payload type
#### Missing fields in the post/put request:
(All fields are mandatory)
* invalid request due to cospar ID is required
* invalid request due to name is required
* invalid request due to payload type is required

## Frontend observations and improvements
* Give hint in each input field what to insert especialy for "COSPAR ID" and "Payload Type".
* Suggestion to have pull down list for "Payload Type" with the type that are allowed.
* Text field for the result when searching for a "Get Configuration by ID". In the same page.
* When creating now result is showing to the userr if successful or not.
* No Update of existing configuration is poaaible via the web-page.
* No possibility to get all the active configuration:
  ERROR  [0423] A path was reached with no defined route: URL '/configs/?' method 'GET'  httpRequest="{GET /configs/? Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0 }"
  {"meta":null,"data":null,"errors":[{"message":"'resource '/configs/?' of type 'page'' does not exist","source":"data-server"}]}
* In case server is down and user tries to get or create a new configuration it will get a normal page "This site can’t be reached" without an indication/hint to check if the server is up.
  It rather advises the user to check the internet and firewall.
