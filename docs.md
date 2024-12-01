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

    * **cospar_id (string):** COSPAR identifier, must follow the pattern `YYYY-###XX`, where `YYYY` is the launch year, `###` is a three-digit mission code, and `XX` is a two-letter identifier. This pattern applies for both creation and update requests.
    * **name (string):** Name of the mission.
    * **payload_type (string):** Type of payload (e.g., "OPTICAL", "SAR", "TELECOM").

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

