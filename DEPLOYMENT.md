# Vertex Experience - Contact Form Deployment Guide

This guide explains how to deploy the PHP contact form backend to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account**: Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud SDK**: Install from [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install)
3. **Docker**: Install from [docker.com](https://www.docker.com/get-started)
4. **SMTP Credentials**: Gmail, SendGrid, or any SMTP service

## Initial Setup

### 1. Install Google Cloud SDK

```bash
# macOS
brew install google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

### 2. Authenticate with Google Cloud

```bash
gcloud auth login
gcloud auth application-default login
```

### 3. Create or Select a Project

```bash
# List existing projects
gcloud projects list

# Create a new project (optional)
gcloud projects create vertex-contact-form --name="Vertex Contact Form"

# Set the project
gcloud config set project YOUR_PROJECT_ID
```

### 4. Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## Email Configuration

### Option 1: Gmail (Recommended for Testing)

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Generate an App Password at [App Passwords](https://myaccount.google.com/apppasswords)
4. Use these credentials:
   - SMTP_HOST: `smtp.gmail.com`
   - SMTP_PORT: `587`
   - SMTP_USERNAME: `your-email@gmail.com`
   - SMTP_PASSWORD: `your-app-password`

### Option 2: SendGrid

1. Sign up at [sendgrid.com](https://sendgrid.com)
2. Create an API key
3. Use these credentials:
   - SMTP_HOST: `smtp.sendgrid.net`
   - SMTP_PORT: `587`
   - SMTP_USERNAME: `apikey`
   - SMTP_PASSWORD: `your-sendgrid-api-key`

## Deployment Methods

### Method 1: Manual Deployment (Recommended for First Time)

#### Step 1: Build the Docker Image

```bash
cd /Users/noman/Downloads/vertex

# Build the image
docker build -t gcr.io/YOUR_PROJECT_ID/vertex-contact-form:latest .
```

#### Step 2: Push to Google Container Registry

```bash
# Configure Docker to use gcloud credentials
gcloud auth configure-docker

# Push the image
docker push gcr.io/YOUR_PROJECT_ID/vertex-contact-form:latest
```

#### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy vertex-contact-form \
  --image gcr.io/YOUR_PROJECT_ID/vertex-contact-form:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "SMTP_HOST=smtp.gmail.com,SMTP_PORT=587,SMTP_USERNAME=your-email@gmail.com,SMTP_PASSWORD=your-app-password,RECIPIENT_EMAIL=recipient@vertexexperience.com,REDIRECT_URL=https://vertexexperience.com/thank-you"
```

**Important**: Replace the environment variables with your actual values.

#### Step 4: Get the Service URL

```bash
gcloud run services describe vertex-contact-form \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

The output will be your Cloud Run service URL (e.g., `https://vertex-contact-form-xxxxx-uc.a.run.app`)

### Method 2: Automated Deployment with Cloud Build

#### Step 1: Set Substitution Variables

```bash
gcloud builds submit \
  --config cloudbuild.yaml \
  --substitutions _SMTP_HOST="smtp.gmail.com",_SMTP_PORT="587",_SMTP_USERNAME="your-email@gmail.com",_SMTP_PASSWORD="your-app-password",_RECIPIENT_EMAIL="recipient@vertexexperience.com",_REDIRECT_URL="https://vertexexperience.com/thank-you"
```

## Update the HTML Form

After deployment, update `free-audit.html` to use your Cloud Run service URL:

1. Get your service URL from the deployment output
2. Update the form action in `free-audit.html` (around line 994):

```html
<form id="wf-form-Audit-Form" 
      name="wf-form-Audit-Form" 
      data-name="Audit Form" 
      method="POST"
      action="https://YOUR-CLOUD-RUN-URL/contact-form-handler.php"
      class="form_component">
```

## Testing

### Test Locally with Docker

```bash
# Build the image
docker build -t vertex-contact-form:test .

# Run locally
docker run -p 8080:8080 \
  -e SMTP_HOST=smtp.gmail.com \
  -e SMTP_PORT=587 \
  -e SMTP_USERNAME=your-email@gmail.com \
  -e SMTP_PASSWORD=your-app-password \
  -e RECIPIENT_EMAIL=recipient@vertexexperience.com \
  -e REDIRECT_URL=https://vertexexperience.com/thank-you \
  vertex-contact-form:test

# Test the endpoint
curl -X POST http://localhost:8080/contact-form-handler.php \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "Website-Link": "https://example.com",
    "message": "This is a test message",
    "Privacy-Policy": "on"
  }'
```

### Test on Cloud Run

```bash
# Get your service URL
SERVICE_URL=$(gcloud run services describe vertex-contact-form \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

# Test the endpoint
curl -X POST $SERVICE_URL/contact-form-handler.php \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "Website-Link": "https://example.com",
    "message": "This is a test message",
    "Privacy-Policy": "on"
  }'
```

## Monitoring and Logs

### View Logs

```bash
# View recent logs
gcloud run services logs read vertex-contact-form \
  --platform managed \
  --region us-central1 \
  --limit 50

# Stream logs in real-time
gcloud run services logs tail vertex-contact-form \
  --platform managed \
  --region us-central1
```

### View Metrics

Visit the [Cloud Run Console](https://console.cloud.google.com/run) to view:
- Request count
- Request latency
- Container instance count
- Error rate

## Updating Environment Variables

```bash
gcloud run services update vertex-contact-form \
  --platform managed \
  --region us-central1 \
  --update-env-vars "SMTP_HOST=new-smtp-host.com,RECIPIENT_EMAIL=new-recipient@example.com"
```

## Troubleshooting

### Issue: Email not sending

**Check logs:**
```bash
gcloud run services logs read vertex-contact-form --limit 50
```

**Common causes:**
- Incorrect SMTP credentials
- Gmail blocking "less secure apps" (use App Password)
- Firewall blocking SMTP port 587

### Issue: CORS errors

The PHP handler includes CORS headers by default. If you still see CORS errors:
1. Check that the form is making requests to the correct URL
2. Verify the Cloud Run service allows unauthenticated requests

### Issue: 500 Internal Server Error

**Check environment variables:**
```bash
gcloud run services describe vertex-contact-form \
  --platform managed \
  --region us-central1 \
  --format 'value(spec.template.spec.containers[0].env)'
```

Ensure all required variables are set:
- SMTP_HOST
- SMTP_PORT
- SMTP_USERNAME
- SMTP_PASSWORD
- RECIPIENT_EMAIL

## Cost Estimation

Cloud Run pricing (as of 2024):
- **Free tier**: 2 million requests/month
- **After free tier**: $0.40 per million requests
- **Memory**: $0.0000025 per GB-second
- **CPU**: $0.00002400 per vCPU-second

For a typical contact form with ~100 submissions/month, costs will be **$0.00** (within free tier).

## Security Best Practices

1. **Never commit credentials**: Keep `.env` in `.gitignore`
2. **Use App Passwords**: For Gmail, use App Passwords instead of account passwords
3. **Rotate credentials**: Regularly update SMTP passwords
4. **Monitor logs**: Check for suspicious activity
5. **Rate limiting**: Consider adding rate limiting for production use

## Next Steps

1. Deploy the service to Cloud Run
2. Update `free-audit.html` with the Cloud Run URL
3. Test the form submission
4. Monitor logs for any issues
5. Set up alerts for errors (optional)

## Support

For issues or questions:
- Check [Cloud Run Documentation](https://cloud.google.com/run/docs)
- Review logs with `gcloud run services logs read`
- Contact Google Cloud Support
