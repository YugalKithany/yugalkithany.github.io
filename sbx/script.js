const portfolioData = {
    // Corner spaces
    jail: {
        category: "Unemployment",
        title: "",
        color: "#f39c12",
        details: `
        `
    },
    parking: {
        category: "FREE Parking",
        title: "",
        color: "#27ae60",
        details: ''

    },
    gojail: {
        category: "Go to Unemployment",
        title: "",
        color: "#8e44ad",
        details: `
        `
    },
    start: {
        category: "GO",
        title: "Collect Salary As You Pass",
        color: "#e74c3c",
        details: `
        `
    },
    railroad: {
        category: "Railroad",
        title: "",
        color: "#7f8c8d",
        details: `
        `
    },
    tax: {
        category: "TAX",
        title: "",
        color: "#1fb25a",
        details: `
        `
    },
    chance: {
        category: "Chance",
        title: "",
        color: "#f7941d",
        details: `
        `
    },
    cchest: {
        category: "Community Chest",
        title: "",
        color: "#aae0fa",
        details: `
        `
    },

    "future": {
        "category": "EXPERIENCE",
        "title": "Software Engineer Intern",
        "color": "#aae0fa",
        "details": "\n            <p><strong>Company:</strong> <strong></p>"
    },
    "mil": {
        "category": "EXPERIENCE",
        "title": "Embedded Systems Software Engineer Intern",
        "color": "#aae0fa",
        "details": "\n            <p><strong>Company:</strong> Milwaukee Tool <strong>Duration:</strong> May – Aug 2024</p>\n            <h4>Key Responsibilities</h4>\n            <ul>\n                <li>Developed data acquisition system effectively integrating with 5+ product lines, ensuring robust embedded integration.</li>\n                <li>Optimized system architecture with collaborative processes, providing live performance metrics with 12x less overhead.</li>\n            </ul>\n            <div class=\"tech-stack\">\n                <span class=\"tech-tag\">Embedded Systems</span>\n                <span class=\"tech-tag\">Data Acquisition</span>\n            </div>\n        "
    },
    "os": {
        "category": "EXPERIENCE",
        "title": "Operating Systems Course Assistant",
        "color": "#aae0fa",
        "details": "\n            <p><strong>Company:</strong> UIUC <strong>Duration:</strong> Aug 2023 – Aug 2024</p>\n            <h4>Key Responsibilities</h4>\n            <ul>\n                <li>Discussed key-note ideas about complex OS design topics for 200+ students. Grade exams and project submissions.</li>\n                <li>Mentored students in debugging x86 and C driver code to verse core concepts for Unix-based projects.</li>\n            </ul>\n            <div class=\"tech-stack\">\n                <span class=\"tech-tag\">x86 Assembly</span>\n                <span class=\"tech-tag\">C</span>\n                <span class=\"tech-tag\">Unix</span>\n                <span class=\"tech-tag\">Operating Systems</span>\n            </div>\n        "
    },
    "fh": {
        "category": "EXPERIENCE",
        "title": "Software Developer Intern",
        "color": "#aae0fa",
        "details": "\n            <p><strong>Company:</strong> Federated Hermes Global Trading and Technology <strong>Duration:</strong> May – Aug 2023</p>\n            <h4>Key Responsibilities</h4>\n            <ul>\n                <li>Modernized a SQL-based investment report into a real-time system, adding user-input functionality.</li>\n                <li>Optimized SQL queries and stored procedures, improving investment portfolio reporting efficiency by 30-40%.</li>\n            </ul>\n            <div class=\"tech-stack\">\n                <span class=\"tech-tag\">SQL</span>\n            </div>\n        "
    },
    "db": {
        "category": "EXPERIENCE",
        "title": "Branch Teller",
        "color": "#aae0fa",
        "details": "\n            <p><strong>Company:</strong> Dollar Bank, <strong>Duration:</strong> May 2022 – Dec 2023</p>\n            <h4>Key Responsibilities</h4>\n            <ul>\n                <li>Processed deposits, loans, and credit payments while ensuring compliance with financial regulations and audits.</li>\n            </ul>\n        "
    },
    "sm": {
        "category": "EXPERIENCE",
        "title": "Software Developer",
        "color": "#aae0fa",
        "details": "\n            <p><strong>Company:</strong> Prof. Sayan Mitra’s Reliable Autonomy Group <strong>Duration:</strong> Sep 2023 - Dec 2024</p>\n            <h4>Key Responsibilities</h4>\n            <ul>\n                <li>Developed PID controller to optimize drone velocity and safety for gate-based racing with RRT to guarantee stability.</li>\n                <li>Designed MPC algorithms on Airsim to execute algorithms for vision-based UAV tracking with depth estimation.</li>\n                <li>Enhanced control performance by increasing velocity 20% and reducing collisions 75% through PID and MPC tuning.</li>\n            </ul>\n            <div class=\"tech-stack\">\n                <span class=\"tech-tag\">Python</span>\n                <span class=\"tech-tag\">ROS</span>\n                <span class=\"tech-tag\">PID</span>\n                <span class=\"tech-tag\">MPC</span>\n                <span class=\"tech-tag\">Airsim</span>\n            </div>\n        "
    },
    "dkw": {
        "category": "EXPERIENCE",
        "title": "RTL Engineer",
        "color": "#aae0fa",
        "details": "\n            <p><strong>Company:</strong> Prof. Dong Kai Wang’s Computer Architecture Lab, <strong>Duration:</strong> Sep 2023 – Dec 2024</p>\n            <h4>Key Responsibilities</h4>\n            <ul>\n                <li>Developed synthesizable SystemVerilog modules for RISCV vector processors, improving cache latency by 20%.</li>\n                <li>Assessed 10+ open-source RTL libraries, enhancing hardware-software co-design for scalable vector processors.</li>\n            </ul>\n            <div class=\"tech-stack\">\n                <span class=\"tech-tag\">SystemVerilog</span>\n                <span class=\"tech-tag\">RISCV</span>\n                <span class=\"tech-tag\">RTL</span>\n                <span class=\"tech-tag\">RV32IM</span>\n            </div>\n        "
    },


    // Your existing and newly added projects, grouped under "PROJECTS"
    yulatin_llm: {
        category: "PROJECTS",
        title: "YuLatin: Latin Quote LLM",
        color: "#FFA07A", // A new color
        details: `
            <p>
                • Developed YuLatin LLM, an AI-powered model that analyzes emotions from user input and generates relevant Latin quotes based on detected sentiment.
            </p>
            <p>
                • Utilized Hugging Face's <a href="https://huggingface.co/SamLowe/roberta-base-go_emotions/">roberta-base-go_emotions</a> as a base model to classify emotions from user input, ensuring accurate sentiment detection, and match to Latin Quote.
            </p>
            <p>
                • Developed a full-stack application using Node.js (Express.js) for the backend and Railway for secure and scalable deployment.
            </p>
            <form action="https://latinllm.onrender.com//" target="_blank" class="form-container">
                <button class="expand-btn" type="submit">Latin LLM (~30 sec to render website)</button>
            </form>
            <div class="tech-stack">
                <span class="tech-tag">Node.js</span>
                <span class="tech-tag">Railway</span>
                <span class="tech-tag">Hugging Face API</span>
            </div>
        `
    },
    cnn: {
        category: "PROJECTS",
        title: "Convolution Neural Network for Image Classification",
        color: "#0072bb",
        details: `
            <p>A project focused on optimizing Convolutional Neural Networks using NVIDIA CUDA for image classification.</p>
            <h4>Features</h4>
            <ul>
                <li>Optimized forward-pass of convolution layers using NVIDIA CUDA Platform, developing software for processors with massively parallel computing resources.</li>
                <li>Evaluated performance with Nsight systems/computer profiling tools to refine CUDA kernels for optimal execution.</li>
                <li>Implemented a modified LeNet5 architecture for working with the Fashion MNIST dataset.</li>
                <li>Applied kernel optimization methods including unroll and shared-memory matrix multiply.</li>
                <li>Conducted kernel fusion for unrolling and multiplication to further enhance speed.</li>
                <li>Performed extensive sweeping of CUDA parameters to identify best performance values.</li>
                <li>Developed different kernel implementations to handle varying layer sizes effectively.</li>
            </ul>
            <div class="tech-stack">
                <span class="tech-tag">NVIDIA CUDA</span>
                <span class="tech-tag">Python</span>
                <span class="tech-tag">LeNet5</span>
                <span class="tech-tag">Fashion MNIST</span>
                <span class="tech-tag">Nsight</span>
            </div>
        `
    },
    mazegest: {
        category: "PROJECTS",
        title: "MazeGest: Gesture-controlled Maze Game",
        color: "#a0522d",
        details: `
            <p>
                • Developed MazeGest, an interactive maze game that leverages real-time hand gesture recognition using <a href="https://chuoling.github.io/mediapipe/solutions/hands.html/">MediaPipe Hands</a> to control in-game movement              
            </p>
            <p>
                • Utilized HTML5, CSS3, and vanilla JavaScript to dynamically generate maze layouts and implement responsive, collision-aware gameplay 
            </p>
            <form action="game/index.html" target="_blank" class="form-container">
                <button class="expand-btn" type="submit">MazeGest</button>
            </form>
            <div class="tech-stack">
                <span class="tech-tag">MediaPipe</span>
                <span class="tech-tag">HTML5</span>
                <span class="tech-tag">CSS3</span>
                <span class="tech-tag">JavaScript</span>
            </div>
        `
    },
    thesis: {
        category: "PROJECTS",
        title: "Control Algorithms for Vision-Based Navigation",
        color: "#9932CC", // A new color, choose as appropriate
        details: `
            <p>
                • Conducted two key drone experiments: (1) <strong>Drone tracking</strong>—an Ego drone followed a Target
                drone using a controller
                with trajectory tracking and YOLO-8-based perception for dynamic adaptation. (2) <strong>Gate
                navigation</strong>—compared PID and
                MPC controllers for optimal race performance, using both ground truth and relative gate positions.
            </p>
            <p>
                • Developed a predictive drone navigation algorithm using Model Predictive Control (MPC), optimizing flight
                paths and reducing trajectory deviation by 25% over PID controllers. Implemented in the CasADi framework
                with
                IPOPT solver for real-time drone racing scenarios.
            </p>
            <p>
                • Integrated Microsoft AirSim for high-fidelity testing of navigation algorithms and efficient dynamic pose
                estimation. Utilized <a href="https://msl.stanford.edu/papers/madaan_airsim_2020.pdf/">"AirSim Drone Racing Lab"</a> (Madaan et al. 2020) as base environment for gate racing.
            </p>
            <form action="https://github.com/YugalKithany/Undergraduate-Thesis" target="_blank" class="form-container">
                <button class="expand-btn" type="submit">GitHub Repo</button>
            </form>
            <div class="tech-stack">
                <span class="tech-tag">Python</span>
                <span class="tech-tag">YOLOv8</span>
                <span class="tech-tag">CasADi</span>
            </div>
        `
    },
    z486: {
        category: "PROJECTS",
        title: "Nonlinear Underactuated System",
        color: "#e67e22",
        details: `
            <p>This project focused on the control and stabilization of a Reaction Wheel Pendulum, a type of nonlinear underactuated system.</p>
            <h4>Features</h4>
            <ul>
                <li>Utilized two optical encoders to measure angles for calculating swing velocity and saturation of the Reaction Wheel Pendulum.</li>
                <li>Developed six controllers to stabilize and implement all components for the final robotic arm.</li>
                <li>Simulated a three-state feedback controller on MATLAB Simulink to stabilize the rotor's velocity.</li>
                <li>Implemented error control to instantiate the controller onto the Reaction Wheel Pendulum.</li>
                <li>The design process encompassed comprehensive system identification, model validation, and design validation.</li>
            </ul>
            <div class="tech-stack">
                <span class="tech-tag">MATLAB</span>
                <span class="tech-tag">Simulink</span>
                <span class="tech-tag">Control Systems</span>
                <span class="tech-tag">Robotics</span>
            </div>
        `
    },
    unix_kernel: {
        category: "PROJECTS",
        title: "Single Core Unix x86 Kernel",
        color: "#aae0fa",
        details: `
            <p>
                • Implemented device drivers for keyboard, RTC, Terminal, TUX
                controller, Process Control Blocks in x86 Assembly.
            </p>
            <p>
                • Introduced compatibility for Linux commands shell (<10 concurrent), ls, cat, and grep on Posix style
                shell with keyboard comparability.
            </p>
            <p>
                • Designed paging-based virtual memory, context switching, read only filesystem, round-robin scheduler.
            </p>
            <div class="tech-stack">
                <span class="tech-tag">C99</span>
                <span class="tech-tag">Qemu</span>
                <span class="tech-tag">x86 Assembly</span>
            </div>
        `
    },
    ur3: {
        category: "PROJECTS",
        title: "UR3 Robotic Knight's Tour",
        color: "#1fb25a",
        details: `
            <p>A robotic project implementing the Knight's Tour problem on a physical board using a UR3 robot.</p>
            <h4>Features</h4>
            <ul>
                <li>Implemented an Open Knight's Tour on a physical board using a modified Hamiltonian Path Algorithm with a heuristic prioritizing moves with the fewest remaining options, optimizing for linear time complexity.</li>
                <li>Integrated UR3 robot control with inverse kinematics, manually mapped XYZ positions for precise movement, and used blob detection with a suction mechanism to identify and manipulate the knight.</li>
                <li>Utilized ROS and ROS Bags for real-time execution, synchronized motion control, and data logging, ensuring accurate tracking and debugging of robotic operations.</li>
            </ul>
            <div class="tech-stack">
                <span class="tech-tag">Python</span>
                <span class="tech-tag">ROS</span>
                <span class="tech-tag">UR3 Robot</span>
            </div>
        `
    },
    z225: {
        category: "PROJECTS",
        title: "Open Flights Airplane Path Optimization",
        color: "#3498db",
        details: `
            <p>A program developed to find the shortest flight paths between airports using the OpenFlights dataset.</p>
            <h4>Features</h4>
            <ul>
                <li>Developed a program to find the shortest path between airports using the OpenFlights dataset.</li>
                <li>Created a weighted directed graph using adjacency lists, calculating distances between vertices from routes.dat.</li>
                <li>Implemented both Floyd-Warshall and A* algorithms for efficient shortest path discovery.</li>
                <li>Performed data cleaning and graph construction, utilizing DFS to validate path existence between airports.</li>
            </ul>
            <div class="tech-stack">
                <span class="tech-tag">C++</span>
                <span class="tech-tag">Docker</span>
                <span class="tech-tag">Graph Algorithms</span>
                <span class="tech-tag">Data Structures</span>
            </div>
            <p><a href="https://github.com/YugalKithany/OpenFlights" target="_blank">View on GitHub</a></p>
        `
    },
    am_receiver: {
        category: "PROJECTS",
        title: "Superheterodyne AM Receiver",
        color: "#aae0fa",
        details: `
            <p>
                • Built receiver on breadboard with RF/IF amplifier, Mixer,
                Demodulator, local oscillator, and audio amplifier elements.
            </p>
            <p>
                • Designed digital filter to demodulate AM signal, replace IF signal
                with soundcard-based sampler receiver, and play audio on speakers
                for software radio. Measured AM receiver performance, sensitivity to
                noise, and image rejection.
            </p>
            <div class="tech-stack">
                <span class="tech-tag">Circuit Design</span>
                <span class="tech-tag">Signal Processing</span>
                <span class="tech-tag">Analog Electronics</span>
            </div>
        `
    },
    fpga_projects: {
        category: "PROJECTS",
        title: "System Verilog Projects on DE10-Lite FPGA board",
        color: "#aae0fa",
        details: `
            <p>
                • Designed and built digital systems with TTL and FPGAs. Debugged
                on Model Sim and Signal Tap Logic Analyzer.
            </p>
            <p>
                • Replicated classical Tetris with NIOS II and SOC, using 32-bit
                modified Harvard RISC-V architecture. The game was outputted on
                monitor via VGA output. Utilized Electronic Design Automation to
                synthesize logic.
            </p>
            <p>
                • Developed three-stage (fetch, decode, execute) SLC3 processor
                for LC3 ISA (ADD, NOT, BR, STR, LDR). Created CPU, SRAM, IR of
                processor on breadboard. A software implementation done on Quartus
                Prime with System Verilog.
            </p>
            <div class="tech-stack">
                <span class="tech-tag">SystemVerilog</span>
                <span class="tech-tag">Quartus Prime</span>
                <span class="tech-tag">ModelSim</span>
            </div>
        `
    },
    multi_cycle_processor: {
        category: "PROJECTS",
        title: "Multi-Cycle RISC-V Processor",
        color: "#a0522d",
        details: `
            <p>
                • Designed multi-cycle processor using the RISC-V instruction set
                and standard CPU data path using Verilog and Verdi.
            </p>
            <p>
                • Implemented register-immediate instructions, load and store
                memory instructions, conditional branch operations.
            </p>
            <p>
                • Developed test bench to run sequence of instructions, and to run
                RISC-V assembly. Verified design using RVFI monitor and SPIKE
            </p>
            <div class="tech-stack">
                <span class="tech-tag">SystemVerilog</span>
                <span class="tech-tag">Synopsys</span>
            </div>
        `
    },
    ooo_processor: {
        category: "PROJECTS",
        title: "Speculative Out-of-Order RISC-V Processor",
        color: "#4682B4", // A new color
        details: `
            <p>
                • Designing and verifying ERR out-of-order processor, implementing RV32IM ISA with FP and Mult
                extensions.
            </p>
            <p>
                • Developed arbiter for Icache and Dcache, stride prefetchers, and cacheline adapter for efficient two
                stage cache-DRAM integration.
            </p>
            <p>
                • Optimizing design with early branch recovery, Perceptron branch predictor with BTB, and split
                load-store queue.
            </p>
            <p>
                • Below is a VERY high level overview of the system.
            </p>
            <button class="expand-btn" onclick="toggleExpand(this)">Expand PDF</button>
            <div class="tech-stack">
                <span class="tech-tag">SystemVerilog</span>
                <span class="tech-tag">Synopsys</span>
                <span class="tech-tag">Verilator</span>
            </div>
            <div class="pdf-container">
                <embed src="images/ERR block diagram.pdf" type="application/pdf" />
            </div>
        `
    },
    RTAccelerator: {
        "category": "PROJECTS",
        "title": "RTAccelerator: A RISC-V Accelerator for Triangle Intersection in Ray Tracing",
        "color": "#0072bb",
        "details": "\n            <p>This project implements a hardware accelerator for the ray-triangle intersection component of a ray tracing engine, built on a RISC-V core with floating-point support. The accelerator achieves a 70.8% performance improvement and 69.2% energy reduction over baseline execution. </p>\n            <h4>Features</h4>\n            <ul>\n                <li>Simulates light by casting rays through pixels and determining their interactions with 3D triangle meshes. </li>\n                <li>Presents a hardware accelerator for the Ray-Triangle intersection test, built on a RISC-V core. </li>\n                <li>Utilizes a Finite State Machine and floating-point units for parallel computation, improving performance by over 70% while significantly reducing energy consumption. </li>\n                <li>The Ray-Triangle Intersection algorithm is divided into two stages: the ray-plane intersection phase and the barycentric coordinate phase. </li>\n                <li>Hardware acceleration is achieved by creating a module with an FSM closely following the algorithm with minimum floating-point computational units to enhance parallelized derivations. </li>\n                <li>Requires two custom instructions for processor-accelerator communication: RTI.S (starts computation) and RTILD.S (loads 15 floating-point numbers from memory). </li>\n                <li>Achieves a performance improvement of 70.8% and an energy usage improvement of 69.2% with constant power consumption. </li>\n            </ul>\n            <div class=\"tech-stack\">\n                <span class=\"tech-tag\">RISC-V</span>\n                <span class=\"tech-tag\">Floating-Point Units</span>\n                <span class=\"tech-tag\">Finite State Machine</span>\n                <span class=\"tech-tag\">Synopsys Design Compiler</span>\n                <span class=\"tech-tag\">Verilator</span>\n                <span class=\"tech-tag\">VCS / Verdi</span>\n                <span class=\"tech-tag\">fpnew</span>\n            </div>\n            <p><a href=\"https://github.com/YugalKithany/RTAccelerator\" target=\"_blank\">View on GitHub</a></p>\n        "
    }
};

function showModal(propertyId) {
    const property = portfolioData[propertyId];
    if (!property) return;

    const modal = document.getElementById('modal');
    const modalHeader = document.getElementById('modal-header');
    const modalCategory = document.getElementById('modal-category');
    const modalTitle = document.getElementById('modal-title');
    const modalDetails = document.getElementById('modal-details');

    modalHeader.style.background = property.color;
    modalCategory.textContent = property.category;
    modalTitle.textContent = property.title;
    modalDetails.innerHTML = property.details;

    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// Function to toggle PDF expansion (for OOO Processor)
function toggleExpand(button) {
    const pdfContainer = button.closest('.wrapper').nextElementSibling; // Assuming pdf-container is sibling of wrapper
    if (pdfContainer && pdfContainer.classList.contains('pdf-container')) {
        pdfContainer.style.display = pdfContainer.style.display === 'block' ? 'none' : 'block';
        button.textContent = pdfContainer.style.display === 'block' ? 'Collapse PDF' : 'Expand PDF';
    }
}