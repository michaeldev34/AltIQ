/**
 * AltIQ Scroll Animations
 * 
 * Handles scroll-triggered animations using IntersectionObserver.
 * For more complex animations, GSAP ScrollTrigger can be added later.
 * 
 * Usage:
 *   <div data-animate>Fades in from below</div>
 *   <div data-animate="fade">Fades in only</div>
 *   <div data-animate="scale">Scales up</div>
 *   <div data-animate data-stagger="1">First in sequence</div>
 *   <div data-animate data-stagger="2">Second in sequence</div>
 */

(function () {
  'use strict';

  // Hero entrance animation
  function animateHero() {
    const heroElements = [
      document.getElementById('hero-title'),
      document.getElementById('hero-lead'),
      document.getElementById('hero-bullets'),
      document.getElementById('hero-card')
    ].filter(Boolean);

    heroElements.forEach((el, index) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = `opacity 0.6s ease-out ${index * 100}ms, transform 0.6s ease-out ${index * 100}ms`;
    });

    // Trigger after a small delay to ensure styles are applied
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        heroElements.forEach((el) => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        });
      });
    });
  }

  // Scroll-triggered animations using IntersectionObserver
  function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');

    if (!animatedElements.length) return;

    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -10% 0px', // Trigger slightly before element is fully visible
      threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          // Optionally unobserve after animation (one-time animation)
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    animatedElements.forEach((el) => {
      observer.observe(el);
    });
  }

  // Stats counter animation
  function initCounterAnimations() {
    const counters = document.querySelectorAll('[data-counter]');

    if (!counters.length) return;

    const observerOptions = {
      threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.counter, 10);
          const duration = parseInt(el.dataset.duration, 10) || 1500;
          const prefix = el.dataset.prefix || '';
          const suffix = el.dataset.suffix || '';

          animateCounter(el, 0, target, duration, prefix, suffix);
          observer.unobserve(el);
        }
      });
    }, observerOptions);

    counters.forEach((el) => observer.observe(el));
  }

  function animateCounter(el, start, end, duration, prefix, suffix) {
    const startTime = performance.now();
    const range = end - start;

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Ease out quad
      const eased = 1 - (1 - progress) * (1 - progress);
      const current = Math.floor(start + range * eased);

      el.textContent = prefix + current.toLocaleString() + suffix;

      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }

    requestAnimationFrame(update);
  }

  // CTA hover effects for cursor expansion
  function initCTAHoverEffects() {
    const ring = document.getElementById('cursor-ring');
    if (!ring) return;

    const ctaElements = document.querySelectorAll('[data-cursor="cta"]');

    ctaElements.forEach((el) => {
      el.addEventListener('mouseenter', () => {
        ring.classList.add('cursor-ring--active');
      });

      el.addEventListener('mouseleave', () => {
        ring.classList.remove('cursor-ring--active');
      });
    });
  }

  // Initialize all animations on DOM ready
  function init() {
    animateHero();
    initScrollAnimations();
    initCounterAnimations();
    initCTAHoverEffects();
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

