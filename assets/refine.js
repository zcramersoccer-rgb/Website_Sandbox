/* refine.js - homepage scroll reveals and the testimonial carousel, 2026-09-18.
   Everything here is progressive: without this file the page is fully visible
   and the testimonials are still a swipeable row. */
(function () {
  var root = document.documentElement;

  /* Scroll reveals. The rf-js class is what arms the hidden state in
     refine.css, so it is only added once we know we can undo it. */
  var items = document.querySelectorAll('.rf-reveal');
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (items.length && 'IntersectionObserver' in window && !still) {
    root.classList.add('rf-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('rf-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* Testimonial arrows. The track is a native scroll-snap row, so touch
     swiping works on its own; the arrows move it one card at a time. */
  document.querySelectorAll('.rf-quotes').forEach(function (box) {
    var track = box.querySelector('.rf-track');
    var prev = box.querySelector('.rf-prev');
    var next = box.querySelector('.rf-next');
    if (!track || !prev || !next) return;

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
