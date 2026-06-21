// ============================================
// Fares Amir Hassen — Personal Website JS
// Custom cursor + scroll reveal + mobile nav
// ============================================

document.addEventListener('DOMContentLoaded', () => {

  // --- Internationalization (i18n) ---
  initI18n();

  // --- Custom Cursor ---
  const dot = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');

  if (dot && ring && window.matchMedia('(pointer: fine)').matches) {
    document.body.classList.add('custom-cursor-active');
    let mouseX = 0, mouseY = 0;
    let ringX = 0, ringY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.left = mouseX + 'px';
      dot.style.top = mouseY + 'px';
    });

    // Smooth follow for ring
    function animateRing() {
      ringX += (mouseX - ringX) * 0.15;
      ringY += (mouseY - ringY) * 0.15;
      ring.style.left = ringX + 'px';
      ring.style.top = ringY + 'px';
      requestAnimationFrame(animateRing);
    }
    animateRing();

    // Hover effect on interactive elements
    const hoverTargets = document.querySelectorAll('a, button, .skill-card, .cert-item');
    hoverTargets.forEach(el => {
      el.addEventListener('mouseenter', () => {
        dot.classList.add('hover');
        ring.classList.add('hover');
      });
      el.addEventListener('mouseleave', () => {
        dot.classList.remove('hover');
        ring.classList.remove('hover');
      });
    });
  } else {
    // Hide cursor elements on touch devices
    if (dot) dot.style.display = 'none';
    if (ring) ring.style.display = 'none';
  }

  // --- Scroll Reveal (IntersectionObserver) ---
  const reveals = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -120px 0px' });

    reveals.forEach(el => observer.observe(el));
  } else {
    // Fallback: reveal everything immediately
    reveals.forEach(el => el.classList.add('visible'));
  }

  // --- Mobile Nav Toggle ---
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (toggle && navLinks) {
    const setMenu = (open) => {
      toggle.classList.toggle('active', open);
      navLinks.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
    };

    toggle.addEventListener('click', () => {
      setMenu(!navLinks.classList.contains('open'));
    });

    // Close menu on link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => setMenu(false));
    });

    // Close menu on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navLinks.classList.contains('open')) {
        setMenu(false);
        toggle.focus();
      }
    });
  }

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // --- Constellation Background Animation ---
  initConstellation();

});

// ============================================
// Constellation Lines — Network Topology Effect
// ============================================
function initConstellation() {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) return;

  const canvas = document.getElementById('constellation-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let stars = [];
  let animationId;

  // Configuration — visible but still subtle
  const STAR_COUNT = 60;
  const CONNECTION_DIST = 180;
  const STAR_RADIUS_MIN = 1.5;
  const STAR_RADIUS_MAX = 3;
  const SPEED = 0.25;
  const LINE_OPACITY_BASE = 0.25;

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }

  class Star {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * SPEED;
      this.vy = (Math.random() - 0.5) * SPEED;
      this.radius = STAR_RADIUS_MIN + Math.random() * (STAR_RADIUS_MAX - STAR_RADIUS_MIN);
      // Each star has a pulse cycle for fade in/out
      this.pulsePhase = Math.random() * Math.PI * 2;
      this.pulseSpeed = 0.005 + Math.random() * 0.01;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      // Wrap around edges
      if (this.x < -10) this.x = width + 10;
      if (this.x > width + 10) this.x = -10;
      if (this.y < -10) this.y = height + 10;
      if (this.y > height + 10) this.y = -10;

      // Pulse phase for fade effect
      this.pulsePhase += this.pulseSpeed;
    }

    draw() {
      const pulse = 0.3 + 0.7 * (0.5 + 0.5 * Math.sin(this.pulsePhase));
      // Glow effect — larger faint circle behind the dot
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius * 4, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 45, 45, ${pulse * 0.06})`;
      ctx.fill();
      // Main dot
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 45, 45, ${pulse * 0.6})`;
      ctx.fill();
    }
  }

  function init() {
    resize();
    stars = [];
    for (let i = 0; i < STAR_COUNT; i++) {
      stars.push(new Star());
    }
  }

  function drawConnections() {
    for (let i = 0; i < stars.length; i++) {
      for (let j = i + 1; j < stars.length; j++) {
        const dx = stars[i].x - stars[j].x;
        const dy = stars[i].y - stars[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < CONNECTION_DIST) {
          // Opacity based on distance — closer = more opaque
          const opacity = LINE_OPACITY_BASE * (1 - dist / CONNECTION_DIST);
          // Add a slow fade pulse to the line itself
          const linePulse = 0.5 + 0.5 * Math.sin((stars[i].pulsePhase + stars[j].pulsePhase) * 0.5);

          ctx.beginPath();
          ctx.moveTo(stars[i].x, stars[i].y);
          ctx.lineTo(stars[j].x, stars[j].y);
          ctx.strokeStyle = `rgba(255, 45, 45, ${opacity * linePulse})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    // Update and draw stars
    for (const star of stars) {
      star.update();
      star.draw();
    }

    // Draw connections between nearby stars
    drawConnections();

    animationId = requestAnimationFrame(animate);
  }

  init();
  animate();

  window.addEventListener('resize', () => {
    resize();
  });
}

// ============================================
// Internationalization — auto-detect + manual switch
// English is the default (text lives in the HTML).
// ============================================
function initI18n() {
  var SUPPORTED = ['en', 'fr', 'ar', 'ja'];
  var RTL = ['ar'];
  var STORAGE_KEY = 'preferred-lang';
  var dict = window.I18N || {};

  // Cache the original English text/HTML so we can restore it without a reload.
  var nodes = document.querySelectorAll('[data-i18n]');
  nodes.forEach(function (el) {
    el.setAttribute('data-i18n-en', el.innerHTML);
  });

  function pickLanguage() {
    // 1) explicit ?lang= override  2) saved choice  3) browser preference  4) English
    var params = new URLSearchParams(window.location.search);
    var q = (params.get('lang') || '').toLowerCase();
    if (SUPPORTED.indexOf(q) !== -1) return q;

    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved && SUPPORTED.indexOf(saved) !== -1) return saved;

    var prefs = navigator.languages || [navigator.language || 'en'];
    for (var i = 0; i < prefs.length; i++) {
      var base = prefs[i].toLowerCase().split('-')[0];
      if (SUPPORTED.indexOf(base) !== -1) return base;
    }
    return 'en';
  }

  function apply(lang, persist) {
    var table = lang === 'en' ? null : dict[lang];

    nodes.forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (lang === 'en') {
        el.innerHTML = el.getAttribute('data-i18n-en');
      } else if (table && table[key] != null) {
        el.innerHTML = table[key];
      } else {
        el.innerHTML = el.getAttribute('data-i18n-en'); // fallback to English
      }
    });

    // Expired-cert badge (CSS ::after reads this attribute via content)
    var badge = (table && table['certs.expiredBadge']) || 'EXPIRED';
    document.querySelectorAll('.cert-expired').forEach(function (el) {
      el.setAttribute('data-badge', badge);
    });

    // Document direction + lang
    var isRtl = RTL.indexOf(lang) !== -1;
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', isRtl ? 'rtl' : 'ltr');
    document.body.classList.toggle('rtl', isRtl);
    document.body.classList.toggle('lang-ar', lang === 'ar');
    document.body.classList.toggle('lang-ja', lang === 'ja');

    // Reflect active state on the switcher buttons
    document.querySelectorAll('.lang-btn').forEach(function (b) {
      var active = b.getAttribute('data-lang') === lang;
      b.classList.toggle('active', active);
      b.setAttribute('aria-pressed', String(active));
    });

    if (persist) localStorage.setItem(STORAGE_KEY, lang);
  }

  // Wire up the switcher
  document.querySelectorAll('.lang-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      apply(btn.getAttribute('data-lang'), true);
    });
  });

  apply(pickLanguage(), false);
}

