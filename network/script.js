// Three.js 3D Background Animation
function initThreeJS() {
    const container = document.getElementById('threejs-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000, 0);
    container.appendChild(renderer.domElement);

    // Create floating geometric shapes
    const geometries = [
        new THREE.BoxGeometry(1, 1, 1),
        new THREE.SphereGeometry(0.7, 8, 8),
        new THREE.ConeGeometry(0.7, 1.5, 8)
    ];

    const materials = [
        new THREE.MeshBasicMaterial({ color: 0x4f46e5, wireframe: true }),
        new THREE.MeshBasicMaterial({ color: 0x7c3aed, wireframe: true }),
        new THREE.MeshBasicMaterial({ color: 0x06b6d4, wireframe: true })
    ];

    const meshes = [];
    for (let i = 0; i < 20; i++) {
        const geometry = geometries[Math.floor(Math.random() * geometries.length)];
        const material = materials[Math.floor(Math.random() * materials.length)];
        const mesh = new THREE.Mesh(geometry, material);
        
        mesh.position.x = (Math.random() - 0.5) * 50;
        mesh.position.y = (Math.random() - 0.5) * 30;
        mesh.position.z = (Math.random() - 0.5) * 30;
        
        mesh.rotation.x = Math.random() * Math.PI;
        mesh.rotation.y = Math.random() * Math.PI;
        
        scene.add(mesh);
        meshes.push(mesh);
    }

    camera.position.z = 20;

    function animate() {
        requestAnimationFrame(animate);
        
        meshes.forEach((mesh, index) => {
            mesh.rotation.x += 0.005 + index * 0.001;
            mesh.rotation.y += 0.003 + index * 0.0005;
            mesh.position.y += Math.sin(Date.now() * 0.001 + index) * 0.001;
        });

        renderer.render(scene, camera);
    }
    animate();

    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// Initialize Chart.js charts
function initCharts() {
    // Chart 1: Line chart
    const ctx1 = document.getElementById('chart1').getContext('2d');
    new Chart(ctx1, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Performance',
                data: [0, 15, 30, 45, 60, 90],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: 'white' }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: 'white' },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                },
                x: {
                    ticks: { color: 'white' },
                    grid: { color: 'rgba(255,255,255,0.1)' }
                }
            }
        }
    });

    // Chart 2: Doughnut chart
    const ctx2 = document.getElementById('chart2').getContext('2d');
    new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: ['AI/ML', 'Data Science', 'Web Dev', 'Mobile'],
            datasets: [{
                data: [35, 25, 25, 15],
                backgroundColor: [
                    '#4f46e5',
                    '#7c3aed',
                    '#06b6d4',
                    '#10b981'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { 
                        color: 'white',
                        padding: 20
                    }
                }
            }
        }
    });
}

// Chat input functionality with specific responses
function initChat() {
    const input = document.querySelector('.chat-input');
    const sendButton = document.querySelector('.send-button');
    const chatMain = document.querySelector('.chat-main');
    const inputContainer = document.querySelector('.input-container');
    
    let messageCount = 0;
    let tokensExhausted = false;
    
    function adjustTextareaHeight() {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    }
    
    input.addEventListener('input', adjustTextareaHeight);
    
    function addMessage(content, isUser = false, isYoutube = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message';
        
        if (isUser) {
            messageDiv.innerHTML = `
                <div class="message-avatar user-avatar">😊</div>
                <div class="message-content">
                    <p>${content}</p>
                </div>
            `;
        } else if (isYoutube) {
            messageDiv.innerHTML = `
                <div class="message-avatar assistant-avatar">🤖</div>
                <div class="message-content">
                    <div class="youtube-preview">
                        <a href="https://www.youtube.com/watch?v=9AjkUyX0rVw" target="_blank">
                            <img src="https://img.youtube.com/vi/9AjkUyX0rVw/maxresdefault.jpg" alt="We Are The World" class="youtube-thumbnail">
                            <div class="youtube-info">
                                <div class="youtube-title">We Are The World</div>
                                <div class="youtube-channel">USA for Africa</div>
                            </div>
                        </a>
                    </div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-avatar assistant-avatar">🤖</div>
                <div class="message-content">
                    <p>${content}</p>
                </div>
            `;
        }
        
        chatMain.appendChild(messageDiv);
        chatMain.scrollTop = chatMain.scrollHeight;
    }
    
    function sendMessage() {
        if (tokensExhausted) return;
        
        const message = input.value.trim();
        if (!message) return;
        
        // Add user message
        addMessage(message, true);
        input.value = '';
        adjustTextareaHeight();
        
        // Simulate typing delay
        setTimeout(() => {
            if (messageCount === 0) {
                // First response: "Tokens aren't cheap..."
                addMessage("Tokens aren't cheap...");
                messageCount++;
            } else if (messageCount === 1) {
                // Second response: YouTube link
                addMessage("", false, true);
                messageCount++;
                
                // After YouTube response, disable input and show "Out of Tokens"
                setTimeout(() => {
                    tokensExhausted = true;
                    input.disabled = true;
                    sendButton.disabled = true;
                    input.placeholder = "Out of Tokens...";
                    input.style.backgroundColor = "#1a1a1a";
                    input.style.color = "#666";
                    sendButton.style.color = "#666";
                    sendButton.style.cursor = "not-allowed";
                }, 500);
            }
        }, 1000);
    }
    
    sendButton.addEventListener('click', sendMessage);
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// Section snapping functionality
let isScrolling = false;
let scrollTimeout;

// Replace the initSectionSnapping function with this updated version:

function initSectionSnapping() {
    const sections = document.querySelectorAll('section');
    let currentSection = 0;
    const snapThreshold = 100; // pixels to scroll before snapping
    
    function snapToSection(sectionIndex) {
        if (sectionIndex >= 0 && sectionIndex < sections.length) {
            sections[sectionIndex].scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
            document.body.setAttribute('data-section', sectionIndex);
            currentSection = sectionIndex;
        }
    }
    
    // Special handling for the paper section (allow free scrolling)
    function isPaperSection(sectionIndex) {
        return sections[sectionIndex] && sections[sectionIndex].classList.contains('paper-section');
    }
    
    function handleScroll() {
        if (isScrolling) return;
        
        const scrollTop = window.scrollY;
        let targetSection = currentSection;
        
        // Find which section we're currently in
        sections.forEach((section, index) => {
            const sectionTop = section.offsetTop;
            const sectionBottom = sectionTop + section.offsetHeight;
            
            if (scrollTop >= sectionTop - window.innerHeight/3 && 
                scrollTop < sectionBottom - window.innerHeight/3) {
                targetSection = index;
            }
        });
        
        // If we're in the paper section, allow free scrolling
        if (isPaperSection(targetSection)) {
            currentSection = targetSection;
            document.body.setAttribute('data-section', targetSection);
            return;
        }
        
        // For other sections, check if we've scrolled enough to snap
        const currentSectionElement = sections[currentSection];
        const currentSectionTop = currentSectionElement.offsetTop;
        const scrollDistance = Math.abs(scrollTop - currentSectionTop);
        
        if (scrollDistance > snapThreshold && targetSection !== currentSection) {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                isScrolling = true;
                snapToSection(targetSection);
                setTimeout(() => {
                    isScrolling = false;
                }, 800);
            }, 150);
        }
    }
    
    function handleWheel(e) {
        // Allow free scrolling in paper section
        if (isPaperSection(currentSection)) {
            return;
        }
        
        if (isScrolling) {
            e.preventDefault();
            return;
        }
        
        // Only snap if scroll is significant enough
        if (Math.abs(e.deltaY) > 10) {
            e.preventDefault();
            isScrolling = true;
            
            if (e.deltaY > 0 && currentSection < sections.length - 1) {
                snapToSection(currentSection + 1);
            } else if (e.deltaY < 0 && currentSection > 0) {
                snapToSection(currentSection - 1);
            }
            
            setTimeout(() => {
                isScrolling = false;
            }, 800);
        }
    }
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('wheel', handleWheel, { passive: false });
    
    // Initialize with first section
    snapToSection(0);
}
// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', () => {
    initThreeJS();
    initCharts();
    initChat();
    initSectionSnapping();
});

// Smooth scroll effect on sections - removed since we now have section snapping
// window.addEventListener('scroll', () => {
//     const sections = document.querySelectorAll('section');
//     sections.forEach((section, index) => {
//         const rect = section.getBoundingClientRect();
//         const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
        
//         if (isVisible) {
//             section.style.opacity = '1';
//             section.style.transform = 'translateY(0)';
//         } else {
//             section.style.opacity = '0.8';
//             section.style.transform = 'translateY(20px)';
//         }
//     });
// });
