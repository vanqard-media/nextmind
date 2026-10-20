(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Language selector: close when choosing, tapping outside or pressing Escape
  var langMenu = document.querySelector('.lang-menu');
  if (langMenu) {
    document.addEventListener('click', function (ev) { if (langMenu.open && !langMenu.contains(ev.target)) langMenu.open = false; });
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && langMenu.open) { langMenu.open = false; langMenu.querySelector('summary').focus(); } });
    langMenu.addEventListener('toggle', function () { if (langMenu.open && nav && nav.classList.contains('open')) { nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); } });
  }
  if (btn) btn.addEventListener('click', function () { if (langMenu) langMenu.open = false; });

  // Catalog: closed until the visitor picks an area; can be closed again.
  var filter = document.querySelector('.catalog-filter');
  if (!filter) return;
  var chips = filter.querySelectorAll('.tag');
  var panel = document.getElementById('catalog-panel');
  var items = panel.querySelectorAll('.catalog li');
  var count = panel.querySelector('.catalog-count');
  var hint = document.querySelector('.catalog-hint');
  var closeBtn = panel.querySelector('.catalog-close');
  var tpl = count ? count.getAttribute('data-template') : '';
  var current = null;

  function setHash(h) { if (history.replaceState) history.replaceState(null, '', h ? '#' + h : location.pathname + location.search); }

  function close(focusChip) {
    var was = current;
    current = null;
    panel.classList.remove('open');
    if (hint) hint.hidden = false;
    chips.forEach(function (c) { c.setAttribute('aria-pressed', 'false'); c.setAttribute('aria-expanded', 'false'); });
    setHash('');
    if (focusChip && was) { var b = filter.querySelector('[data-area="' + was + '"]'); if (b) b.focus(); }
  }

  function open(area) {
    var shown = 0;
    current = area;
    chips.forEach(function (c) {
      var on = c.getAttribute('data-area') === area;
      c.setAttribute('aria-pressed', on ? 'true' : 'false');
      c.setAttribute('aria-expanded', on ? 'true' : 'false');
    });
    items.forEach(function (li) {
      var on = area === 'all' || li.getAttribute('data-area') === area;
      li.hidden = !on;
      if (on) shown++;
    });
    if (count) count.textContent = tpl.replace('{n}', shown);
    if (hint) hint.hidden = true;
    panel.classList.add('open');
  }

  chips.forEach(function (c) {
    c.setAttribute('aria-expanded', 'false');
    c.addEventListener('click', function () {
      var a = c.getAttribute('data-area');
      if (current === a) { close(false); return; }   // clicking the open area closes it
      open(a);
      setHash(a === 'all' ? 'area-all' : 'area-' + a);
    });
  });
  if (closeBtn) closeBtn.addEventListener('click', function () { close(true); });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && current) close(true); });
  // Tap or click anywhere outside the area buttons and the open list closes it (no Escape key on phones).
  document.addEventListener('click', function (ev) {
    if (!current) return;
    if (ev.target.closest('.catalog-filter') || ev.target.closest('#catalog-panel')) return;
    close(false);
  });

  var m = location.hash.match(/^#area-([a-z]+)$/);
  if (m && filter.querySelector('[data-area="' + m[1] + '"]')) {
    open(m[1]);
    var s = document.getElementById('catalog'); if (s) s.scrollIntoView();
  }
})();
(function () {
  // Hero background video: only loads when the visitor allows motion and is not saving data.
  var v = document.querySelector('.hero-video');
  if (!v) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var conn = navigator.connection || {};
  if (reduce || conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '')) return; // poster only
  var mobile = window.matchMedia('(max-width: 720px) and (orientation: portrait)').matches;
  var list = [];
  if (mobile && v.dataset.mobile) list.push([v.dataset.mobile, 'video/mp4']);
  else {
    if (v.dataset.webm) list.push([v.dataset.webm, 'video/webm']);
    list.push([v.dataset.mp4, 'video/mp4']);
  }
  list.forEach(function (s) { var el = document.createElement('source'); el.src = s[0]; el.type = s[1]; v.appendChild(el); });
  v.muted = true;
  v.addEventListener('playing', function () { v.classList.add('is-playing'); });
  var btn = document.querySelector('.hero-toggle');
  function sync() {
    if (!btn) return;
    btn.hidden = false;
    var paused = v.paused;
    btn.setAttribute('aria-label', paused ? btn.dataset.play : btn.dataset.pause);
    btn.firstElementChild.textContent = paused ? '\u25B6' : 'II';
  }
  v.addEventListener('play', sync); v.addEventListener('pause', sync);
  if (btn) btn.addEventListener('click', function () { v.paused ? v.play() : v.pause(); });
  // Pause when the hero is off screen to save battery and CPU.
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) { if (!v.dataset.userPaused) v.play().catch(function () {}); }
        else v.pause();
      });
    }, { threshold: 0.15 }).observe(v);
  } else { v.play().catch(function () {}); }
  if (btn) btn.addEventListener('click', function () { v.dataset.userPaused = v.paused ? '1' : ''; });
  v.load();
})();
