# Deployment Guide – Sahil Bodke Portfolio

> **Your progress so far:**
> - ✅ Step 1 – Firebase project created and CLI connected (PowerShell)
> - ✅ Step 2 – `firebase deploy --only hosting` ran successfully
> - ✅ Step 3 – GitHub Actions CI/CD set up (`FIREBASE_SERVICE_ACCOUNT` secret added)
> - ⏳ Step 4 – Custom domain `www.sahilbodke.xyz` — **do this next** (see below)

---

## Folder Structure

```
SB110604/                  ← GitHub repository root
├── public/                ← Firebase public directory
│   ├── index.html
│   ├── css/styles.css
│   ├── js/script.js
│   └── assets/
│       ├── resume.pdf
│       └── images/profile.jpg
├── firebase.json
├── .firebaserc            ← project alias: "portfolio"
└── .github/workflows/
    └── firebase-deploy.yml
```

---

## Step 4 – Get a FREE `.xyz` Domain via GitHub Student Developer Pack

The GitHub Student Developer Pack gives you **1 free `.xyz` domain for 1 year** through Namecheap. Here is the exact process:

### 4.0 – Apply for GitHub Student Developer Pack (if not already done)

1. Go to **[https://education.github.com/pack](https://education.github.com/pack)**
2. Click **"Get student benefits"**
3. Sign in with your GitHub account
4. Fill in the form:
   - **School email** (e.g. your college `.edu` address) **or** upload a photo of your student ID / enrollment letter
   - Select your school name
5. Submit and wait for approval (usually **minutes to a few hours**)
6. You will receive an email from GitHub confirming you have the pack ✅

> If you already have the pack approved, skip to **4.1** below.

---

### 4.1 – Claim Your Free `.xyz` Domain on Namecheap

1. Visit **[https://education.github.com/pack/offers](https://education.github.com/pack/offers)**
2. Search for **"Namecheap"** and click **"Get access"** (you must be signed in to GitHub)
3. You will be redirected to Namecheap with a special link
4. In the Namecheap search bar, type: `sahilbodke.xyz`
5. If it is available, click **"Add to cart"**
6. At checkout the price will show as **$0.00** (free for 1 year) ✅
7. Complete the order — create a Namecheap account if you don't have one
8. You now own **sahilbodke.xyz** for 1 year at no cost 🎉

> **Note:** The free `.xyz` offer gives you the domain for 1 year. After that, renewal costs ~$1–2/year. There are no hidden fees.

---

### 4.2 – Add the Domain to Firebase Hosting

1. Open **[https://console.firebase.google.com/](https://console.firebase.google.com/)**
2. Select your **portfolio** project
3. In the left sidebar: **Build → Hosting**
4. Click **"Add custom domain"**
5. Enter: `sahilbodke.xyz` → click **Continue**
6. Repeat the same steps and also add: `www.sahilbodke.xyz` → click **Continue**

Firebase will show you:
- A **TXT record** to prove domain ownership
- **A records** (two IP addresses) to point the domain at Firebase

Copy these values — you will need them in Step 4.3.

---

### 4.3 – Configure DNS on Namecheap

1. Log in to **[https://www.namecheap.com](https://www.namecheap.com)**
2. Click **Domain List** in the left sidebar
3. Click **Manage** next to `sahilbodke.xyz`
4. Click the **"Advanced DNS"** tab

Add the following records (exact values come from your Firebase Console):

#### Verification TXT record (add first, then click Verify in Firebase)

| Type | Host | Value                          | TTL        |
|------|------|--------------------------------|------------|
| TXT  | `@`  | `firebase=XXXXXXXXXXXXXXXXXXXX` | Automatic  |

> Replace `XXXXXXXXXXXXXXXXXXXX` with the token Firebase shows you.

#### A records (point the root domain to Firebase)

| Type | Host | Value           | TTL       |
|------|------|-----------------|-----------|
| A    | `@`  | `151.101.1.195` | Automatic |
| A    | `@`  | `151.101.65.195`| Automatic |

> ⚠️ **Use the exact IP addresses shown in your Firebase Console** — do not copy the examples above. Firebase assigns different IPs per project.

#### CNAME record (point `www` subdomain to Firebase)

| Type  | Host  | Value                  | TTL       |
|-------|-------|------------------------|-----------|
| CNAME | `www` | `portfolio.web.app.`   | Automatic |

> Make sure to include the trailing dot after `portfolio.web.app.`

5. Click **Save all changes** in Namecheap

---

### 4.4 – Verify and Wait for SSL

1. Go back to **Firebase Console → Build → Hosting**
2. Click **Verify** next to `sahilbodke.xyz` (after adding the TXT record)
3. Once verified, Firebase will start provisioning a free **SSL certificate**

| What to expect | Timeline |
|----------------|----------|
| TXT verification | Instant – 30 min |
| DNS propagation | 15 min – 48 hours |
| SSL certificate issued | Within 24 hours of DNS propagating |

4. Once complete, your site will be live at:
   - **https://www.sahilbodke.xyz** ✅
   - **https://sahilbodke.xyz** ✅ (redirects to www)

Check DNS propagation globally at **[https://dnschecker.org](https://dnschecker.org)** — enter `sahilbodke.xyz` and check the A record.

---

## Step 5 – Add Your Real Resume & Profile Photo

```powershell
# Replace placeholder resume
Copy-Item "C:\path\to\your\resume.pdf" "public\assets\resume.pdf"

# Replace placeholder photo (must be a square JPG, ideally 400×400px or larger)
Copy-Item "C:\path\to\your\photo.jpg" "public\assets\images\profile.jpg"

git add public/assets/
git commit -m "Add real resume and profile photo"
git push origin main
```

The GitHub Actions workflow will auto-deploy within ~1 minute.

---

## Step 6 – Update Site Content

All content is in `public/index.html`. Key placeholders to personalise:

| What to update   | Search for in index.html               |
|------------------|----------------------------------------|
| Profile photo    | Replace `public/assets/images/profile.jpg` |
| Resume           | Replace `public/assets/resume.pdf`    |
| Bio / About text | `id="about"` section                  |
| Projects         | `id="projects"` section               |
| LinkedIn URL     | `linkedin.com/in/SahilBodke`          |
| GitHub URL       | `github.com/SB110604`                 |
| Email            | `sahilbodke51@gmail.com`              |
| Colour scheme    | CSS variables at top of `public/css/styles.css` |

---

## Quick Reference – Useful URLs

| Resource | URL |
|----------|-----|
| Your live site | https://www.sahilbodke.xyz |
| Firebase Console | https://console.firebase.google.com/ |
| GitHub Actions | https://github.com/SB110604/SB110604/actions |
| GitHub Student Pack | https://education.github.com/pack |
| Namecheap login | https://www.namecheap.com |
| DNS checker | https://dnschecker.org |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `firebase: command not found` | Run `npm install -g firebase-tools` in PowerShell |
| `Error: Permission denied` | Run `firebase login` again |
| `Project not found` | Check `.firebaserc` — project ID must match Firebase Console |
| TXT verify fails | Wait 5–10 min for DNS to propagate, then click Verify again |
| DNS not propagating | Use [dnschecker.org](https://dnschecker.org) to check globally |
| SSL certificate pending | Wait up to 24 h after DNS fully propagates |
| GitHub Actions failing | Check Actions tab; confirm `FIREBASE_SERVICE_ACCOUNT` secret is set |
| Namecheap "conflicting records" | Delete any default Namecheap parking A/CNAME records first |

---

## Reference Docs

- [Firebase Hosting docs](https://firebase.google.com/docs/hosting)
- [Firebase CLI reference](https://firebase.google.com/docs/cli)
- [Firebase custom domain setup](https://firebase.google.com/docs/hosting/custom-domain)
- [GitHub Actions for Firebase](https://github.com/FirebaseExtended/action-hosting-deploy)
- [GitHub Student Developer Pack](https://education.github.com/pack)
- [Namecheap Advanced DNS help](https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/how-can-i-set-up-an-a-address-record-for-my-domain/)
