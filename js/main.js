// ============================================
// Fares Amir Hassen — Personal Website JS
// Custom cursor + scroll reveal + mobile nav
// ============================================

document.addEventListener('DOMContentLoaded', () => {

  // --- Custom Cursor ---
  const dot = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');

  if (dot && ring && window.matchMedia('(pointer: fine)').matches) {
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

  // --- Scroll Reveal ---
  const reveals = document.querySelectorAll('.reveal');

  function checkReveal() {
    const windowHeight = window.innerHeight;
    const revealPoint = 120;

    reveals.forEach(el => {
      const elementTop = el.getBoundingClientRect().top;
      if (elementTop < windowHeight - revealPoint) {
        el.classList.add('visible');
      }
    });
  }

  // Initial check + scroll listener
  checkReveal();
  window.addEventListener('scroll', checkReveal, { passive: true });

  // --- Mobile Nav Toggle ---
  const toggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('active');
      navLinks.classList.toggle('open');
    });

    // Close menu on link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        toggle.classList.remove('active');
        navLinks.classList.remove('open');
      });
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
