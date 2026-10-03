(() => {
  const nav = document.querySelector('.nav');
  const links = document.getElementById('navLinks');
  const toggle = document.getElementById('navToggle');
  if (!nav || !links || !toggle) return;
  const mobile = window.matchMedia('(max-width: 1100px)');
  toggle.setAttribute('aria-controls', 'navLinks');
  toggle.setAttribute('aria-expanded', 'false');
  const sync = () => {
    const open = mobile.matches && links.classList.contains('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
  };
  const close = (focus = false) => {
    links.classList.remove('is-open');
    sync();
    if (focus) toggle.focus();
  };
  // Existing page handlers continue to toggle the menu; synchronize afterward.
  toggle.addEventListener('click', sync);
  nav.addEventListener('click', event => {
    if (event.target.closest('a')) close();
  });
  document.addEventListener('keydown', event => {
    if (!links.classList.contains('is-open')) return;
    if (event.key === 'Escape') { event.preventDefault(); close(true); return; }
    if (event.key !== 'Tab') return;
    const controls = [toggle, ...links.querySelectorAll('a[href]')];
    const first = controls[0], last = controls[controls.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  mobile.addEventListener('change', () => close());
  window.addEventListener('pageshow', () => close());
  sync();
})();
