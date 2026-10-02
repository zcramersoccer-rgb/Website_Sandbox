/* refine.js - homepage scroll reveals and the testimonial carousel, 2026-09-18.
   Everything here is progressive: without this file the page is fully visible
   and the testimonials are still a swipeable row. */
(function () {
  var root = document.documentElement;

  /* Hero video: the poster is the first paint (and the LCP image). The video file itself is only
     attached once the page has finished loading, so it never competes with the first screen on phones.
     Reduced-motion and data-saver visitors keep the still poster. */
  var vid = document.querySelector('.rf-vhero-video');
  if (vid) {
    var keepStill = (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) ||
                (navigator.connection && navigator.connection.saveData);
    if (!keepStill) {
      var startVideo = function () {
        var small = window.matchMedia && window.matchMedia('(max-width: 900px)').matches;
        var go = function () { var p = vid.play(); if (p && p.catch) p.catch(function () {}); };
        vid.muted = true;
        vid.autoplay = true;
        vid.preload = 'auto';
        vid.src = small ? vid.getAttribute('data-src-sm') : vid.getAttribute('data-src-lg');
        vid.addEventListener('canplay', go, { once: true });
        document.addEventListener('visibilitychange', function () { if (!document.hidden && vid.paused) go(); });
        vid.load();
      };
      if (document.readyState === 'complete') setTimeout(startVideo, 300);
      else window.addEventListener('load', function () { setTimeout(startVideo, 300); });
    }
  }

  /* Scroll reveals. Nothing is ever hidden up front (a page parked at opacity:0
     stops Chrome measuring Largest Contentful Paint). Sections already on screen
     at load are left alone; the rest get .rf-in just before they scroll into
     view, which plays the fade-up animation in refine.css. */
  var items = document.querySelectorAll('.rf-reveal');
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (items.length && 'IntersectionObserver' in window && !still) {
    root.classList.add('rf-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('rf-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px 6% 0px', threshold: 0 });
    var fold = window.innerHeight;
    items.forEach(function (el) {
      if (el.getBoundingClientRect().top < fold) return;  // visible at load: no animation
      io.observe(el);
    });
  }

  /* Testimonial arrows. Swiping works natively; the arrows move one card at a
     time. Scroll snapping is only switched on after the first touch, click or
     key press on the carousel, so nothing scrolls while the page is loading. */
  document.querySelectorAll('.rf-quotes').forEach(function (box) {
    var track = box.querySelector('.rf-track');
    var prev = box.querySelector('.rf-prev');
    var next = box.querySelector('.rf-next');
    if (!track || !prev || !next) return;

    function snapOn() { track.classList.add('rf-snap'); }
    ['pointerdown', 'touchstart', 'keydown', 'wheel'].forEach(function (ev) {
      box.addEventListener(ev, snapOn, { once: true, passive: true });
    });

    function step() {
      var card = track.querySelector('.rf-quote');
      if (!card) return track.clientWidth;
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      return card.getBoundingClientRect().width + gap;
    }
    function sync() {
      var max = track.scrollWidth - track.clientWidth - 2;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
    }
    prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('scroll', function () { window.requestAnimationFrame(sync); }, { passive: true });
    window.addEventListener('resize', sync);
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); next.click(); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); prev.click(); }
    });
    sync();
  });
})();

/* Keep the chat button off the call and consultation buttons on phones (2026-10-02, Zach: "go ahead and fix
   the homepage"). Every ad now lands here, and at 375x812 the hero's "Request a Consultation" sits right at the
   fold where the fixed chat button (and its once-per-visit teaser) is drawn, covering it. While any of the
   page's call/consultation button rows - or the form's submit button - is inside the bottom strip of the
   screen where the chat sits, the chat steps aside; it comes back as soon as the visitor scrolls on. Phones
   only: on desktop the hero buttons are nowhere near the corner. The chat itself is untouched (its script is
   served from chat.cramerslandscaping.com); this only hides it with a class on <html>. */
(function () {
  if (!('IntersectionObserver' in window) || !window.matchMedia) return;
  var root = document.documentElement;
  var STRIP = 120;            // chat button 64px + 14px margin, with room for the teaser's tail
  var css = document.createElement('style');
  css.textContent = 'html.cl-chat-tuck .clw-fab,html.cl-chat-tuck .clw-tip' +
    '{opacity:0!important;visibility:hidden!important;pointer-events:none!important}';
  document.head.appendChild(css);
  var mq = window.matchMedia('(max-width: 760px)');
  var targets = [].slice.call(document.querySelectorAll('.ib-kk-home-btn-container, .wpforms-submit-container'));
  if (!targets.length) return;
  var io = null;
  function update() {
    var hit = targets.some(function (t) { return t.clInStrip; });
    root.classList.toggle('cl-chat-tuck', mq.matches && hit);
  }
  function build() {
    if (io) io.disconnect();
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { e.target.clInStrip = e.isIntersecting; });
      update();
    }, { rootMargin: '-' + Math.max(0, window.innerHeight - STRIP) + 'px 0px 0px 0px' });
    targets.forEach(function (t) { io.observe(t); });
  }
  var timer = null;
  window.addEventListener('resize', function () { clearTimeout(timer); timer = setTimeout(build, 150); });
  if (mq.addEventListener) mq.addEventListener('change', update);
  build();
})();
