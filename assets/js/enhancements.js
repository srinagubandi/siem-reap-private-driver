/* Angkor Drivers — accessibility & interaction enhancements */
(function () {
  'use strict';

  function init() {
    var hamburger = document.getElementById('hamburger');
    var drawer = document.getElementById('mobileDrawer');
    var closeBtn = document.getElementById('drawerClose');
    var overlay = document.getElementById('drawerOverlay');
    var langLeft = document.getElementById('langLeft');
    var langRight = document.getElementById('langRight');
    var langBar = document.getElementById('langBar');

    // ---------- Mobile drawer ----------
    if (hamburger && drawer && closeBtn && overlay) {
      drawer.setAttribute('aria-hidden', 'true');
      var lastFocused = null;
      var focusableSelector = 'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])';

      function getFocusable() {
        return Array.prototype.slice.call(drawer.querySelectorAll(focusableSelector))
          .filter(function (el) { return !el.hasAttribute('disabled') && el.offsetParent !== null; });
      }

      function openDrawer() {
        lastFocused = document.activeElement;
        drawer.classList.add('open');
        drawer.setAttribute('aria-hidden', 'false');
        hamburger.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
        var items = getFocusable();
        if (items.length) items[0].focus();
      }

      function closeDrawer() {
        drawer.classList.remove('open');
        drawer.setAttribute('aria-hidden', 'true');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
        if (lastFocused && document.contains(lastFocused)) lastFocused.focus();
        else hamburger.focus();
      }

      hamburger.addEventListener('click', function () {
        if (drawer.classList.contains('open')) closeDrawer();
        else openDrawer();
      });

      closeBtn.addEventListener('click', closeDrawer);
      overlay.addEventListener('click', closeDrawer);

      // Single keydown listener handles both focus trap and Escape
      drawer.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
          e.preventDefault();
          closeDrawer();
          return;
        }
        if (e.key === 'Tab') {
          var items = getFocusable();
          if (!items.length) return;
          var first = items[0];
          var last = items[items.length - 1];
          if (e.shiftKey) {
            if (document.activeElement === first) {
              e.preventDefault();
              last.focus();
            }
          } else {
            if (document.activeElement === last) {
              e.preventDefault();
              first.focus();
            }
          }
        }
      });
    }

    // ---------- Language strip scrolling (RTL aware) ----------
    if (langLeft && langRight && langBar) {
      var isRTL = window.getComputedStyle(document.documentElement).direction === 'rtl';
      var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      var behavior = reduceMotion ? 'auto' : 'smooth';
      var scrollAmount = 220;

      langLeft.addEventListener('click', function () {
        langBar.scrollBy({ left: isRTL ? scrollAmount : -scrollAmount, behavior: behavior });
      });
      langRight.addEventListener('click', function () {
        langBar.scrollBy({ left: isRTL ? -scrollAmount : scrollAmount, behavior: behavior });
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
