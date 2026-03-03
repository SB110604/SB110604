/* ===================================================
   Er. Sahil Bodke – Portfolio JavaScript
   =================================================== */

'use strict';

// ---- Typed text animation ----
const TYPED_STRINGS = [
  'AI & ML Engineer',
  'Data Science Enthusiast',
  'Cloud Computing',
  'Computer Vision',
  'Final-Year CS Student',
];

let typedIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeWriter() {
  const el = document.getElementById('typed-text');
  if (!el) return;

  const current = TYPED_STRINGS[typedIndex];

  if (isDeleting) {
    el.textContent = current.slice(0, --charIndex);
  } else {
    el.textContent = current.slice(0, ++charIndex);
  }

  let delay = isDeleting ? 60 : 100;

  if (!isDeleting && charIndex === current.length) {
    delay = 2000;
    isDeleting = true;
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false;
    typedIndex = (typedIndex + 1) % TYPED_STRINGS.length;
    delay = 400;
  }

  setTimeout(typeWriter, delay);
}

// ---- Navbar scroll behaviour ----
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const backToTop = document.getElementById('back-to-top');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    if (window.scrollY > 400) {
      backToTop.classList.add('visible');
    } else {
      backToTop.classList.remove('visible');
    }

    highlightNavLink();
  }, { passive: true });

  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ---- Active nav link on scroll ----
function highlightNavLink() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');
  let current = '';

  sections.forEach(section => {
    const top = section.getBoundingClientRect().top;
    if (top <= 120) current = section.getAttribute('id');
  });

  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === '#' + current) {
      link.classList.add('active');
    }
  });
}

// ---- Hamburger menu ----
function initHamburger() {
  const hamburger = document.getElementById('hamburger');
  const navMenu = document.getElementById('nav-menu');

  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', navMenu.classList.contains('open'));
  });

  // Close on nav link click
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      navMenu.classList.remove('open');
    });
  });

  // Close on outside click only when menu is open
  document.addEventListener('click', (e) => {
    if (navMenu.classList.contains('open') &&
        !hamburger.contains(e.target) && !navMenu.contains(e.target)) {
      hamburger.classList.remove('active');
      navMenu.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  });
}

// ---- Intersection Observer fade-in ----
function initFadeIn() {
  const elements = document.querySelectorAll(
    '.info-card, .skill-category, .project-card, .contact-item, .about-info, .about-cards, .contact-info, .contact-form-wrapper'
  );

  elements.forEach(el => el.classList.add('fade-in'));

  elements.forEach((el, i) => el.setAttribute('data-fade-index', i));

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const delay = Number(entry.target.getAttribute('data-fade-index')) * 80;
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, delay);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  elements.forEach(el => observer.observe(el));
}

// ---- Profile image fallback ----
function initProfileImage() {
  const img = document.getElementById('profile-photo');
  const placeholder = document.getElementById('profile-placeholder');
  if (!img) return;

  img.onload = () => {
    img.classList.add('loaded');
    if (placeholder) placeholder.style.display = 'none';
  };

  img.onerror = () => {
    img.style.display = 'none';
    if (placeholder) placeholder.style.display = 'flex';
  };

  // Trigger if already cached
  if (img.complete && img.naturalWidth) {
    img.classList.add('loaded');
    if (placeholder) placeholder.style.display = 'none';
  }
}

// ---- Contact form ----
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    if (!validateForm(form)) return;

    const name    = form.name.value.trim();
    const email   = form.email.value.trim();
    const subject = form.subject.value.trim() || 'Portfolio Contact';
    const message = form.message.value.trim();

    const body = encodeURIComponent(
      `Hi Sahil,\n\nMy name is ${name}.\n\n${message}\n\nBest regards,\n${name}\n${email}`
    );
    const mailtoLink = `mailto:sahilbodke51@gmail.com?subject=${encodeURIComponent(subject)}&body=${body}`;

    // Show brief success feedback before opening mailto
    const submitBtn  = document.getElementById('submit-btn');
    const btnText    = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    const successMsg = document.getElementById('form-success');

    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    submitBtn.disabled = true;

    setTimeout(() => {
      window.location.href = mailtoLink;

      btnText.style.display = 'inline-flex';
      btnLoading.style.display = 'none';
      submitBtn.disabled = false;
      successMsg.style.display = 'block';
      form.reset();

      setTimeout(() => { successMsg.style.display = 'none'; }, 6000);
    }, 800);
  });

  // Live validation
  ['name', 'email', 'message'].forEach(field => {
    const el = form[field];
    if (el) {
      el.addEventListener('blur', () => validateField(el));
      el.addEventListener('input', () => {
        el.classList.remove('error');
        const errEl = document.getElementById(field + '-error');
        if (errEl) errEl.textContent = '';
      });
    }
  });
}

function validateForm(form) {
  let valid = true;
  ['name', 'email', 'message'].forEach(field => {
    if (!validateField(form[field])) valid = false;
  });
  return valid;
}

function validateField(el) {
  const errEl = document.getElementById(el.name + '-error');
  let msg = '';

  if (!el.value.trim()) {
    msg = 'This field is required.';
  } else if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}$/.test(el.value)) {
    msg = 'Please enter a valid email address.';
  }

  if (msg) {
    el.classList.add('error');
    if (errEl) errEl.textContent = msg;
    return false;
  }

  el.classList.remove('error');
  if (errEl) errEl.textContent = '';
  return true;
}

// ---- Year in footer ----
function setYear() {
  const el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
}

// ---- Smooth scroll for anchor links ----
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
}

// ---- Init ----
document.addEventListener('DOMContentLoaded', () => {
  typeWriter();
  initNavbar();
  initHamburger();
  initFadeIn();
  initProfileImage();
  initContactForm();
  initSmoothScroll();
  setYear();
});
