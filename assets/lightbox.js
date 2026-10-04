/* lightbox.js - gallery photos open over the page instead of in a new tab (2026-10-03).
   Before this, every portfolio and project-page photo was <a href="...-1600.webp" target="_blank">, and with no
   lightbox loaded a tap opened a raw image file in a new browser tab: no branding, no menu, no way back but closing
   the tab. /portfolio/ is the second most visited page and shows up as an exit page.
   Progressive: the links are untouched, so without this script they still open the image. No library.
   Shipped in the shell (deploy_shell.py) so it covers every page that has a gallery. */
(function () {
  var SEL = 'main a[href$=".webp"]';
  var links = [].slice.call(document.querySelectorAll(SEL)).filter(function (a) { return a.querySelector('img'); });
  if (!links.length) return;

  var css = document.createElement('style');
  css.textContent =
    '.clb{position:fixed;inset:0;z-index:2147483600;background:rgba(10,14,12,.94);display:flex;align-items:center;' +
    'justify-content:center;flex-direction:column;padding:56px 12px 20px;box-sizing:border-box;touch-action:pan-y}' +
    '.clb[hidden]{display:none}' +
    '.clb img{max-width:100%;max-height:calc(100% - 64px);object-fit:contain;border-radius:6px;' +
    'box-shadow:0 10px 40px rgba(0,0,0,.5);user-select:none;-webkit-user-select:none}' +
    '.clb p{color:#e5e7eb;font:400 15px/1.45 "DM Sans",system-ui,sans-serif;text-align:center;max-width:720px;margin:14px 8px 0}' +
    '.clb button{position:absolute;border:0;background:rgba(255,255,255,.12);color:#fff;width:48px;height:48px;' +
    'border-radius:50%;font:400 28px/48px system-ui,sans-serif;cursor:pointer;padding:0}' +
    '.clb button:hover{background:rgba(255,255,255,.24)}' +
    '.clb button:focus-visible{outline:3px solid #34d399;outline-offset:2px}' +
    '.clb .clb-x{top:10px;right:10px}' +
    '.clb .clb-p{left:10px;top:50%;margin-top:-24px}.clb .clb-n{right:10px;top:50%;margin-top:-24px}' +
    '.clb .clb-c{position:absolute;top:22px;left:16px;color:#9ca3af;font:500 14px/1 "DM Sans",system-ui,sans-serif}' +
    '@media (max-width:600px){.clb .clb-p,.clb .clb-n{top:auto;bottom:14px;margin-top:0}}';
  document.head.appendChild(css);

  var box = document.createElement('div');
  box.className = 'clb';
  box.hidden = true;
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.setAttribute('aria-label', 'Photo viewer');
  box.innerHTML = '<span class="clb-c" aria-live="polite"></span>' +
    '<button type="button" class="clb-x" aria-label="Close photo">&times;</button>' +
    '<button type="button" class="clb-p" aria-label="Previous photo">&#8249;</button>' +
    '<button type="button" class="clb-n" aria-label="Next photo">&#8250;</button>' +
    '<img alt=""><p></p>';
  document.body.appendChild(box);
  var img = box.querySelector('img'), cap = box.querySelector('p'), count = box.querySelector('.clb-c');
  var btnX = box.querySelector('.clb-x'), btnP = box.querySelector('.clb-p'), btnN = box.querySelector('.clb-n');

  var set = [], i = 0, opener = null, overflow = '';

  function groupOf(a) {          // step through the gallery the photo belongs to, not the whole page
    var g = a.closest('.cl-work-grid, .pj-gallery, section, .cl-sec') || document.querySelector('main');
    return links.filter(function (l) { return g.contains(l); });
  }
  function caption(a) {
    var f = a.closest('figure'), fc = f && f.querySelector('figcaption');
    var t = fc ? fc.textContent : (a.querySelector('img').getAttribute('alt') || '');
    return t.replace(/\s+/g, ' ').trim();
  }
  function show(k) {
    i = (k + set.length) % set.length;
    var a = set[i], im = a.querySelector('img');
    img.src = a.getAttribute('href');
    img.alt = im.getAttribute('alt') || '';
    cap.textContent = caption(a);
    count.textContent = set.length > 1 ? (i + 1) + ' / ' + set.length : '';
    btnP.hidden = btnN.hidden = set.length < 2;
  }
  function open(a) {
    opener = a; set = groupOf(a);
    show(set.indexOf(a));
    overflow = document.documentElement.style.overflow;
    document.documentElement.style.overflow = 'hidden';
    box.hidden = false;
    btnX.focus();
  }
  function close() {
    box.hidden = true;
    img.removeAttribute('src');
    document.documentElement.style.overflow = overflow;
    if (opener) opener.focus();
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest(SEL);
    if (!a || links.indexOf(a) < 0) return;
    e.preventDefault();
    open(a);
  });
  btnX.addEventListener('click', close);
  btnP.addEventListener('click', function () { show(i - 1); });
  btnN.addEventListener('click', function () { show(i + 1); });
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'Escape') { e.preventDefault(); close(); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); show(i - 1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); show(i + 1); }
    else if (e.key === 'Tab') {            // keep focus inside the viewer
      var f = [btnX, btnP, btnN].filter(function (b) { return !b.hidden; });
      var at = f.indexOf(document.activeElement);
      e.preventDefault();
      f[(at + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    }
  });
  var x0 = null;
  box.addEventListener('touchstart', function (e) { x0 = e.touches.length === 1 ? e.touches[0].clientX : null; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (x0 === null || set.length < 2) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1));
    x0 = null;
  }, { passive: true });
})();
