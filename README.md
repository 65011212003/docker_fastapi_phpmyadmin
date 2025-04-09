# FastAPI with Docker and MySQL

This project demonstrates a FastAPI application with MySQL database and PHPMyAdmin for database management, all containerized with Docker.

## Project Structure

```
.
├── app/
│   └── main.py         # FastAPI application
├── Dockerfile          # FastAPI application container
├── docker-compose.yml  # Service orchestration
└── requirements.txt    # Python dependencies
```

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Running the Application

1. Build and start the containers:
   ```
   docker-compose up -d
   ```

2. The following services will be available:
   - FastAPI application: http://localhost:8000
   - FastAPI Swagger documentation: http://localhost:8000/docs
   - PHPMyAdmin: http://localhost:8080 (Server: db, Username: root, Password: password)

3. Stop the containers:
   ```
   docker-compose down
   ```

## API Endpoints

- `GET /`: Home endpoint
- `GET /items/`: List all items
- `POST /items/?name=item_name&description=item_description`: Create a new item 