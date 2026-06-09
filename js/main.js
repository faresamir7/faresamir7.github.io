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

});
