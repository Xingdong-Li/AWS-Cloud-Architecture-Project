# Cloud Architecture Project

This project demonstrates a cloud architecture using Flask, DynamoDB, and S3 with Localstack for local AWS service emulation. It includes REST API endpoints for creating, reading, updating, and deleting items stored in DynamoDB and S3. The project is set up to run in Docker containers using Docker Compose and includes automated testing with pytest.

## Project Structure
cloud_architecture_project/
├── app/
│ ├── init.py
│ └── main.py
├── tests/
│ ├── init.py
│ └── test_app.py
├── docker-compose.test.yml
├── docker-compose.yml
├── Dockerfile
├── init.sh
├── README.md
├── requirements.txt
└── run_tests.sh


## Prerequisites

- Docker
- Docker Compose

## Setup

### 1. Build and Run the Application

To start the application stack and keep it running until manually stopped:

```sh
docker-compose up --build
```
This script will:

- Build the Docker images for your application.
- Start the services defined in docker-compose.yml (your app and Localstack).
- Run the initialization script (init.sh) to set up the S3 bucket and DynamoDB table.
- The API will be accessible at http://localhost:8000.

### 2. Run the Tests

To run the tests and exit based on the result:

```sh
./run_tests.sh
```

This script will:

- Start the services defined in docker-compose.test.yml.
- Run the tests using pytest.

### API Endpoints
- GET /items/{item_id}: Get an item by ID
- POST /items: Create a new item
- PUT /items/{item_id}: Update an item by ID
- DELETE /items/{item_id}: Delete an item by ID