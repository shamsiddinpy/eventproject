Event Management API
A RESTful API built with Django REST Framework for managing events. This API allows authenticated users to create, update, list, and delete events with features like JWT authentication, pagination, and filtering.

Features
User Authentication
JWT-based authentication (signup, login, token refresh)
Only authenticated users can create/update events
Users can only edit their own events
Event Management
Create, read, update, and delete events
Paginated list of events
Filter events by date range and location
API Documentation
Interactive API documentation with Swagger and ReDoc
Postman collection included
Development Tools
Docker for containerization
Unit tests for both auth and events
PostgreSQL database
Technology Stack
Python 3.11
Django 4.2
Django REST Framework
PostgreSQL
JWT Authentication
Docker & Docker Compose
Pytest for testing
Project Structure
event_management/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── event_management/       # Main project settings
├── authentication/         # Auth app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── events/                 # Events app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   ├── permissions.py
│   └── tests.py
└── postman/               # API testing collection
    └── Event_Management_API.json
Setup Instructions
Using Docker (Recommended)
Clone the repository:
bash
git clone https://github.com/yourusername/event-management-api.git
cd event-management-api
Create an .env file (optional - defaults are provided in docker-compose.yml):
DATABASE_URL=postgresql://postgres:postgres@db:5432/eventmanagement
DEBUG=True
SECRET_KEY=your_secret_key_here
Build and start the containers:
bash
docker-compose up --build
Run migrations:
bash
docker-compose exec web python manage.py migrate
Create a superuser (optional):
bash
docker-compose exec web python manage.py createsuperuser
Access the API at http://localhost:8000
Manual Setup
Clone the repository:
bash
git clone https://github.com/yourusername/event-management-api.git
cd event-management-api
Create and activate a virtual environment:
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
bash
pip install -r requirements.txt
Set up PostgreSQL database and update settings accordingly in settings.py
Run migrations:
bash
python manage.py migrate
Run the development server:
bash
python manage.py runserver
Access the API at http://localhost:8000
API Endpoints
Authentication
POST /api/auth/register/ - Register a new user
POST /api/auth/login/ - Login and get JWT tokens
POST /api/auth/token/refresh/ - Refresh JWT token
Events
GET /api/events/ - List all events (with pagination)
GET /api/events/?min_date=2023-05-01&max_date=2023-06-01&location=New York - Filter events
GET /api/events/{id}/ - Get a specific event
POST /api/events/ - Create a new event (requires authentication)
PUT /api/events/{id}/ - Update an event (requires authentication and ownership)
PATCH /api/events/{id}/ - Partially update an event (requires authentication and ownership)
DELETE /api/events/{id}/ - Delete an event (requires authentication and ownership)
API Documentation
Swagger UI: /swagger/
ReDoc: /redoc/
Testing
Running Tests
bash
# Using Docker
docker-compose exec web pytest

# Manual
pytest
Using Postman
Import the provided Postman collection (postman/Event_Management_API.json) to test all endpoints.

Set your environment variable base_url to where your API is running (e.g., http://localhost:8000)
Register a user or login with an existing user
The login response will contain tokens; set the access_token and refresh_token variables in your Postman environment
Use the endpoints to create, read, update, and delete events
Event Model
The Event model includes the following fields:

title (string) - Title of the event
description (text) - Detailed description of the event
date (ISO date) - Date and time of the event
location (string) - Location of the event
created_by (user reference) - User who created the event
created_at (datetime) - Timestamp of creation
updated_at (datetime) - Timestamp of last update
License
MIT License

