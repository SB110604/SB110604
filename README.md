# Er. Sahil Bodke – Portfolio Website

[![Deploy to Firebase](https://github.com/SB110604/SB110604/actions/workflows/firebase-deploy.yml/badge.svg)](https://github.com/SB110604/SB110604/actions/workflows/firebase-deploy.yml)
[![Firebase Hosting](https://img.shields.io/badge/Hosted%20on-Firebase-FFCA28?logo=firebase&logoColor=white)](https://portfolio.web.app)

A modern, responsive portfolio website for **Er. Sahil Bodke** — Computer Science Engineer specialising in AI, ML, Data Science and Cloud Computing.

🌐 **Live site:** [https://www.sahilbodke.xyz](https://www.sahilbodke.xyz)

---

## ✨ Features

- **Fully responsive** – looks great on mobile, tablet and desktop
- **Dark theme** with purple accent palette
- **Typed text animation** in the hero section
- **Smooth scroll navigation** with active link highlighting
- **Intersection Observer** fade-in animations
- **Hamburger menu** for mobile
- **Contact form** that opens your default email client
- **Direct action buttons** – Resume download, LinkedIn, Email, GitHub
- **Firebase Hosting** with CI/CD via GitHub Actions
- **Security headers** (X-Frame-Options, X-Content-Type-Options, etc.)
- **SEO** and Open Graph meta tags

---

## 📁 Project Structure

```
SB110604/
├── public/                             # ← Firebase public directory
│   ├── index.html                      # Main portfolio page
│   ├── css/
│   │   └── styles.css                  # Complete responsive stylesheet
│   ├── js/
│   │   └── script.js                   # Interactivity & animations
│   └── assets/
│       ├── resume.pdf                  # Your CV (replace with your own)
│       └── images/
│           └── profile.jpg             # Profile photo (replace with your own)
├── firebase.json                       # Firebase Hosting configuration
├── .firebaserc                         # Firebase project alias ("portfolio")
├── .github/
│   └── workflows/
│       └── firebase-deploy.yml         # Auto-deploy on push to main/master
├── DEPLOYMENT.md                       # Step-by-step deployment guide
└── README.md                           # This file
```

---

## 🚀 Local Development

No build step needed — it's pure HTML/CSS/JS.

```bash
# Clone the repo
git clone https://github.com/SB110604/SB110604.git
cd SB110604

# Serve the public/ folder locally (any static server works)
npx serve public
# or
python -m http.server 8000 --directory public
# then open http://localhost:8000
```

---

## 🔧 Customising Content

All content lives in `public/index.html`. Key things to update:

| Item | Location |
|------|----------|
| Profile photo | Replace `public/assets/images/profile.jpg` |
| Resume | Replace `public/assets/resume.pdf` |
| Bio text | `#about` section |
| Projects | `#projects` section |
| LinkedIn URL | Search `linkedin.com/in/SahilBodke` |
| GitHub URL | Search `github.com/SB110604` |
| Email | Search `sahilbodke51@gmail.com` |
| Colour scheme | CSS variables at the top of `public/css/styles.css` |

---

## ☁️ Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for the full step-by-step guide covering:

1. ✅ Firebase already connected (you did this!)
2. Deploying manually (`firebase deploy --only hosting`)
3. Connecting the custom domain (`www.er.sahilbodke.com`)
4. Setting up GitHub Actions for automatic deployment on every push
5. Adding your real resume and profile photo

### Quick deploy (from repo root)

```powershell
firebase deploy --only hosting
```

---

## 🔒 Security

The `firebase.json` configuration applies the following HTTP security headers to every response:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- Long-lived cache headers for static assets

---

## 💫 About Me

🎓 Computer Science student · 🤖 AI & ML · 📊 Data Science · ☁️ Cloud · 🐍 Python · 👁️ Computer Vision · 🛠️ Final-year AI industrial safety project

## 🌐 Socials

[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?logo=Instagram&logoColor=white)](https://instagram.com/bodkesahil_11) [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/SahilBodke) [![email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white)](mailto:sahilbodke51@gmail.com)

## 💻 Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white) ![Firebase](https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) ![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)

## 📊 GitHub Stats

![](https://github-readme-stats.vercel.app/api?username=SB110604&theme=dark&hide_border=false&include_all_commits=false&count_private=false)<br/>
![](https://nirzak-streak-stats.vercel.app/?user=SB110604&theme=dark&hide_border=false)<br/>
![](https://github-readme-stats.vercel.app/api/top-langs/?username=SB110604&theme=dark&hide_border=false&include_all_commits=false&count_private=false&layout=compact)

---
[![](https://visitcount.itsvg.in/api?id=SB110604&icon=0&color=0)](https://visitcount.itsvg.in)

<!-- Proudly created with GPRM ( https://gprm.itsvg.in ) -->
