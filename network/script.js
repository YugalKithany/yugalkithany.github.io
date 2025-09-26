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
    const ctx1 = document.getElementById('chart1');
    if (ctx1) {
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
    }

    // Chart 2: Doughnut chart
    const ctx2 = document.getElementById('chart2');
    if (ctx2) {
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
}

// Chat input functionality with specific responses
function initChat() {
    const input = document.querySelector('.chat-input');
    const sendButton = document.querySelector('.send-button');
    const chatMain = document.querySelector('.chat-main');
    const inputContainer = document.querySelector('.input-container');
    
    if (!input || !sendButton || !chatMain) return;
    
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

// Fixed Section snapping functionality
function initSectionSnapping() {
    const sections = document.querySelectorAll('section');
    let currentSection = 0;
    let isSnapping = false;
    let lastScrollTime = 0;
    
    function snapToSection(sectionIndex) {
        if (sectionIndex >= 0 && sectionIndex < sections.length && !isSnapping) {
            isSnapping = true;
            currentSection = sectionIndex;
            
            sections[sectionIndex].scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
            
            document.body.setAttribute('data-section', sectionIndex);
            updateNavArrows();
            
            setTimeout(() => {
                isSnapping = false;
            }, 1000);
        }
    }
    
    function updateNavArrows() {
        const upArrow = document.getElementById('upArrow');
        const downArrow = document.getElementById('downArrow');
        
        if (upArrow && downArrow) {
            upArrow.style.display = currentSection === 0 ? 'none' : 'flex';
            downArrow.style.display = currentSection === sections.length - 1 ? 'none' : 'flex';
        }
    }
    
    function handleWheel(e) {
        if (isSnapping) {
            e.preventDefault();
            return;
        }
        
        const currentTime = Date.now();
        if (currentTime - lastScrollTime < 100) return; // Throttle wheel events
        lastScrollTime = currentTime;
        
        // For dashboard and paper sections, allow free scrolling
        if (sections[currentSection].classList.contains('dashboard-section') || 
            sections[currentSection].classList.contains('paper-section')) {
            return;
        }
        
        if (Math.abs(e.deltaY) > 50) {
            e.preventDefault();
            
            if (e.deltaY > 0 && currentSection < sections.length - 1) {
                snapToSection(currentSection + 1);
            } else if (e.deltaY < 0 && currentSection > 0) {
                snapToSection(currentSection - 1);
            }
        }
    }
    
    function handleScroll() {
        if (isSnapping) return;
        
        // Find the section that's most visible
        let mostVisible = 0;
        let maxVisibility = 0;
        
        sections.forEach((section, index) => {
            const rect = section.getBoundingClientRect();
            const visibility = Math.max(0, Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, 0));
            
            if (visibility > maxVisibility) {
                maxVisibility = visibility;
                mostVisible = index;
            }
        });
        
        if (mostVisible !== currentSection) {
            currentSection = mostVisible;
            document.body.setAttribute('data-section', currentSection);
            updateNavArrows();
        }
    }
    
    // Event listeners
    window.addEventListener('wheel', handleWheel, { passive: false });
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    // Initialize
    snapToSection(0);
}

function initNavArrows() {
    const upArrow = document.getElementById('upArrow');
    const downArrow = document.getElementById('downArrow');
    const sections = document.querySelectorAll('section');
    
    if (!upArrow || !downArrow) return;
    
    function getCurrentSection() {
        return parseInt(document.body.getAttribute('data-section')) || 0;
    }
    
    function snapToSection(sectionIndex) {
        if (sectionIndex >= 0 && sectionIndex < sections.length) {
            sections[sectionIndex].scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
            document.body.setAttribute('data-section', sectionIndex);
            updateNavArrows();
        }
    }
    
    function updateNavArrows() {
        const current = getCurrentSection();
        upArrow.style.display = current === 0 ? 'none' : 'flex';
        downArrow.style.display = current === sections.length - 1 ? 'none' : 'flex';
    }
    
    upArrow.addEventListener('click', () => {
        const current = getCurrentSection();
        if (current > 0) snapToSection(current - 1);
    });
    
    downArrow.addEventListener('click', () => {
        const current = getCurrentSection();
        if (current < sections.length - 1) snapToSection(current + 1);
    });
    
    // Initial update
    updateNavArrows();
}

// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Only init ThreeJS and Charts if their containers exist
    if (document.getElementById('threejs-container')) {
        initThreeJS();
    }
    if (document.getElementById('chart1') || document.getElementById('chart2')) {
        initCharts();
    }
    
    initNavArrows();
    initChat();
    initSectionSnapping();
});