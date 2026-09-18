/* refine.js - homepage scroll reveals and the testimonial carousel, 2026-09-18.
   Everything here is progressive: without this file the page is fully visible
   and the testimonials are still a swipeable row. */
(function () {
  var root = document.documentElement;

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
