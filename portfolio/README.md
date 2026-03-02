# Sahil Bodke — Personal Portfolio Website

A responsive personal portfolio/resume website built with **HTML5, CSS3, and JavaScript**, deployed publicly on **GitHub Pages** (free, no login required).

## 🌐 Live Site

**👉 Visit: [https://sb110604.github.io/SB110604/](https://sb110604.github.io/SB110604/)**

> **Domain:** `sb110604.github.io` — a free subdomain provided by **GitHub Pages**.
> The full URL is `https://sb110604.github.io/SB110604/` (repository name is the path segment).

The site deploys automatically every time code is pushed to the `main`/`master` branch via the GitHub Actions workflow at `.github/workflows/deploy-pages.yml`.

### Enable GitHub Pages (one-time setup)
1. Go to your repository on GitHub: **Settings → Pages**
2. Under **Source**, select **GitHub Actions**
3. Push to `main`/`master` — the workflow deploys automatically
4. Your site will be live at `https://sb110604.github.io/SB110604/`

## ✨ Features

- **Hero section** — Name, title, and social links
- **Live search** — Search across skills, projects, education, and contact info
- **Skills / Tech Stack** — Filterable grid of all technologies
- **Education timeline** — Academic background
- **Projects showcase** — Cards with tech tags and status
- **Contact section** — All social links in one place
- **Responsive design** — Works on mobile, tablet, and desktop
- **Smooth animations** — Scroll-triggered fade-in effects

## 📁 Files

| File | Description |
|------|-------------|
| `index.html` | Main portfolio page |
| `style.css` | All styles (dark theme, responsive) |
| `script.js` | Search, filters, navbar, animations |
| `firebase.json` | Firebase Hosting configuration |
| `.firebaserc` | Firebase project reference |

## 🚀 Deploy to Google Firebase Hosting

### Prerequisites
- A Google account
- [Node.js](https://nodejs.org/) installed

### Steps

1. **Install Firebase CLI**
   ```bash
   npm install -g firebase-tools
   ```

2. **Login to Firebase**
   ```bash
   firebase login
   ```

3. **Create a Firebase project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add project" → follow the steps
   - Copy your **Project ID**

4. **Update `.firebaserc`**
   - Replace `YOUR_FIREBASE_PROJECT_ID` with your actual project ID

5. **Deploy from the `portfolio/` folder**
   ```bash
   cd portfolio
   firebase deploy --only hosting
   ```

6. **Your site is live!**
   - URL: `https://YOUR_PROJECT_ID.web.app`
   - Also available at: `https://YOUR_PROJECT_ID.firebaseapp.com`

### Re-deploy after changes
```bash
firebase deploy --only hosting
```

## 🛠️ Local Development

Simply open `index.html` in any browser — no build step needed.

Or use a local server:
```bash
# Python
python -m http.server 3000

# Node.js
npx serve .
```

Then open `http://localhost:3000` in your browser.

## 📝 Customization

To update your information, edit `index.html`:
- Update name, bio, and social links in the **Hero** and **Contact** sections
- Add/remove skills in the **Tech Stack** section
- Add projects in the **Projects** section
- Update education timeline entries

---

**Sahil Bodke** | [GitHub](https://github.com/SB110604) | [Email](mailto:sahilbodke51@gmail.com)
