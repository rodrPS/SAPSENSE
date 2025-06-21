function toggleMobileMenu() {
  const menu = document.getElementById('navbar-links');
  menu.classList.toggle('show');
}

function toggleDropdown() {
  const dropdown = document.getElementById('dropdown-menu');
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}
