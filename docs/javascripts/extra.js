// Custom JavaScript for DevPulse documentation

document.addEventListener('DOMContentLoaded', function() {
  // Add copy button functionality enhancement
  const codeBlocks = document.querySelectorAll('pre code');
  codeBlocks.forEach(block => {
    block.addEventListener('click', function() {
      this.classList.add('copied');
      setTimeout(() => {
        this.classList.remove('copied');
      }, 2000);
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Add external link indicators
  const links = document.querySelectorAll('a[href^="http"]');
  links.forEach(link => {
    if (!link.hostname.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });

  // Table of contents highlight on scroll
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const id = entry.target.getAttribute('id');
      const tocLink = document.querySelector(`.md-nav__link[href="#${id}"]`);
      if (tocLink) {
        if (entry.isIntersecting) {
          tocLink.classList.add('md-nav__link--active');
        } else {
          tocLink.classList.remove('md-nav__link--active');
        }
      }
    });
  }, { rootMargin: '-20% 0px -35% 0px' });

  // Observe all headings
  document.querySelectorAll('h2[id], h3[id]').forEach(heading => {
    observer.observe(heading);
  });
});

// Add copy feedback
function copyFeedback(button) {
  const originalText = button.textContent;
  button.textContent = '✓ Copied!';
  button.classList.add('copied');
  
  setTimeout(() => {
    button.textContent = originalText;
    button.classList.remove('copied');
  }, 2000);
}
