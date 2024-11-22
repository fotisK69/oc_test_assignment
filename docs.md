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
```json
[
  {
    "id": "1",
    "name": "Optic Satellite One",
    "type": "OPTIC",
    "cospar_id": "2024-003ZZZ"
  },
  {
    "id": "2",
    "name": "Optic Satellite Two",
    "type": "OPTIC",
    "cospar_id": "2023-001ABC"
  },
  {
    "id": "3",
    "name": "Optic Satellite Three",
    "type": "OPTIC",
    "cospar_id": "2050-002ZZZ"
  }
]

```

----

### GET /configs/{id}

**Description:** Retrieves the configuration for a specific satellite by its unique mission id.

* **Method:** GET
* **URL:** /configs/{id}
    * `id` is a unique string identifier for the mission.
* **Response:** JSON object containing the satellite configuration details.


**Example Request:** 

`GET /configs/1`

**Example Response:**

```json
{
  "id": "1",
  "name": "Optic Satellite One",
  "type": "OPTIC",
  "cospar_id": "2024-003ZZZ"
}

```

----

### POST /configs

**Description:** Creates a new satellite configuration. The service can store a maximum of `10` configurations at a time. If this limit is exceeded, an error will be returned.

* **Method:** POST
* **URL:** /configs
* **Request Body:** JSON object with the following required fields:

    * **cospar_id (string):** COSPAR identifier, must follow the pattern `YYYY-###XXX`, where `YYYY` is the launch year, `###` is a three-digit mission code, and `XXX` is a three-letter identifier. This pattern applies for both creation and update requests.
    * **name (string):** Name of the mission.
    * **payload_type (string):** Type of payload (e.g., "OPTIC", "SARS", "TELECOM").

**Example Request Body:**

```json
{
  "cospar_id": "2024-003ZZZ",
  "name": "New Satellite Mission",
  "payload_type": "OPTIC"
}
```

**Response:** JSON object with a confirmation message.

**Example Response:**

```json
{
  "message": "Mission configuration created successfully."
}
```

----

### DELETE /configs/{id}

**Description:** Deletes a satellite configuration specified by its mission id.

* **Method:** DELETE
* **URL:** /configs/{id}
    * `id` is a unique string identifier for the mission.
* **Response:** Confirmation message indicating successful deletion.


**Example Request:** 

`DELETE /configs/1`

**Example Response:**

```json
{
  "message": "Mission configuration deleted successfully."
}
```

----

### PUT /configs/{id}

**Description:** Updates an existing satellite configuration based on id.

* **Method:** PUT
* **URL:** /configs/{id}
    * `id` is a unique string identifier for the mission.
* **Request Body:** JSON object with any updatable fields:
    * **cospar_id (string, optional)**: COSPAR identifier, must follow the pattern `YYYY-###XXX`, where `YYYY` is the launch year, `###` is a three-digit mission code, and `XXX` is a three-letter identifier. This pattern applies for both creation and update requests.
    * **name (string, optional)**: Name of the mission.
    * **payload_type (string, optional)**: Type of payload (e.g., "OPTIC", "SARS", "TELECOM").


**Example Request:**

```json
{
  "cospar_id": "2025-005XYZ",
  "name": "Updated Satellite Mission",
  "payload_type": "SARS"
}
```

**Response:** JSON object with a confirmation message.

**Example Response:**

```json
{
  "message": "Mission configuration updated successfully."
}
```
