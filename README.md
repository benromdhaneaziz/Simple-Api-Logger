# Simple API Logger

## Overview
**Simple API Logger** is a lightweight REST API built using FastAPI. It logs incoming requests, provides simple analytics, and features a modern web dashboard for viewing logs and statistics. The application uses SQLite for data storage and is organized into modular components for clarity and maintainability.

A unique feature is the **trigger500** mechanism—by sending a specific payload, you can intentionally trigger a 500 Internal Server Error for testing purposes. This helps ensure that error handling and logging are working as expected.

## Features
- **API Endpoints:**
  - **POST /api/log:** Accepts JSON data to log a new message.
    - If `"message": "trigger500"` is provided, the endpoint intentionally causes a division by zero error to trigger a 500 error.
  - **GET /api/logs:** Retrieves logged entries with optional filtering (e.g., by status code and limit).
  - **GET /api/stats:** Provides analytics including:
    - Total number of requests
    - Count of successful (2xx) and error (≥400) responses
    - Average response time
    - Most commonly accessed endpoints
  - **GET /**: Serves the modern web dashboard.

- **Web Dashboard:**
  - Displays key statistics in stylish Bootstrap cards.
  - Lists the most commonly accessed endpoints.
  - Provides a logs table with filtering options.
  - Auto-refreshes every 5 seconds.

- **Custom Logging Middleware:**
  - Captures all requests—including errors—and logs HTTP method, URL, request body, status code, and response time.

- **Trigger500 Mechanism:**
  - Send a POST request with `"message": "trigger500"` to simulate a 500 Internal Server Error.
  - This error is logged and displayed in the dashboard, enabling comprehensive error handling tests.

## Project Structure
```
simple_api_logger/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application, middleware registration, routers, etc.
│   ├── database.py      # SQLite connection and initialization
│   ├── models.py        # Pydantic models for request validation
│   ├── middleware.py    # Logging middleware capturing all requests and errors
│   └── routers/
│       ├── __init__.py
│       ├── logs.py      # Endpoints: POST /api/log (with trigger500) and GET /api/logs
│       └── stats.py     # Endpoint: GET /api/stats (analytics)
├── static/
│   ├── css/
│   │   └── styles.css   # Custom CSS for dashboard styling
│   └── js/
│       └── main.js      # JavaScript for fetching and auto-refreshing data
├── templates/
│   └── index.html       # HTML dashboard view (uses Bootstrap 5)
├── README.md            # This file
└── requirements.txt     # List of dependencies
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/simple_api_logger.git
cd simple_api_logger
```

### 2. Create and Activate a Virtual Environment

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload
```
The API and dashboard will be accessible at [http://localhost:8000](http://localhost:8000).

## Example API Calls

### Log a New Message (Normal Request)
```bash
curl -X POST "http://localhost:8000/api/log"      -H "Content-Type: application/json"      -d '{
           "message": "Hello World",
           "priority": "high",
           "tags": ["test", "example"]
         }'
```

### Trigger a 500 Internal Server Error
Send a POST request with `"message": "trigger500"`:
```bash
curl -X POST "http://localhost:8000/api/log"      -H "Content-Type: application/json"      -d '{
           "message": "trigger500",
           "priority": "high",
           "tags": ["test", "example"]
         }'
```
This causes a division by zero error, resulting in a 500 error that is logged and displayed.

### Retrieve Logs
```bash
curl "http://localhost:8000/api/logs?limit=50"
```

### Retrieve Analytics
```bash
curl "http://localhost:8000/api/stats"
```

### Access the Dashboard
Open your web browser and go to [http://localhost:8000](http://localhost:8000).

## Design Choices

### **FastAPI**
- Selected for its speed, ease of asynchronous programming, and powerful validation features using Pydantic.

### **SQLite**
- A lightweight, file-based database that simplifies deployment while being sufficient for a logging system.

### **Modular Architecture**
- The code is organized into distinct modules (routers, models, middleware, etc.) to ensure clarity, ease of maintenance, and scalability.

### **Jinja2 & Bootstrap 5**
- **Jinja2** renders the HTML dashboard.
- **Bootstrap 5** provides a modern, responsive design for the user interface.

### **Custom Logging Middleware**
- Intercepts all requests and logs critical details, ensuring even error responses (including 500 errors triggered by `trigger500`) are captured.

---

### 🚀 **Enjoy using Simple API Logger!**
