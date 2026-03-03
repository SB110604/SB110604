# Deployment Guide – Er. Sahil Bodke Portfolio

This document explains how the portfolio is deployed to **Google Firebase Hosting** and how to connect a custom domain.

> ✅ **Firebase already connected** – you have already run `firebase init hosting` and set the public directory to `public`. The steps below pick up from there.

---

## Folder Structure

```
SB110604/                  ← GitHub repository root
├── public/                ← Firebase public directory (all site files live here)
│   ├── index.html
│   ├── css/styles.css
│   ├── js/script.js
│   └── assets/
│       ├── resume.pdf
│       └── images/profile.jpg
├── firebase.json          ← Firebase Hosting config
├── .firebaserc            ← Firebase project alias ("portfolio")
└── .github/workflows/
    └── firebase-deploy.yml
```

---

## Step 1 – Verify Local Firebase Setup

Make sure your local `firebase.json` points to `public`:

```json
{
  "hosting": {
    "public": "public",
    ...
  }
}
```

And `.firebaserc` uses your project:

```json
{
  "projects": {
    "default": "portfolio"
  }
}
```

---

## Step 2 – Deploy Manually from PowerShell / Terminal

```powershell
# Navigate to the repo root (where firebase.json lives)
cd C:\path\to\SB110604

# Deploy to Firebase Hosting
firebase deploy --only hosting
```

After a successful deploy you will see:

```
✔  Deploy complete!

Project Console: https://console.firebase.google.com/project/portfolio/overview
Hosting URL:     https://portfolio.web.app
```

---

## Step 3 – Set Up GitHub Actions (Automatic Deployment)

Every push to `main` or `master` will automatically re-deploy the site.

### 3.1 Generate a Firebase Service Account key

1. Open [Firebase Console](https://console.firebase.google.com/)
2. Select your **portfolio** project
3. Click the ⚙ gear icon → **Project Settings**
4. Go to the **Service accounts** tab
5. Click **Generate new private key** → **Generate key**
6. A JSON file is downloaded — keep it safe, **do not commit it**

### 3.2 Add the secret to GitHub

1. In your GitHub repo, go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. **Name:** `FIREBASE_SERVICE_ACCOUNT`
4. **Value:** paste the entire contents of the downloaded JSON key file
5. Click **Add secret**

### 3.3 Merge / push to main

```bash
git add .
git commit -m "Update portfolio"
git push origin main
```

The workflow (`.github/workflows/firebase-deploy.yml`) will trigger and deploy automatically. Monitor progress under the **Actions** tab in GitHub.

---

## Step 4 – Connect a Custom Domain

### 4.1 Add the domain in Firebase Console

1. Open [Firebase Console](https://console.firebase.google.com/)
2. Select project **portfolio**
3. Left sidebar → **Build → Hosting**
4. Click **Add custom domain**
5. Enter your domain, e.g. `www.er.sahilbodke.com`
6. Click **Continue**

### 4.2 Verify domain ownership

Firebase shows a **TXT record**. Add it at your DNS registrar (GoDaddy, Namecheap, etc.):

| Type | Name / Host | Value             |
|------|-------------|-------------------|
| TXT  | `@`         | `firebase=<token>` (provided by Firebase) |

Click **Verify** in Firebase Console after a few minutes.

### 4.3 Point DNS to Firebase

Firebase then provides **A records**. Add them at your registrar:

| Type  | Name  | Value                                     |
|-------|-------|-------------------------------------------|
| A     | `@`   | (IP address 1 shown in Firebase Console)  |
| A     | `@`   | (IP address 2 shown in Firebase Console)  |
| CNAME | `www` | `portfolio.web.app.`                      |

> ⚠️ Use the exact IPs shown in **your** Firebase Console — do not copy examples.

### 4.4 Wait for SSL

- DNS propagation: **15 min – 48 hours**
- Firebase auto-provisions a free SSL certificate (Let's Encrypt)
- Site goes live at `https://www.er.sahilbodke.com` ✅

---

## Step 5 – Add Your Real Resume

```powershell
# Replace the placeholder
Copy-Item "C:\path\to\your\resume.pdf" "public\assets\resume.pdf"

git add public/assets/resume.pdf
git commit -m "Add real resume"
git push
```

---

## Step 6 – Update Site Content

All content is in `public/index.html`. Key placeholders:

| What to update      | Search for                          |
|---------------------|-------------------------------------|
| Profile photo       | Replace `public/assets/images/profile.jpg` |
| LinkedIn URL        | `linkedin.com/in/SahilBodke`        |
| GitHub URL          | `github.com/SB110604`               |
| Email               | `sahilbodke51@gmail.com`            |
| Projects section    | `id="projects"` in index.html       |
| About / bio         | `id="about"` in index.html          |
| Colour scheme       | CSS variables at top of `public/css/styles.css` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `firebase: command not found` | Run `npm install -g firebase-tools` |
| `Error: Permission denied` | Run `firebase login` again |
| `Project not found` | Check `.firebaserc` — project ID must match Firebase Console |
| DNS not propagating | Use [dnschecker.org](https://dnschecker.org) to check globally |
| SSL certificate pending | Wait up to 24 h after DNS fully propagates |
| GitHub Actions failing | Check Actions tab logs; confirm `FIREBASE_SERVICE_ACCOUNT` secret is set |

---

## Useful Links

- [Firebase Hosting docs](https://firebase.google.com/docs/hosting)
- [Firebase CLI reference](https://firebase.google.com/docs/cli)
- [Custom domain setup](https://firebase.google.com/docs/hosting/custom-domain)
- [GitHub Actions for Firebase](https://github.com/FirebaseExtended/action-hosting-deploy)
- [Free domain options (Freenom)](https://www.freenom.com)
- [Buy a domain (Namecheap)](https://www.namecheap.com)
