const links = [...document.querySelectorAll('nav a')];
const sectionLinks = links.filter((link) => link.getAttribute('href')?.startsWith('#'));
const sections = sectionLinks.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      sectionLinks.forEach((link) => link.removeAttribute('aria-current'));
      const active = sectionLinks.find((link) => link.getAttribute('href') === `#${entry.target.id}`);
      if (active) active.setAttribute('aria-current', 'page');
    });
  }, { rootMargin: '-35% 0px -55%' });
  sections.forEach((section) => observer.observe(section));
}

document.querySelectorAll('[data-lang]').forEach((link) => {
  if (!(link instanceof HTMLAnchorElement)) return;
  link.addEventListener('click', () => {
    try { localStorage.setItem('tikaz-docs-language', link.dataset.lang || 'en'); } catch (_) {}
  });
});
