# Terraform Configuration for Flask CRUD App

This directory contains Terraform configuration to deploy the Flask CRUD application to Google Cloud Platform.

## Resources Created

- **Cloud Run Service**: Hosts the Flask application
- **Firestore Database**: Native mode database for data persistence
- **Secret Manager**: Stores `SECRET_KEY` and `JWT_SECRET_KEY` securely
- **Artifact Registry**: Docker repository for application images
- **Service Account**: Dedicated service account with minimal permissions
- **IAM Bindings**: Proper access controls for Firestore and Secret Manager

## Prerequisites

1. [Terraform](https://www.terraform.io/downloads.html) >= 1.0
2. [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated
3. GCP project with billing enabled
4. Docker installed for building images

## Quick Start

### 1. Authenticate with GCP

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Configure Variables

```bash
cd ops/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your project details
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Build and Push Docker Image

Before deploying, build and push your Docker image to Artifact Registry:

```bash
# From the repository root
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"

# Build the image
cd app
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/flask-crud-app-repo/flask-app:latest .

# Configure Docker for Artifact Registry
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Push the image (Note: Artifact Registry must be created first)
# You may need to run 'terraform apply -target=google_artifact_registry_repository.app_repo' first
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/flask-crud-app-repo/flask-app:latest
```

### 5. Deploy Infrastructure

```bash
# Review the plan
terraform plan

# Apply the configuration
terraform apply
```

### 6. Access Your Application

After deployment, Terraform will output the Cloud Run URL:

```bash
terraform output cloud_run_url
```

## Configuration Options

### Variables

Edit `terraform.tfvars` to customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `project_id` | GCP Project ID | Required |
| `region` | GCP region | `us-central1` |
| `service_name` | Cloud Run service name | `flask-crud-app` |
| `firestore_location` | Firestore database location | `nam5` |
| `environment` | Environment name | `dev` |
| `allow_unauthenticated` | Allow public access | `true` |
| `min_instances` | Minimum instances | `0` |
| `max_instances` | Maximum instances | `10` |
| `cpu_limit` | CPU limit | `1000m` |
| `memory_limit` | Memory limit | `512Mi` |

### Backend Configuration (Optional)

For production, use GCS for Terraform state:

```bash
# Create a GCS bucket for state
gsutil mb gs://your-terraform-state-bucket

# Configure backend
cp backend.tf.example backend.tf
# Edit backend.tf with your bucket name

# Reinitialize Terraform
terraform init
```

## Deployment Workflow

### Option 1: Two-Step Deployment (Recommended for First Deploy)

1. **Create Artifact Registry first:**
   ```bash
   terraform apply -target=google_artifact_registry_repository.app_repo
   ```

2. **Build and push Docker image** (see step 4 above)

3. **Deploy remaining infrastructure:**
   ```bash
   terraform apply
   ```

### Option 2: Update Image After Infrastructure

1. **Deploy all infrastructure:**
   ```bash
   terraform apply
   ```

2. **Build and push Docker image**

3. **Force Cloud Run to redeploy:**
   ```bash
   gcloud run services update flask-crud-app \
     --region us-central1 \
     --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/flask-crud-app-repo/flask-app:latest
   ```

## Updating the Application

To update the application after making code changes:

```bash
# Build new image
cd app
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/flask-crud-app-repo/flask-app:latest .

# Push to registry
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/flask-crud-app-repo/flask-app:latest

# Update Cloud Run service
gcloud run services update flask-crud-app \
  --region ${REGION} \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/flask-crud-app-repo/flask-app:latest
```

## Destroying Resources

To tear down all infrastructure:

```bash
terraform destroy
```

**Warning**: This will delete all data in Firestore. Back up data before destroying.

## Security Considerations

- Secrets are automatically generated and stored in Secret Manager
- Service account follows principle of least privilege
- For production:
  - Set `allow_unauthenticated = false`
  - Use Cloud Identity-Aware Proxy (IAP) or Firebase Auth
  - Enable VPC Service Controls
  - Use GCS backend for Terraform state
  - Enable audit logging

## Troubleshooting

### API Not Enabled Error

If you get API not enabled errors, manually enable them:

```bash
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Docker Push Permission Denied

Ensure you're authenticated:

```bash
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

### Firestore Already Exists Error

If Firestore database already exists in your project, import it:

```bash
terraform import google_firestore_database.database "(default)"
```

## Outputs

After successful deployment, useful outputs include:

- `cloud_run_url`: Application URL
- `artifact_registry_repository`: Docker repository URL
- `docker_image_url`: Full image path
- `service_account_email`: Service account used by Cloud Run

View outputs:

```bash
terraform output
```
