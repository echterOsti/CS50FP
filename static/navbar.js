const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('nav');

// listen for clicks on menu toggle button
menuToggle.addEventListener('click', function() {
  // toggle "active" class on nav element
  nav.classList.toggle('active');
});
