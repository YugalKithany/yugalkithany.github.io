// Typewriter Effect
class TypeWriter {
    constructor(element, words, wait = 3000) {
        this.element = element;
        this.words = words;
        this.txt = '';
        this.wordIndex = 0;
        this.wait = parseInt(wait, 10);
        this.type();
        this.isDeleting = false;
    }

    type() {
        const current = this.wordIndex % this.words.length;
        const fullTxt = this.words[current];

        if (this.isDeleting) {
            this.txt = fullTxt.substring(0, this.txt.length - 1);
        } else {
            this.txt = fullTxt.substring(0, this.txt.length + 1);
        }

        this.element.innerHTML = `<span class="txt">${this.txt}</span>`;

        let typeSpeed = 100;

        if (this.isDeleting) {
            typeSpeed /= 2;
        }

        if (!this.isDeleting && this.txt === fullTxt) {
            typeSpeed = this.wait;
            this.isDeleting = true;
        } else if (this.isDeleting && this.txt === '') {
            this.isDeleting = false;
            this.wordIndex++;
            typeSpeed = 200;
        }

        setTimeout(() => this.type(), typeSpeed);
    }
}

// Initialize typewriter
document.addEventListener('DOMContentLoaded', function() {
    const typeWriterElement = document.getElementById('typewriter');
    const words = ['Research Assistant', 'Software Developer', 'Systems Engineer', 'AI/ML Enthusiast'];
    new TypeWriter(typeWriterElement, words, 2000);
});

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Smooth scrolling for navigation links
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

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe all fade-in elements
document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Parallax effect for background orbs
// window.addEventListener('scroll', function() {
//     const scrolled = window.pageYOffset;
//     const parallax1 = document.querySelector('.orb-1');
//     const parallax2 = document.querySelector('.orb-2');
    
//     if (parallax1) {
//         parallax1.style.transform = `translateY(${scrolled * 0.5}px)`;
//     }
//     if (parallax2) {
//         parallax2.style.transform = `translateY(${scrolled * -0.3}px)`;
//     }
// });


// Dynamic cursor effect (optional enhancement)
document.addEventListener('mousemove', function(e) {
    const cursor = document.querySelector('.cursor');
    if (cursor) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    }
});

// Add loading animation
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Easter egg - Konami code
let konamiCode = [];
const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];

document.addEventListener('keydown', function(e) {
    konamiCode.push(e.keyCode);
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        // Easter egg triggered
        document.body.style.filter = 'hue-rotate(180deg)';
        setTimeout(() => {
            document.body.style.filter = 'none';
        }, 3000);
    }
});

// Performance optimization - throttle scroll events
function throttle(func, limit) {
    let lastFunc;
    let lastRan;
    return function() {
        const context = this;
        const args = arguments;
        if (!lastRan) {
            func.apply(context, args);
            lastRan = Date.now();
        } else {
            clearTimeout(lastFunc);
            lastFunc = setTimeout(function() {
                if ((Date.now() - lastRan) >= limit) {
                    func.apply(context, args);
                    lastRan = Date.now();
                }
            }, limit - (Date.now() - lastRan));
        }
    };
}

// Apply throttling to scroll events
window.addEventListener('scroll', throttle(function() {
    // Scroll-dependent animations can be added here
}, 16)); // ~60fps

// Theme Switcher
document.addEventListener('DOMContentLoaded', () => {
    const themeSwitcher = document.getElementById('theme-switcher');
    const body = document.body;

    // Check for saved theme in localStorage or default to light
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        if (savedTheme === 'light-theme') {
            themeSwitcher.innerHTML = '☽';
        } else {
            themeSwitcher.innerHTML = '☀';
        }
    } else {
        // Default to light theme if no theme is saved
        body.classList.add('light-theme');
        themeSwitcher.innerHTML = '☽';
        localStorage.setItem('theme', 'light-theme');
    }

    themeSwitcher.addEventListener('click', () => {
        if (body.classList.contains('dark-theme')) {
            body.classList.replace('dark-theme', 'light-theme');
            themeSwitcher.innerHTML = '☽';
            localStorage.setItem('theme', 'light-theme');
        } else {
            body.classList.replace('light-theme', 'dark-theme');
            themeSwitcher.innerHTML = '☀';
            localStorage.setItem('theme', 'dark-theme');
        }
    });
});

// Orb Animation on Scroll
let hasScrolled = false; // Flag to ensure animation starts only once

window.addEventListener('scroll', function() {
    if (!hasScrolled) {
        const orb1 = document.querySelector('.orb-1');
        const orb2 = document.querySelector('.orb-2');

        if (orb1) {
            orb1.style.animationPlayState = 'running';
        }
        if (orb2) {
            orb2.style.animationPlayState = 'running';
        }
        hasScrolled = true; // Set flag to true after animations start
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Filter projects
            projectCards.forEach(card => {
                const tags = card.getAttribute('data-tags');
                
                if (filter === 'all' || (tags && tags.includes(filter))) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });
});



// Keyboard Animation
document.addEventListener('DOMContentLoaded', function() {
    const keyboardContainer = document.getElementById('keyboardContainer');
    const heroContent = document.getElementById('heroContent');
    const signatureOverlay = document.getElementById('signatureOverlay');
    
// Check if mobile device
    const isMobile = window.innerWidth <= 768 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    if (isMobile) {
        // Skip animation on mobile, show content immediately with original layout
        keyboardContainer.style.display = 'none';
        heroContent.style.display = 'block';
        heroContent.style.textAlign = 'center';
        heroContent.style.opacity = '1';
        heroContent.style.animation = 'none';
        return;
    }
    
    // Realistic QWERTY keyboard layout positions matching actual keyboards
    const keyPositions = {
        'Q': [0, 0], 'W': [1, 0], 'E': [2, 0], 'R': [3, 0], 'T': [4, 0],
        'Y': [5, 0], 'U': [6, 0], 'I': [7, 0], 'O': [8, 0], 'P': [9, 0],
        'A': [0.25, 1], 'S': [1.25, 1], 'D': [2.25, 1], 'F': [3.25, 1], 'G': [4.25, 1],
        'H': [5.25, 1], 'J': [6.25, 1], 'K': [7.25, 1], 'L': [8.25, 1],
        'Z': [0.75, 2], 'X': [1.75, 2], 'C': [2.75, 2], 'V': [3.75, 2], 'B': [4.75, 2],
        'N': [5.75, 2], 'M': [6.75, 2]
    };
    
    const name = 'YUGALKITHANY';
    let currentIndex = 0;
    let lines = [];
    
    function createLine(from, to) {
        const keyboard = document.querySelector('.keyboard');
        const line = document.createElement('div');
        line.className = 'line';
        
        const fromPos = keyPositions[from];
        const toPos = keyPositions[to];
        
        if (!fromPos || !toPos) return;
        
        const fromX = fromPos[0] * 70 + 30;
        const fromY = fromPos[1] * 70 + 30;
        const toX = toPos[0] * 70 + 30;
        const toY = toPos[1] * 70 + 30;
        
        const length = Math.sqrt(Math.pow(toX - fromX, 2) + Math.pow(toY - fromY, 2));
        const angle = Math.atan2(toY - fromY, toX - fromX) * 180 / Math.PI;
        
        line.style.width = length + 'px';
        line.style.left = fromX + 'px';
        line.style.top = fromY + 'px';
        line.style.transform = `rotate(${angle}deg)`;
        line.style.transformOrigin = '0 50%';
        
        keyboard.appendChild(line);
        return line;
    }
    
    function animateKeyboard() {
        keyboardContainer.style.animation = 'fadeInKeyboard 0.3s ease-out forwards';
        
        const interval = setInterval(() => {
            if (currentIndex >= name.length) {
                clearInterval(interval);
                setTimeout(showSignatureOverlay, 300);
                return;
            }
            
            const currentLetter = name[currentIndex];
            const key = document.querySelector(`[data-key="${currentLetter}"]`);
            
            if (key) {
                key.classList.add('active');
                
                if (currentIndex > 0) {
                    const prevLetter = name[currentIndex - 1];
                    const line = createLine(prevLetter, currentLetter);
                    if (line) {
                        lines.push(line);
                        setTimeout(() => line.classList.add('active'), 25);
                    }
                }
            }
            
            currentIndex++;
        }, 120);
    }
    
    function showSignatureOverlay() {
        // Fade out keyboard, fade in signature
        keyboardContainer.style.transition = 'opacity 0.8s ease';
        keyboardContainer.style.opacity = '0';
        
        signatureOverlay.style.opacity = '1';
        
        setTimeout(transitionToFinalLayout, 1000);
    }
    
    function transitionToFinalLayout() {
        // Hide keyboard container
        keyboardContainer.style.display = 'none';
        
        // Show hero content with animation
        heroContent.style.display = 'flex';
        heroContent.classList.add('animated');
        
        setTimeout(() => {
            heroContent.style.animation = 'slideInContent 0.6s ease-out forwards';
            heroContent.style.opacity = '1';
        }, 50);
    }
    
    // Start the animation after a brief delay
    setTimeout(animateKeyboard, 300);
    
    // Initially hide hero content
    heroContent.style.display = 'none';
});

// Handle window resize
window.addEventListener('resize', function() {
    const isMobileNow = window.innerWidth <= 768;
    const heroContent = document.getElementById('heroContent');
    const keyboardContainer = document.getElementById('keyboardContainer');
    
    if (isMobileNow) {
        keyboardContainer.style.display = 'none';
        heroContent.style.display = 'block';
        heroContent.style.textAlign = 'center';
        heroContent.style.opacity = '1';
    }
});