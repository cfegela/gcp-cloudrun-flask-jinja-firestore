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
.
├── app/                       # Flask application
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── db.py                  # Firestore database initialization
│   ├── models.py              # User and Item models
│   ├── auth.py                # Authentication helpers and decorators
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Docker configuration
│   ├── docker-compose.yml     # Docker Compose setup
│   ├── .env.example           # Environment variables template
│   ├── templates/             # Jinja2 templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── item_form.html
│   └── static/
│       └── css/
│           └── style.css      # Application styles
├── ops/                       # Operations and infrastructure
│   └── terraform/             # Terraform configuration for GCP
│       ├── main.tf            # Main infrastructure resources
│       ├── variables.tf       # Input variables
│       ├── outputs.tf         # Output values
│       ├── versions.tf        # Provider versions
│       ├── terraform.tfvars.example
│       ├── backend.tf.example # GCS backend configuration
│       └── README.md          # Terraform documentation
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd gcp-cloudrun-flask-jinja-firestore
   ```

2. **Create environment file**
   ```bash
   cp app/.env.example app/.env
   ```

3. **Start the application with Docker Compose**
   ```bash
   cd app && docker-compose up --build
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
   pip install -r app/requirements.txt
   ```

3. **Start Firestore emulator separately**
   ```bash
   gcloud emulators firestore start --host-port=localhost:8080
   ```

4. **Run the application**
   ```bash
   export FIRESTORE_EMULATOR_HOST=localhost:8080
   python app/app.py
   ```

### Environment Variables

Configure these in `app/.env` file:

- `SECRET_KEY`: Flask session secret key
- `JWT_SECRET_KEY`: JWT token signing key
- `FIRESTORE_PROJECT_ID`: Google Cloud project ID
- `USE_FIRESTORE_EMULATOR`: Set to `true` for local development
- `FIRESTORE_EMULATOR_HOST`: Firestore emulator host (default: firestore:8080)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to GCP credentials (production only)

## Deployment to Google Cloud Run

You can deploy this application using either Terraform (recommended) or the gcloud CLI.

### Option 1: Terraform Deployment (Recommended)

Terraform provides infrastructure-as-code for repeatable, version-controlled deployments.

#### Prerequisites
- Google Cloud account with billing enabled
- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated
- Docker installed

#### Steps

1. **Authenticate with GCP**
   ```bash
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Configure Terraform variables**
   ```bash
   cd ops/terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your project ID and preferences
   ```

3. **Initialize and deploy infrastructure**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **Build and push Docker image**
   ```bash
   # Get the Artifact Registry URL from Terraform output
   export DOCKER_REPO=$(terraform output -raw artifact_registry_repository)

   # Configure Docker authentication
   gcloud auth configure-docker $(echo $DOCKER_REPO | cut -d'/' -f1)

   # Build and push image
   cd ../../app
   docker build -t ${DOCKER_REPO}/flask-app:latest .
   docker push ${DOCKER_REPO}/flask-app:latest
   ```

5. **Access your application**
   ```bash
   cd ../ops/terraform
   terraform output cloud_run_url
   ```

**Resources Created:**
- Cloud Run service with autoscaling
- Firestore database (Native mode)
- Secret Manager secrets (auto-generated)
- Artifact Registry repository
- Service account with minimal permissions
- IAM bindings for secure access

For detailed Terraform documentation, see [ops/terraform/README.md](ops/terraform/README.md).

### Option 2: gcloud CLI Deployment

For quick deployments without infrastructure-as-code.

#### Prerequisites
- Google Cloud account
- gcloud CLI installed
- Firestore database created in your GCP project

#### Steps

1. **Enable required APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable firestore.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   ```

2. **Create Firestore database** (if not already created)
   - Go to Google Cloud Console
   - Navigate to Firestore
   - Create a Native mode database

3. **Set up secrets**
   ```bash
   echo -n "your-secret-key-here" | gcloud secrets create flask-secret --data-file=-
   echo -n "your-jwt-secret-here" | gcloud secrets create jwt-secret --data-file=-
   ```

4. **Build and deploy**
   ```bash
   gcloud run deploy flask-crud-app \
     --source ./app \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars USE_FIRESTORE_EMULATOR=false,FIRESTORE_PROJECT_ID=your-project-id \
     --set-secrets SECRET_KEY=flask-secret:latest,JWT_SECRET_KEY=jwt-secret:latest
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
