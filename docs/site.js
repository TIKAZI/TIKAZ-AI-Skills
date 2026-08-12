const links = [...document.querySelectorAll('nav a')];
const sections = links.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      links.forEach((link) => link.removeAttribute('aria-current'));
      const active = links.find((link) => link.getAttribute('href') === `#${entry.target.id}`);
      if (active) active.setAttribute('aria-current', 'page');
    });
  }, { rootMargin: '-35% 0px -55%' });
  sections.forEach((section) => observer.observe(section));
}
