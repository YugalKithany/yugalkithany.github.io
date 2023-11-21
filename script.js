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
  
  
  
  
  var TxtType = function(el, toRotate, period) {
    this.toRotate = toRotate;
    this.el = el;
    this.loopNum = 0;
    this.period = parseInt(period, 10) || 2000;
    this.txt = '';
    this.tick();
    this.isDeleting = false;
  };
  
  TxtType.prototype.tick = function() {
    var i = this.loopNum % this.toRotate.length;
    var fullTxt = this.toRotate[i];
  
    if (this.isDeleting) {
    this.txt = fullTxt.substring(0, this.txt.length - 1);
    } else {
    this.txt = fullTxt.substring(0, this.txt.length + 1);
    }
  
    this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';
  
    var that = this;
    var delta = 200 - Math.random() * 100;
  
    if (this.isDeleting) { delta /= 2; }
  
    if (!this.isDeleting && this.txt === fullTxt) {
    delta = this.period;
    this.isDeleting = true;
    } else if (this.isDeleting && this.txt === '') {
    this.isDeleting = false;
    this.loopNum++;
    delta = 500;
    }
  
    setTimeout(function() {
    that.tick();
    }, delta);
  };
  
  window.onload = function() {
    var elements = document.getElementsByClassName('typewrite');
    for (var i=0; i<elements.length; i++) {
        var toRotate = JSON.parse(elements[i].getAttribute('data-type'));
        toRotate = Object.values(toRotate); // Convert parsed JSON object to array of strings
        var period = elements[i].getAttribute('data-period');
        if (toRotate) {
          new TxtType(elements[i], toRotate, period);
        }
    }
    // INJECT CSS
    var css = document.createElement("style");
    // css.type = "text/css";
    css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #fff}";
    document.body.appendChild(css);
  };
  
  
  
  
  
  //Scroll Down button
  $(function() {
    $('a[href*=#about]').on('click', function(e) {
      e.preventDefault();
      $('html, body').animate({ scrollTop: $($(this).attr('href')).offset().top}, 500, 'linear');
    });
  });