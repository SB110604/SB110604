# Deployment Guide – Er. Sahil Bodke Portfolio

This document contains step-by-step instructions for deploying the portfolio website to **Google Firebase Hosting** and connecting the custom domain **www.er.sahilbodke.com**.

---

## Prerequisites

- Node.js 18+ installed
- A Google account
- A registered domain (e.g., from GoDaddy, Namecheap, Google Domains)
- Git installed

---

## Step 1 – Create a Firebase Project

1. Go to [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. Click **Add Project**
3. Enter project name: `sahil-bodke-portfolio`
4. (Optional) Disable Google Analytics for a simple static site
5. Click **Create Project** and wait for it to be ready
6. Select the free **Spark** plan (sufficient for a portfolio site)

---

## Step 2 – Install the Firebase CLI

```bash
# Install globally
npm install -g firebase-tools

# Log in to your Google account
firebase login

# Verify the CLI is working
firebase --version
```

---

## Step 3 – Initialise Firebase Hosting (first-time setup)

> **Skip this step if you are using the pre-configured `firebase.json` and `.firebaserc` files already in the repository.**

```bash
cd /path/to/SB110604

# Initialise hosting (follow the prompts)
firebase init hosting
```

When prompted:
- **Which Firebase project?** → Select `sahil-bodke-portfolio`
- **Public directory?** → `.` (current directory / repo root)
- **Configure as single-page app?** → `Yes`
- **Overwrite `index.html`?** → `No`

---

## Step 4 – Deploy to Firebase

```bash
firebase deploy
```

After a successful deployment you will see:

```
✔  Deploy complete!

Project Console: https://console.firebase.google.com/project/sahil-bodke-portfolio/overview
Hosting URL:     https://sahil-bodke-portfolio.web.app
```

---

## Step 5 – Connect Custom Domain (www.er.sahilbodke.com)

### 5.1 Add the domain in Firebase Console

1. Open [Firebase Console](https://console.firebase.google.com/)
2. Select project **sahil-bodke-portfolio**
3. In the left sidebar go to **Build → Hosting**
4. Click **Add custom domain**
5. Enter: `www.er.sahilbodke.com`
6. Click **Continue**

### 5.2 Verify domain ownership

Firebase will show a **TXT record** for verification. Add it to your DNS registrar:

| Type | Name / Host | Value                |
|------|-------------|----------------------|
| TXT  | `@`         | `firebase=<token>`   |

Wait a few minutes, then click **Verify** in the Firebase Console.

### 5.3 Point DNS to Firebase

After verification, Firebase provides **A records** (two IP addresses). Add them to your DNS registrar:

| Type | Name / Host | Value (example)    |
|------|-------------|-------------------|
| A    | `@`         | `151.101.1.195`   |
| A    | `@`         | `151.101.65.195`  |

For the `www` subdomain, add a **CNAME**:

| Type  | Name  | Value                            |
|-------|-------|----------------------------------|
| CNAME | `www` | `sahil-bodke-portfolio.web.app.` |

> **Note:** The exact IP addresses are provided by Firebase. Use the values shown in the Firebase Console — do not copy the examples above.

### 5.4 Wait for SSL provisioning

- DNS propagation typically takes **15 minutes to 48 hours**
- Firebase automatically provisions a free **SSL certificate** (Let's Encrypt)
- Once active, your site will be available at `https://www.er.sahilbodke.com`

---

## Step 6 – Set Up GitHub Actions for Automatic Deployment

Every push to the `main` branch will automatically deploy to Firebase Hosting.

### 6.1 Generate a Firebase Service Account key

1. In [Firebase Console](https://console.firebase.google.com/), open project settings (⚙ gear icon)
2. Go to **Service accounts** tab
3. Click **Generate new private key** → **Generate key**
4. Save the downloaded JSON file securely (do not commit it to the repo)

### 6.2 Add the secret to GitHub

1. In your GitHub repository, go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `FIREBASE_SERVICE_ACCOUNT`
4. Value: paste the entire JSON content of the key file
5. Click **Add secret**

### 6.3 Push to main

The workflow (`.github/workflows/firebase-deploy.yml`) will trigger automatically:

```bash
git add .
git commit -m "Deploy portfolio"
git push origin main
```

Monitor the workflow under the **Actions** tab in GitHub.

---

## Step 7 – Add Your Resume

Replace the placeholder resume with your real CV:

```bash
# Copy your resume to the assets folder
cp /path/to/your/resume.pdf assets/resume.pdf

git add assets/resume.pdf
git commit -m "Add resume"
git push
```

---

## Step 8 – Update Content

All placeholder content is in `index.html`. Search for the following comments/placeholders and replace them:

| Item                | Where                     |
|---------------------|---------------------------|
| Profile photo       | `assets/images/profile.jpg` |
| LinkedIn URL        | Search `linkedin.com/in/SahilBodke` |
| GitHub URL          | Search `github.com/SB110604` |
| Email               | Search `sahilbodke51@gmail.com` |
| Project descriptions | `#projects` section in `index.html` |
| Bio text            | `#about` section in `index.html` |

---

## Troubleshooting

### "Permission denied" during `firebase deploy`
Run `firebase login` again to refresh your credentials.

### DNS not propagating
Use [https://dnschecker.org](https://dnschecker.org) to verify your DNS records globally.

### SSL certificate not issued
Ensure the A records and CNAME point to the correct Firebase IPs. Wait up to 24 hours after DNS is fully propagated.

### GitHub Actions failing
1. Check the **Actions** tab for error logs
2. Confirm the `FIREBASE_SERVICE_ACCOUNT` secret is correctly set
3. Ensure the `projectId` in `.github/workflows/firebase-deploy.yml` matches your Firebase project ID

---

## Useful Links

- [Firebase Hosting docs](https://firebase.google.com/docs/hosting)
- [Firebase CLI reference](https://firebase.google.com/docs/cli)
- [Custom domain setup](https://firebase.google.com/docs/hosting/custom-domain)
- [GitHub Actions for Firebase](https://github.com/FirebaseExtended/action-hosting-deploy)
