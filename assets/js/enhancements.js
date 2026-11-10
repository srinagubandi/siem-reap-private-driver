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

    // ---------- Gallery image prefetch ----------
    // Keep the first visible image as the priority image; warm the remaining
    // local cards only while the browser is idle and the connection allows it.
    function scheduleGalleryPrefetch(selector, skipFirst) {
      var links = Array.prototype.slice.call(document.querySelectorAll(selector + ' a[href]'));
      var connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (!links.length || (connection && (connection.saveData || /(^|-)2g$/.test(connection.effectiveType || '')))) return;
      var urls = links.slice(skipFirst ? 1 : 0).map(function (link) {
        try {
          var url = new URL(link.getAttribute('href'), window.location.href);
          return url.origin === window.location.origin && /\.(?:avif|jpe?g|png|webp)(?:\?.*)?$/i.test(url.pathname) ? url.href : null;
        } catch (error) {
          return null;
        }
      }).filter(Boolean);
      if (!urls.length) return;
      var warmImages = function () {
        urls.forEach(function (url) {
          var image = new Image();
          image.decoding = 'async';
          image.src = url;
        });
      };
      if ('requestIdleCallback' in window) window.requestIdleCallback(warmImages, { timeout: 2500 });
      else window.setTimeout(warmImages, 900);
    }
    scheduleGalleryPrefetch('.guest-gallery-cards', false);
    scheduleGalleryPrefetch('.ta-traveler-photo-grid', true);

    // ---------- Static multi-gallery lightboxes ----------
    // Each gallery keeps native links without JS and receives the same controls
    // when JS loads. The Moments lead image is first in its own gallery order.
    var galleryRoots = Array.prototype.slice.call(document.querySelectorAll('[data-gallery-template="thumbsup-cards"]'));
    galleryRoots.forEach(function (galleryRoot) {
      var gallerySection = galleryRoot.closest('#guest-gallery, #tripadvisor-traveler-photos') || galleryRoot;
      var galleryKind = gallerySection.id === 'guest-gallery' ? 'moments' : 'traveler';
      var galleryToolbar = document.querySelector('[data-gallery-toolbar="' + galleryKind + '"]');
      var galleryLinks = galleryKind === 'moments'
        ? [document.querySelector('#guest-family-photo > a')].concat(Array.prototype.slice.call(galleryRoot.querySelectorAll('.guest-gallery-card > a')))
        : Array.prototype.slice.call(galleryRoot.querySelectorAll('.ta-traveler-photo > a'));
      var galleryItems = galleryLinks.filter(function (link) { return link.querySelector('img'); });
      if (!galleryItems.length) return;

      var lightbox = document.createElement('dialog');
      var lightboxId = 'gallery-lightbox-' + galleryKind;
      var hashPrefix = galleryKind === 'moments' ? '#moments-gallery-' : '#gallery-';
      lightbox.className = 'gallery-lightbox';
      lightbox.id = lightboxId;
      lightbox.setAttribute('aria-labelledby', lightboxId + '-title');
      lightbox.innerHTML = '' +
        '<div class="gallery-lightbox__panel" role="document">' +
          '<div class="gallery-lightbox__toolbar">' +
            '<h2 id="' + lightboxId + '-title" class="gallery-lightbox__title">' + (galleryKind === 'moments' ? 'Guest moment' : 'Traveler photo') + '</h2>' +
            '<span class="gallery-lightbox__count" aria-live="polite"></span>' +
            '<button type="button" class="gallery-lightbox__close" aria-label="Close photo viewer">×</button>' +
          '</div>' +
          '<div class="gallery-lightbox__stage">' +
            '<button type="button" class="gallery-lightbox__nav gallery-lightbox__prev" aria-label="Previous photo">‹</button>' +
            '<img class="gallery-lightbox__image" alt="" decoding="async">' +
            '<button type="button" class="gallery-lightbox__nav gallery-lightbox__next" aria-label="Next photo">›</button>' +
          '</div>' +
          '<p class="gallery-lightbox__caption"></p>' +
        '</div>';
      document.body.appendChild(lightbox);

      var viewerImage = lightbox.querySelector('.gallery-lightbox__image');
      var viewerCaption = lightbox.querySelector('.gallery-lightbox__caption');
      var viewerCount = lightbox.querySelector('.gallery-lightbox__count');
      var closeViewer = lightbox.querySelector('.gallery-lightbox__close');
      var previousPhoto = lightbox.querySelector('.gallery-lightbox__prev');
      var nextPhoto = lightbox.querySelector('.gallery-lightbox__next');
      var galleryOpenButton = galleryToolbar && galleryToolbar.querySelector('[data-gallery-open]');
      var galleryCountGroup = galleryToolbar && galleryToolbar.querySelector('[data-gallery-count-group]');
      var galleryCount = galleryToolbar && galleryToolbar.querySelector('[data-gallery-count]');
      var galleryKeyboardHint = galleryToolbar && galleryToolbar.querySelector('[data-gallery-keyboard]');
      var galleryTouchHint = galleryToolbar && galleryToolbar.querySelector('[data-gallery-touch]');
      var activeIndex = 0;
      var lastGalleryFocus = null;
      var lightboxOpen = false;
      var touchStartX = null;
      var touchStartY = null;
      var backgroundState = [];
      lightbox.setAttribute('aria-modal', 'true');

      function galleryHash(index) { return hashPrefix + (index + 1); }
      function renderGalleryPhoto(index, updateHash) {
        activeIndex = (index + galleryItems.length) % galleryItems.length;
        var card = galleryItems[activeIndex].closest('.ta-traveler-photo, .guest-gallery-card, .guest-featured-photo');
        var sourceImage = card.querySelector('img');
        var caption = card.querySelector('figcaption');
        viewerImage.src = sourceImage.currentSrc || sourceImage.src;
        viewerImage.alt = sourceImage.alt || '';
        viewerCaption.textContent = caption ? caption.textContent.trim() : sourceImage.alt;
        viewerCount.textContent = (activeIndex + 1) + ' / ' + galleryItems.length;
        previousPhoto.disabled = galleryItems.length < 2;
        nextPhoto.disabled = galleryItems.length < 2;
        if (updateHash) history.replaceState(null, '', galleryHash(activeIndex));
      }
      function setBackgroundInert(inert) {
        if (inert) {
          backgroundState = Array.prototype.slice.call(document.body.children).filter(function (element) { return element !== lightbox; }).map(function (element) {
            return { element: element, ariaHidden: element.getAttribute('aria-hidden'), inert: Boolean(element.inert) };
          });
          backgroundState.forEach(function (state) { state.element.setAttribute('aria-hidden', 'true'); state.element.inert = true; });
        } else {
          backgroundState.forEach(function (state) {
            if (state.ariaHidden === null) state.element.removeAttribute('aria-hidden');
            else state.element.setAttribute('aria-hidden', state.ariaHidden);
            state.element.inert = state.inert;
          });
          backgroundState = [];
        }
      }
      function openGallery(index) {
        lastGalleryFocus = document.activeElement;
        renderGalleryPhoto(index, true);
        lightboxOpen = true;
        setBackgroundInert(true);
        document.body.classList.add('gallery-lightbox-open');
        if (typeof lightbox.showModal === 'function') lightbox.showModal();
        else lightbox.setAttribute('open', '');
        closeViewer.focus();
      }
      function closeGallery(clearHash) {
        lightboxOpen = false;
        setBackgroundInert(false);
        document.body.classList.remove('gallery-lightbox-open');
        if (typeof lightbox.close === 'function' && lightbox.open) lightbox.close();
        else lightbox.removeAttribute('open');
        if (clearHash && window.location.hash.indexOf(hashPrefix) === 0) history.replaceState(null, '', window.location.pathname + window.location.search);
        if (lastGalleryFocus && document.contains(lastGalleryFocus)) lastGalleryFocus.focus();
      }
      galleryItems.forEach(function (link, index) {
        link.addEventListener('click', function (event) {
          if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
          event.preventDefault();
          openGallery(index);
        });
      });
      if (galleryOpenButton && galleryCount && galleryCountGroup) {
        galleryOpenButton.setAttribute('aria-controls', lightbox.id);
        galleryCount.textContent = String(galleryItems.length);
        galleryCountGroup.removeAttribute('hidden');
        galleryOpenButton.removeAttribute('hidden');
        if (galleryKeyboardHint) galleryKeyboardHint.removeAttribute('hidden');
        if (galleryTouchHint) galleryTouchHint.removeAttribute('hidden');
        galleryOpenButton.addEventListener('click', function () { openGallery(0); });
      }
      closeViewer.addEventListener('click', function () { closeGallery(true); });
      previousPhoto.addEventListener('click', function () { renderGalleryPhoto(activeIndex - 1, true); });
      nextPhoto.addEventListener('click', function () { renderGalleryPhoto(activeIndex + 1, true); });
      lightbox.addEventListener('click', function (event) { if (event.target === lightbox) closeGallery(true); });
      lightbox.addEventListener('cancel', function (event) { event.preventDefault(); closeGallery(true); });
      lightbox.addEventListener('touchstart', function (event) { touchStartX = event.changedTouches[0].clientX; touchStartY = event.changedTouches[0].clientY; }, { passive: true });
      lightbox.addEventListener('touchmove', function (event) {
        if (touchStartX === null || touchStartY === null) return;
        var dx = event.changedTouches[0].clientX - touchStartX;
        var dy = event.changedTouches[0].clientY - touchStartY;
        if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 12) event.preventDefault();
      }, { passive: false });
      lightbox.addEventListener('touchend', function (event) {
        if (touchStartX === null || touchStartY === null) return;
        var delta = event.changedTouches[0].clientX - touchStartX;
        touchStartX = null; touchStartY = null;
        if (Math.abs(delta) < 48) return;
        renderGalleryPhoto(activeIndex + (delta < 0 ? 1 : -1), true);
      }, { passive: true });
      document.addEventListener('keydown', function (event) {
        if (!lightboxOpen) return;
        if (event.key === 'Escape') { event.preventDefault(); closeGallery(true); return; }
        if (event.key === 'ArrowLeft') { event.preventDefault(); renderGalleryPhoto(activeIndex - 1, true); return; }
        if (event.key === 'ArrowRight') { event.preventDefault(); renderGalleryPhoto(activeIndex + 1, true); return; }
        if (event.key !== 'Tab') return;
        var focusable = [closeViewer, previousPhoto, nextPhoto].filter(function (element) { return !element.disabled; });
        if (event.shiftKey && document.activeElement === focusable[0]) { event.preventDefault(); focusable[focusable.length - 1].focus(); }
        else if (!event.shiftKey && document.activeElement === focusable[focusable.length - 1]) { event.preventDefault(); focusable[0].focus(); }
      });
      function openFromHash() {
        var match = window.location.hash.match(new RegExp('^' + hashPrefix.replace('#', '#') + '(\\d+)$'));
        if (!match) { if (lightboxOpen) closeGallery(false); return; }
        var index = parseInt(match[1], 10) - 1;
        if (index >= 0 && index < galleryItems.length) openGallery(index);
      }
      window.addEventListener('hashchange', openFromHash);
      openFromHash();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
