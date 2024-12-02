# User Guide for Client Information Management REST API

This guide provides instructions on how to use the API to create, retrieve, update, delete client data.

---

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
  - [Install Dependencies](#install-dependencies)
  - [Set Up a Virtual Environment](#set-up-a-virtual-environment)
  - [Run Application](#run-application)
- [Usage](#usage)
  - [Base URL](#base-url)
  - [API Endpoints](#api-endpoints)
    - [Retrieve All Clients](#retrieve-all-clients)
    - [Retrieve a Client by ID](#retrieve-a-client-by-id)
    - [Create a New Client](#create-a-new-client)
    - [Update a Client](#update-a-client)
    - [Delete a Client](#delete-a-client)
- [Error Handling](#error-handling)


## Introduction
The REST API provides the following functionalities:
- Retrieve all clients. 
- Retrieve a specific client by ID. 
- Create a new client. 
- Update an existing client's information. 
- Delete a client by ID.

## Installation

### Install Dependencies
To set up the application, install all required Python packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Set Up a Virtual Environment
Using a virtual environment ensures isolated dependency management.

**Create the Virtual Environment:**
```bash
python3 -m venv env
```

**Activate the Virtual Environment:**
```bash
# For macOS/Linux:
source env/bin/activate  
```
```bash
# For Windows:
env\Scripts\activate
```

### Run Application
Start the server with the following command:
```bash
uvicorn app.main:app --reload
```
The application will be accessible at `http://127.0.0.1:8000`.

---
## Usage

### Base UR
All API endpoints are relative to the base URL: 
```arduino
http://127.0.0.1:8000/clients
```
### API Endpoints
#### Retrieve All Clients
- **Method**: `GET`
- **Endpoint:**`/clients`
- **Description:**  Fetches all registered clients.
- **Request Example:**  
  ```bash
  curl -X GET "http://127.0.0.1:8000/clients"
  ```
  
#### Retrieve a Client by ID
- **Method**: `GET`
- **Endpoint:**`/clients/{id}`
- **Description:**  Fetches a specific client’s data by ID.
- **Request Example:**  
  ```bash
  curl -X GET "http://127.0.0.1:8000/clients/4"
  ```

- **Response Example:**
  ```json
  {
    "age": 22,
    "gender": "male",
    "work_experience": 0,
    "canada_workex": 0,
    "dep_num": 3,
    "canada_born": "no",
    "citizen_status": "student visa",
    "level_of_schooling": "Some college",
    "fluent_english": "intermediate",
    "reading_english_scale": 7,
    "speaking_english_scale": 7,
    "writing_english_scale": 7,
    "numeracy_scale": 7,
    "computer_scale": 8,
    "transportation_bool": "no",
    "caregiver_bool": "yes",
    "housing": "dormitory",
    "income_source": "scholarship",
    "felony_bool": "no",
    "attending_school": "yes",
    "currently_employed": "no",
    "substance_use": "no",
    "time_unemployed": 0,
    "need_mental_health_support_bool": "no",
    "client_id": 4
  }
  ```

#### Create a New Client
- **Method**: `POST`
- **Endpoint:**`/clients`
- **Description:** Adds a new client to the database.
- **Request Example:**
  - Content-Type: `application/json`
  - Request Body:
  ```json
    {
    "age": 22,
    "gender": "male",
    "work_experience": 0,
    "canada_workex": 0,
    "dep_num": 3,
    "canada_born": "no",
    "citizen_status": "student visa",
    "level_of_schooling": "",
    "fluent_english": "",
    "reading_english_scale": 0,
    "speaking_english_scale": 0,
    "writing_english_scale": 0,
    "numeracy_scale": 0,
    "computer_scale": 8,
    "transportation_bool": "no",
    "caregiver_bool": "yes",
    "housing": "dormitory",
    "income_source": "scholarship",
    "felony_bool": "no",
    "attending_school": "yes",
    "currently_employed": "no",
    "substance_use": "no",
    "time_unemployed": 0,
    "need_mental_health_support_bool": "no"
    }
  ```
#### Update a Client
- **Method**: `PUT`
- **Endpoint:** `/clients/{id}`
- **Description:**  Updates an existing client’s data.
- **Request Example:**
  - Content-Type: `application/json`
  - Request Body:
    ```json
    {
          "age": 30,
          "gender": "female",
          "work_experience": 5
    }
    ```


#### Delete a Client
- **Method**: `DELETE`
- **Endpoint:** `/clients/{id}`
- **Description:**  Removes a client from the database.
- **Request Example:**
  ```bash
  curl -X DELETE "http://127.0.0.1:8000/clients/4"
  ```

## Error Handling

| Error Code | Description                  | Solution                             |
|------------|------------------------------|--------------------------------------|
| 400        | Invalid input or missing fields | Verify and correct your request.    |
| 401        | Unauthorized access          | Ensure your API key is correct.      |
| 404        | Resource not found           | Verify the endpoint and resource ID. |
| 500        | Internal server error        | Retry or contact support.            |

