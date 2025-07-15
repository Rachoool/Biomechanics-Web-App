// Immediately apply saved theme before render
(function () {
  const savedTheme = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
})();

// DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  const themeDropdown = document.getElementById('themeDropdown');
  const dropdownItems = document.querySelectorAll('.dropdown-item');

  // Load current theme
  const currentTheme = document.documentElement.getAttribute("data-theme");
  updateThemeIcon(currentTheme);
  updateActiveItem(currentTheme);

  // click button to open/close menu
  themeToggle.addEventListener('click', function (e) {
    e.stopPropagation();
    themeDropdown.classList.toggle('show');
  });

  // click other position on page to close the menu
  document.addEventListener('click', function (e) {
    if (!themeToggle.contains(e.target) && !themeDropdown.contains(e.target)) {
      themeDropdown.classList.remove('show');
    }
  });

  // choose mode
  dropdownItems.forEach(item => {
    item.addEventListener('click', function () {
      const selectedTheme = this.getAttribute('data-theme');
      applyTheme(selectedTheme);
      themeDropdown.classList.remove('show');
    });
  });

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateThemeIcon(theme);
    updateActiveItem(theme);
  }

  function updateThemeIcon(theme) {
    if (themeIcon) {
      themeIcon.textContent = theme === 'dark' ? '🌙' : '☀️';
    }
  }

  function updateActiveItem(theme) {
    dropdownItems.forEach(item => {
      item.classList.remove('active');
      if (item.getAttribute('data-theme') === theme) {
        item.classList.add('active');
      }
    });
  }
});
