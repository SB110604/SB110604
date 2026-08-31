# 🚀 Deploying Sahil Bodke's Portfolio on Google Cloud with Custom Domain

This guide covers **end-to-end deployment** of the FastAPI portfolio + Industrial Safety app on Google Cloud Platform (GCP) with a custom domain like `www.sahilbodke.com` or `www.er.sahilbodke.in`.

---

## 📋 Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Docker Desktop | latest | https://docs.docker.com/get-docker/ |
| Google Cloud SDK (`gcloud`) | latest | https://cloud.google.com/sdk/docs/install |
| Python | 3.11+ | https://python.org |
| Git | any | https://git-scm.com |

---

## Step 1 — Upload Your Resume PDF

Place your resume PDF inside the static folder before deploying:

```
BE_project_final/static/resume/Sahil_Bodke_Resume.pdf
```

The **Download Resume** button on the portfolio already points to `/static/resume/Sahil_Bodke_Resume.pdf`.

---

## Step 2 — Prepare the `.env` file

Copy the example and fill in your values:

```bash
cp BE_project_final/.env.example BE_project_final/.env
```

Key variables to set:

```dotenv
APP_ENV=production
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
DATABASE_URL=mysql+pymysql://user:pass@host:3306/safety_db
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_FROM_NUMBER=+1XXXXXXXXXX
TWILIO_TO_NUMBER=+91XXXXXXXXXX
ALLOWED_ORIGINS=https://www.yourdomain.com,https://yourdomain.com
```

> ⚠️ **Never commit `.env` to Git** — it is already in `.gitignore`.

---

## Step 3 — Build & Test the Docker Image Locally

```bash
cd BE_project_final

# Build
docker build -t sahilbodke-portfolio:latest .

# Run locally (port 8000)
docker run --env-file .env -p 8000:8000 sahilbodke-portfolio:latest
```

Open http://localhost:8000 — you should see the portfolio homepage.

---

## Step 4 — Create a GCP Project

```bash
# Login
gcloud auth login

# Create project (choose a unique ID)
gcloud projects create sahilbodke-portfolio --name="Sahil Bodke Portfolio"

# Set as active project
gcloud config set project sahilbodke-portfolio

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  domains.googleapis.com
```

---

## Step 5 — Push the Image to Google Artifact Registry

```bash
# Create a Docker repository in Artifact Registry
gcloud artifacts repositories create portfolio-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Portfolio Docker images"

# Authenticate Docker with GCP
gcloud auth configure-docker us-central1-docker.pkg.dev

# Tag and push
IMAGE=us-central1-docker.pkg.dev/sahilbodke-portfolio/portfolio-repo/app:latest
docker tag sahilbodke-portfolio:latest $IMAGE
docker push $IMAGE
```

---

## Step 6 — Deploy to Google Cloud Run

```bash
gcloud run deploy sahilbodke-portfolio \
  --image=us-central1-docker.pkg.dev/sahilbodke-portfolio/portfolio-repo/app:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8000 \
  --memory=512Mi \
  --cpu=1 \
  --set-env-vars="APP_ENV=production" \
  --set-secrets="SECRET_KEY=SECRET_KEY:latest,DATABASE_URL=DATABASE_URL:latest"
```

After deployment, GCP provides a URL like:
```
https://sahilbodke-portfolio-xxxxxxxxxx-uc.a.run.app
```

Test it in your browser to verify the portfolio loads.

---

## Step 7 — Register a Custom Domain

### Option A — Google Domains / Squarespace Domains
1. Go to https://domains.google.com
2. Search for `sahilbodke.com`, `er.sahilbodke.in`, etc.
3. Purchase the domain (typically $10–$15/year for `.com`).

### Option B — GoDaddy / Namecheap / any registrar
Same process — buy the domain, then configure DNS records as below.

---

## Step 8 — Map Domain to Cloud Run

```bash
# Verify domain ownership via Google Search Console first:
# https://search.google.com/search-console/welcome

# Map the domain
gcloud beta run domain-mappings create \
  --service=sahilbodke-portfolio \
  --domain=www.sahilbodke.com \
  --region=us-central1
```

GCP will provide DNS records (A / AAAA / CNAME). Add them in your domain registrar's DNS panel:

| Type  | Name | Value (example)                    |
|-------|------|------------------------------------|
| CNAME | www  | ghs.googlehosted.com               |
| A     | @    | 216.239.32.21 _(GCP provides this)_ |

SSL/TLS certificate is **automatically provisioned** by Google — no extra cost.

---

## Step 9 — Automated CI/CD with GitHub Actions (optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - uses: google-github-actions/setup-gcloud@v2

      - name: Build & Push Docker image
        run: |
          IMAGE=us-central1-docker.pkg.dev/sahilbodke-portfolio/portfolio-repo/app:${{ github.sha }}
          gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
          docker build -t $IMAGE ./BE_project_final
          docker push $IMAGE

      - name: Deploy to Cloud Run
        run: |
          IMAGE=us-central1-docker.pkg.dev/sahilbodke-portfolio/portfolio-repo/app:${{ github.sha }}
          gcloud run deploy sahilbodke-portfolio \
            --image=$IMAGE \
            --platform=managed \
            --region=us-central1 \
            --allow-unauthenticated
```

Add `GCP_SA_KEY` (JSON key of a service account) as a GitHub repository secret.

---

## Step 10 — Verify Everything

| URL | Expected |
|-----|----------|
| `https://www.sahilbodke.com/`           | 🏠 Portfolio homepage |
| `https://www.sahilbodke.com/portfolio`  | Same portfolio page |
| `https://www.sahilbodke.com/dashboard`  | Industrial Safety dashboard |
| `https://www.sahilbodke.com/docs`       | FastAPI Swagger UI |
| `https://www.sahilbodke.com/health`     | `{"status":"ok"}` |

---

## 💰 Estimated Monthly Cost

| Service | Free tier | Paid |
|---------|-----------|------|
| Cloud Run | 2M req/month free | ~$0–$5 |
| Artifact Registry | 0.5 GB free | negligible |
| Custom domain (annual) | — | $10–$15/year |
| **Total** | **~$0 for low traffic** | <$10/month |

---

## 🔒 Security Checklist

- [x] `.env` is in `.gitignore` — never committed
- [x] CORS restricted to production domain via `ALLOWED_ORIGINS`
- [x] JWT authentication on all sensitive API routes
- [x] Secrets stored in **Google Secret Manager**, not env vars
- [x] HTTPS enforced automatically via Cloud Run
- [ ] Add [Cloud Armor](https://cloud.google.com/armor) WAF for DDoS protection (optional)

---

## 📞 Support

- 📧 sahilbodke51@gmail.com
- 💼 https://linkedin.com/in/sahil-bodke
- 💻 https://github.com/SB110604
