# Satellite Configuration Service - Automation Testing Challenge

## Project Overview

In this project, you are tasked with validating and testing a RESTful API for managing satellite configurations. This involves writing automated tests for various API operations and documenting issues in the provided API documentation. Additionally, you will create a test plan for a mock frontend release associated with this API.

## Project Goals

* **Verify and test** the API's endpoint functionality and error handling.
* **Validate and provide feedback** on the API documentation’s accuracy.
* **Create a test plan** for the new frontend release, focusing on the create & search functionality as well as user experience for managing satellite configurations.

## Assignment

### Setup Instructions

* **Download and run the binary server** provided in the challenge package. This is a REST API server that serves satellite configurations.
  * To run the binary server on port `1234`: 
  ```bash
  ./automation-tester-challenge-project --port 1234
  ```
* **Front-End (FE) File:** Review the simple HTML file, which acts as a mock version of the future release of the satellite configuration frontend. This frontend has basic UI elements, such as text boxes, for searching by missionID.
* **Documentation:** Review the provided API documentation detailing each endpoint.

## API Specifications

Everything related to the API Spec can be found [here](docs.md)

## Assignment Steps

### Part 1: API Testing

1. **Writing Automated Tests**

    Create a set of tests (in a language/framework of your choice) that test the API endpoints for the following:

    * **Basic CRUD Operations:** Test each of the provided endpoints (GET, POST, PUT, DELETE) for standard operation.
    * **Boundary Condition:** Test the server’s behavior on any boundary conditions you find are necessary.
    * **Data Validation:** Test the server’s response to invalid data formats in the request body.
    * **Error Injection:** Handle a deliberate error by querying a specific missionID that returns incorrect data (e.g., malformed JSON or unexpected field values) and ensure your test script can identify this inconsistency.

2. **Analyze the Server’s Behavior**

    Observe the server’s behavior and error-handling responses. Report any anomalies you can find.

### Part 2: Documentation Review

1. **Identify Documentation Inconsistencies**

    As part of your API testing, validate the provided API documentation for accuracy. Specifically:

    * Check for inconsistencies between the documented request/response formats and actual API responses.
    * Note any differences in field formats and incorrect or missing fields.

2. **Document Feedback**

    Write up a summary of any discrepancies or unclear instructions in the documentation. Be specific about what is incorrect or missing, as well as suggestions for improvement.

    **Example Template for Documentation Feedback**

    ```
    Endpoint: GET /configs/:missionID

    Issue: Response body includes a launch_date field in DD-MM-YYYY format, while the documentation specifies YYYY-MM-DD.
    
    Suggested Correction: Update the documentation to specify the correct format or update the API to match the documented format.
    ```

### Part 3: Frontend Test Plan

1. **Review the Frontend (FE) Mock Release**

    The mock frontend HTML file has been provided to represent a future release. This frontend includes a text box for searching missionID as well as adding a new config.

2. **Write a Test Plan**

    Outline a test plan for the frontend that includes the following:

    * Functional Testing: Plan tests to verify that users can create new configs. Plan tests to verify that users can search by missionID and retrieve accurate configuration data. 
    * Usability Testing: Assess the usability of both the search & create functionality, given any limitations you may find.
    * Error Handling and Edge Cases: Define scenarios for handling invalid operations.
    * Suggestions for Improvement: Based on your review, suggest any UI or UX improvements that could enhance the ease of use and accuracy of the search functionality.


## Expected Deliverables

1. **API Automated Tests**

    An automated test set covering the full scope of API testing as outlined.

2. **Documentation Feedback Summary**

    A written summary highlighting any issues or inaccuracies in the API documentation.

3. **Frontend Test Plan**

    A detailed test plan for the frontend that includes functional, usability, and edge-case testing.

## Additional Notes

* **Time Limit:** You are expected to complete the assignment within 7 hours.
* **Submission:** Please submit all code, feedback, and documentation as a zip file or a link to a version-controlled repository.
* **Evaluation:** Your submission will be evaluated on the completeness and accuracy of your test coverage, clarity of documentation feedback, and the thoroughness of your frontend test plan. If you run out of time, just detail what you would have done given more time. Please also prepare a demo (of about 10-20 minutes) to present of the day of the interview, about the solution used, the approach taken, the main challenges and next steps.

This assignment is designed to evaluate your technical skills in API and UI testing, as well as your ability to validate and improve technical documentation. Good luck, and we look forward to your submission!
