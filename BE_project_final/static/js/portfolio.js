/* ================================================================
   Portfolio — JavaScript: typed text, scroll reveal, nav, form
   ================================================================ */

// ---------- Typed-text effect ----------
(function () {
  const roles = [
    'AI & Machine Learning Engineer',
    'Computer Vision Developer',
    'Full-Stack Developer',
    'Data Scientist',
    'Cloud (GCP) Enthusiast',
  ];
  const el = document.getElementById('typed-text');
  if (!el) return;

  let roleIdx = 0, charIdx = 0, deleting = false;

  function tick() {
    const current = roles[roleIdx];
    if (!deleting) {
      el.textContent = current.slice(0, ++charIdx);
      if (charIdx === current.length) {
        deleting = true;
        setTimeout(tick, 1800);
        return;
      }
    } else {
      el.textContent = current.slice(0, --charIdx);
      if (charIdx === 0) {
        deleting = false;
        roleIdx = (roleIdx + 1) % roles.length;
      }
    }
    setTimeout(tick, deleting ? 55 : 80);
  }
  tick();
})();

// ---------- Scroll-reveal ----------
(function () {
  const items = document.querySelectorAll('.reveal');
  if (!items.length) return;

  const observer = new IntersectionObserver(
    (entries) => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } }),
    { threshold: 0.12 }
  );
  items.forEach(el => observer.observe(el));
})();

// ---------- Active nav link on scroll ----------
(function () {
  const sections = document.querySelectorAll('section[id]');
  const links    = document.querySelectorAll('.nav-links a[href^="#"]');
  if (!sections.length || !links.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          links.forEach(l => l.classList.remove('active'));
          const active = document.querySelector(`.nav-links a[href="#${e.target.id}"]`);
          if (active) active.classList.add('active');
        }
      });
    },
    { rootMargin: '-45% 0px -45% 0px' }
  );
  sections.forEach(s => observer.observe(s));
})();

// ---------- Mobile burger ----------
(function () {
  const burger = document.getElementById('burger');
  const navLinks = document.querySelector('.nav-links');
  if (!burger || !navLinks) return;
  burger.addEventListener('click', () => navLinks.classList.toggle('open'));
  document.querySelectorAll('.nav-links a').forEach(a =>
    a.addEventListener('click', () => navLinks.classList.remove('open'))
  );
})();

// ---------- Contact form (mailto fallback) ----------
(function () {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const name    = form.querySelector('#cf-name').value.trim();
    const email   = form.querySelector('#cf-email').value.trim();
    const subject = form.querySelector('#cf-subject').value.trim();
    const message = form.querySelector('#cf-message').value.trim();
    const msgEl   = document.getElementById('form-msg');

    if (!name || !email || !message) {
      msgEl.style.color = '#f85149';
      msgEl.textContent = 'Please fill in all required fields.';
      return;
    }

    // Build mailto link and open
    const body = encodeURIComponent(`Hi Sahil,\n\nMy name is ${name} (${email}).\n\n${message}`);
    const subj = encodeURIComponent(subject || `Portfolio enquiry from ${name}`);
    window.location.href = `mailto:sahilbodke51@gmail.com?subject=${subj}&body=${body}`;

    msgEl.style.color = '#3fb950';
    msgEl.textContent = '✅ Your email client should open now. Thank you!';
    form.reset();
  });
})();

// ---------- Animated counters ----------
(function () {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el  = entry.target;
        const end = parseInt(el.dataset.count, 10);
        let cur = 0;
        const step = Math.ceil(end / 40);
        const id = setInterval(() => {
          cur = Math.min(cur + step, end);
          el.textContent = cur + (el.dataset.suffix || '');
          if (cur >= end) clearInterval(id);
        }, 35);
        observer.unobserve(el);
      });
    },
    { threshold: 0.4 }
  );
  counters.forEach(el => observer.observe(el));
})();
