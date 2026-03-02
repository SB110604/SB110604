/* ===== NAVBAR SCROLL EFFECT ===== */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 20);
});

/* ===== HAMBURGER MENU ===== */
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

/* ===== SKILLS FILTER ===== */
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    document.querySelectorAll('#skillsGrid .skill-card').forEach(card => {
      card.classList.toggle('hidden', filter !== 'all' && card.dataset.category !== filter);
    });
  });
});

/* ===== SEARCH FUNCTIONALITY ===== */
const searchInput = document.getElementById('searchInput');
const searchClear = document.getElementById('searchClear');
const searchResultsEl = document.getElementById('searchResults');

// Build search index from all .searchable elements
const buildIndex = () => {
  return Array.from(document.querySelectorAll('.searchable')).map(el => {
    const h3 = el.querySelector('h3, span');
    const p = el.querySelector('p');
    return {
      el,
      title: h3 ? h3.textContent.trim() : el.textContent.trim().slice(0, 50),
      body: p ? p.textContent.trim() : '',
      tags: el.dataset.tags || '',
      category: el.dataset.category || '',
    };
  });
};

let searchIndex = [];
window.addEventListener('DOMContentLoaded', () => {
  searchIndex = buildIndex();
});

const categoryLabels = {
  languages: 'Language',
  frameworks: 'Framework',
  cloud: 'Cloud / DevOps',
  data: 'Data & ML',
  databases: 'Database',
  education: 'Education',
  projects: 'Project',
  contact: 'Contact',
};

const getSectionHref = (category, title) => {
  const sectionMap = {
    languages: '#skills',
    frameworks: '#skills',
    cloud: '#skills',
    data: '#skills',
    databases: '#skills',
    education: '#education',
    projects: '#projects',
    contact: '#contact',
  };
  return sectionMap[category] || '#';
};

searchInput.addEventListener('input', () => {
  const q = searchInput.value.trim().toLowerCase();
  searchClear.classList.toggle('visible', q.length > 0);
  searchResultsEl.innerHTML = '';

  if (q.length < 2) return;

  const matches = searchIndex.filter(item => {
    const haystack = `${item.title} ${item.body} ${item.tags} ${item.category}`.toLowerCase();
    return haystack.includes(q);
  }).slice(0, 8);

  if (matches.length === 0) {
    searchResultsEl.innerHTML = `<p class="search-no-results">No results found for "<strong>${escapeHtml(q)}</strong>"</p>`;
    return;
  }

  matches.forEach(item => {
    const a = document.createElement('a');
    a.className = 'search-result-item';
    a.href = getSectionHref(item.category, item.title);
    const label = categoryLabels[item.category] || item.category;
    a.innerHTML = `
      <span class="result-label">${escapeHtml(label)}</span>
      <span>${highlightMatch(escapeHtml(item.title), q)}</span>
    `;
    a.addEventListener('click', () => {
      searchResultsEl.innerHTML = '';
      searchInput.value = '';
      searchClear.classList.remove('visible');
    });
    searchResultsEl.appendChild(a);
  });
});

searchClear.addEventListener('click', () => {
  searchInput.value = '';
  searchClear.classList.remove('visible');
  searchResultsEl.innerHTML = '';
  searchInput.focus();
});

// Close search results when clicking outside
document.addEventListener('click', e => {
  if (!e.target.closest('.search-wrapper') && !e.target.closest('.search-results')) {
    searchResultsEl.innerHTML = '';
  }
});

/* ===== HELPERS ===== */
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function highlightMatch(text, query) {
  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  return text.replace(regex, '<mark>$1</mark>');
}

/* ===== ANIMATE ON SCROLL ===== */
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.skill-card, .project-card, .timeline-card, .contact-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
  observer.observe(el);
});
