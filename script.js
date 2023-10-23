  // Get the navigation bar element
const navbar = document.getElementById('navbar');

// Set initial visibility of the navigation bar
navbar.style.display = 'none';

// Function to handle scroll event
function handleScroll() {
  // Get the current scroll position
  const scrollPosition = window.scrollY || document.documentElement.scrollTop;

  // Check if the scroll position is past 1000 pixels
  if (scrollPosition > 750) {
    // Display the navigation bar
    navbar.style.display = 'block';
  } else {
    // Hide the navigation bar
    navbar.style.display = 'none';
  }
}

// Add scroll event listener to the window
window.addEventListener('scroll', handleScroll);



window.onbeforeunload = function () {
    window.scrollTo(0, 0);
  }


  //Scroll Down button
  $(function() {
    $('a[href*=#thanks]').on('click', function(e) {
      e.preventDefault();
      $('html, body').animate({ scrollTop: $($(this).attr('href')).offset().top}, 500, 'linear');
    });
  });
