/**
 * AltIQ Custom Cursor
 * 
 * A sophisticated dual-element cursor with:
 * - Precise dot that follows mouse exactly
 * - Smooth ring that follows with easing
 * - Expansion on CTA/interactive element hover
 * - Magnetic effect on buttons (optional)
 * - Hidden on touch devices (via CSS)
 */

(function () {
  'use strict';

  // Only run on devices with fine pointer (mouse)
  if (window.matchMedia('(pointer: coarse)').matches) return;

  const dot = document.getElementById('cursor-dot');
  const ring = document.getElementById('cursor-ring');

  if (!dot || !ring) return;

  // Mouse position tracking
  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let ringX = mouseX;
  let ringY = mouseY;

  // Easing factor for ring follow (lower = smoother, higher = faster)
  const EASE = 0.15;

  // Track mouse position
  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    dot.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
  });

  // Animation loop for smooth ring follow
  function animateRing() {
    ringX += (mouseX - ringX) * EASE;
    ringY += (mouseY - ringY) * EASE;
    ring.style.transform = `translate(${ringX}px, ${ringY}px)`;
    requestAnimationFrame(animateRing);
  }
  animateRing();

  // Click feedback
  document.addEventListener('mousedown', () => {
    ring.classList.add('cursor-ring--active');
  });

  document.addEventListener('mouseup', () => {
    ring.classList.remove('cursor-ring--active');
  });

  // Interactive element detection
  const interactiveSelectors = [
    'a',
    'button',
    '[role="button"]',
    'input',
    'textarea',
    'select',
    '[data-cursor="cta"]',
    '.btn',
    '.card-interactive'
  ].join(',');

  document.addEventListener('mouseover', (e) => {
    const target = e.target.closest(interactiveSelectors);
    if (target) {
      ring.classList.add('cursor-ring--active');
    }
  });

  document.addEventListener('mouseout', (e) => {
    const target = e.target.closest(interactiveSelectors);
    if (target) {
      ring.classList.remove('cursor-ring--active');
    }
  });

  // Hide cursor when leaving window
  document.addEventListener('mouseleave', () => {
    ring.classList.add('cursor-ring--hidden');
    dot.style.opacity = '0';
  });

  document.addEventListener('mouseenter', () => {
    ring.classList.remove('cursor-ring--hidden');
    dot.style.opacity = '1';
  });

  // Optional: Magnetic effect for buttons with .btn-magnetic class
  const magneticElements = document.querySelectorAll('.btn-magnetic');
  
  magneticElements.forEach((el) => {
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const deltaX = (e.clientX - centerX) * 0.2;
      const deltaY = (e.clientY - centerY) * 0.2;
      el.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
    });

    el.addEventListener('mouseleave', () => {
      el.style.transform = 'translate(0, 0)';
    });
  });
})();

