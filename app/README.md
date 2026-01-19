# Flask CRUD Application with Firestore

A modern full-stack web application built with Flask, featuring a Jinja2 frontend, Firestore database, and JWT-based authentication.

## Features

- **Modern Authentication**: JWT-based authentication flow with session management
- **CRUD Operations**: Full Create, Read, Update, Delete functionality for items
- **Firestore Database**: Google Cloud Firestore for data persistence
- **RESTful API**: JSON API endpoints for programmatic access
- **Responsive UI**: Clean, modern Jinja2 templates with responsive CSS
- **Docker Support**: Complete Docker Compose setup for local development

## Tech Stack

- **Backend**: Flask 3.0
- **Database**: Google Cloud Firestore
- **Authentication**: JWT tokens with bcrypt password hashing
- **Frontend**: Jinja2 templates with modern CSS
- **Deployment**: Docker & Docker Compose

## Project Structure

```
app/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── db.py                  # Firestore database initialization
├── models.py              # User and Item models
├── auth.py                # Authentication helpers and decorators
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── .env.example           # Environment variables template
├── templates/             # Jinja2 templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── item_form.html
└── static/
    └── css/
        └── style.css      # Application styles
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd gcp-cloudrun-flask-jinja-firestore/app
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Start the application with Docker Compose**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - Firestore emulator on port 8080
   - Flask application on port 5000

4. **Access the application**
   - Web Interface: http://localhost:5000
   - Firestore Emulator: http://localhost:8080

### First-Time Setup

1. Navigate to http://localhost:5000
2. Click "Register" to create a new account
3. Fill in your name, email, and password
4. You'll be automatically logged in and redirected to the dashboard

## Usage

### Web Interface

1. **Login/Register**: Access authentication pages at `/login` and `/register`
2. **Dashboard**: View all your items at `/dashboard`
3. **Create Item**: Click "Create New Item" button
4. **Edit Item**: Click "Edit" button on any item card
5. **Delete Item**: Click "Delete" button (with confirmation)

### API Endpoints

#### Authentication

**Register User**
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Login**
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Items (Requires Authentication)

**Get All Items**
```bash
GET /api/items
Authorization: Bearer <your-jwt-token>
```

**Create Item**
```bash
POST /api/items
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "title": "My Item",
  "description": "Item description"
}
```

**Get Single Item**
```bash
GET /api/items/<item_id>
Authorization: Bearer <your-jwt-token>
```

**Update Item**
```bash
PUT /api/items/<item_id>
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description"
}
```

**Delete Item**
```bash
DELETE /api/items/<item_id>
Authorization: Bearer <your-jwt-token>
```

## Development

### Running without Docker

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Firestore emulator separately**
   ```bash
   gcloud emulators firestore start --host-port=localhost:8080
   ```

4. **Run the application**
   ```bash
   export FIRESTORE_EMULATOR_HOST=localhost:8080
   python app.py
   ```

### Environment Variables

Configure these in `.env` file:

- `SECRET_KEY`: Flask session secret key
- `JWT_SECRET_KEY`: JWT token signing key
- `FIRESTORE_PROJECT_ID`: Google Cloud project ID
- `USE_FIRESTORE_EMULATOR`: Set to `true` for local development
- `FIRESTORE_EMULATOR_HOST`: Firestore emulator host (default: firestore:8080)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to GCP credentials (production only)

## Deployment to Google Cloud Run

### Prerequisites
- Google Cloud account
- gcloud CLI installed
- Firestore database created in your GCP project

### Steps

1. **Enable required APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable firestore.googleapis.com
   ```

2. **Create Firestore database** (if not already created)
   - Go to Google Cloud Console
   - Navigate to Firestore
   - Create a Native mode database

3. **Build and deploy**
   ```bash
   gcloud run deploy flask-crud-app \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars USE_FIRESTORE_EMULATOR=false,FIRESTORE_PROJECT_ID=your-project-id \
     --set-secrets SECRET_KEY=flask-secret:latest,JWT_SECRET_KEY=jwt-secret:latest
   ```

4. **Set up secrets** (recommended for production)
   ```bash
   echo -n "your-secret-key" | gcloud secrets create flask-secret --data-file=-
   echo -n "your-jwt-secret" | gcloud secrets create jwt-secret --data-file=-
   ```

## Security Considerations

- Change default `SECRET_KEY` and `JWT_SECRET_KEY` in production
- Use environment variables for sensitive configuration
- Enable HTTPS in production
- Implement rate limiting for API endpoints
- Add CSRF protection for web forms
- Use secure password requirements
- Implement session timeout

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for learning or commercial purposes.

## Support

For issues and questions, please open an issue on GitHub.
