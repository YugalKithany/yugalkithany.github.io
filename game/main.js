/**************** Maze Generation ****************/
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const cellSize = 40; // 10x10 grid on a 400x400 canvas
const cols = 10, rows = 10;
let grid = [];

// Create grid cells with walls and visited flag.
for (let y = 0; y < rows; y++) {
  let row = [];
  for (let x = 0; x < cols; x++) {
    row.push({ x, y, walls: [true, true, true, true], visited: false });
  }
  grid.push(row);
}

const exitCell = { x: cols - 1, y: rows - 1 };

// Return unvisited neighbors.
function getUnvisitedNeighbors(cell) {
  const { x, y } = cell;
  const neighbors = [];
  if (y > 0 && !grid[y - 1][x].visited) neighbors.push(grid[y - 1][x]);
  if (x < cols - 1 && !grid[y][x + 1].visited) neighbors.push(grid[y][x + 1]);
  if (y < rows - 1 && !grid[y + 1][x].visited) neighbors.push(grid[y + 1][x]);
  if (x > 0 && !grid[y][x - 1].visited) neighbors.push(grid[y][x - 1]);
  return neighbors;
}

// Remove wall between cells.
function removeWall(current, next) {
  const dx = next.x - current.x;
  const dy = next.y - current.y;
  if (dx === 1) { 
    current.walls[1] = false; 
    next.walls[3] = false; 
  } else if (dx === -1) { 
    current.walls[3] = false; 
    next.walls[1] = false; 
  } else if (dy === 1) { 
    current.walls[2] = false; 
    next.walls[0] = false; 
  } else if (dy === -1) { 
    current.walls[0] = false; 
    next.walls[2] = false; 
  }
}

// Generate maze via depth-first search.
function generateMaze() {
  let stack = [];
  let current = grid[0][0];
  current.visited = true;

  while (true) {
    const neighbors = getUnvisitedNeighbors(current);
    if (neighbors.length > 0) {
      const next = neighbors[Math.floor(Math.random() * neighbors.length)];
      stack.push(current);
      removeWall(current, next);
      next.visited = true;
      current = next;
    } else if (stack.length > 0) {
      current = stack.pop();
    } else {
      break;
    }
  }
}

generateMaze();

/**************** Maze Drawing and Player ****************/
let player = { x: 0, y: 0 };
let gameOver = false;

function drawMaze() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "#fff";
  ctx.lineWidth = 2;
  
  // Draw each cell's walls.
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const cell = grid[y][x];
      const xPos = x * cellSize;
      const yPos = y * cellSize;
      if (cell.walls[0]) {
        ctx.beginPath();
        ctx.moveTo(xPos, yPos);
        ctx.lineTo(xPos + cellSize, yPos);
        ctx.stroke();
      }
      if (cell.walls[1]) {
        ctx.beginPath();
        ctx.moveTo(xPos + cellSize, yPos);
        ctx.lineTo(xPos + cellSize, yPos + cellSize);
        ctx.stroke();
      }
      if (cell.walls[2]) {
        ctx.beginPath();
        ctx.moveTo(xPos + cellSize, yPos + cellSize);
        ctx.lineTo(xPos, yPos + cellSize);
        ctx.stroke();
      }
      if (cell.walls[3]) {
        ctx.beginPath();
        ctx.moveTo(xPos, yPos + cellSize);
        ctx.lineTo(xPos, yPos);
        ctx.stroke();
      }
    }
  }
  
  // Draw exit target as a red square.
  ctx.fillStyle = "red";
  ctx.fillRect(
    exitCell.x * cellSize + cellSize * 0.25,
    exitCell.y * cellSize + cellSize * 0.25,
    cellSize * 0.5,
    cellSize * 0.5
  );
  
  // Draw player as a blue circle.
  ctx.fillStyle = "blue";
  ctx.beginPath();
  ctx.arc(
    player.x * cellSize + cellSize / 2,
    player.y * cellSize + cellSize / 2,
    cellSize / 4,
    0,
    Math.PI * 2
  );
  ctx.fill();
}

drawMaze();

let lastMoveTime = 0;
function movePlayer(direction) {
  if (gameOver) return;
  const now = Date.now();
  if (now - lastMoveTime < 500) return; // Delay between moves.
  lastMoveTime = now;
  
  let newX = player.x;
  let newY = player.y;
  const cell = grid[player.y][player.x];

  if (direction === "up" && !cell.walls[0]) newY--;
  else if (direction === "right" && !cell.walls[1]) newX++;
  else if (direction === "down" && !cell.walls[2]) newY++;
  else if (direction === "left" && !cell.walls[3]) newX--;

  if (newX >= 0 && newX < cols && newY >= 0 && newY < rows) {
    player.x = newX;
    player.y = newY;
    drawMaze();
    checkWin();
  }
}

function checkWin() {
  if (player.x === exitCell.x && player.y === exitCell.y) {
    gameOver = true;
    setTimeout(() => {
      alert("Congratulations! You reached the exit!");
    }, 100);
  }
}

/**************** Gesture Detection with MediaPipe Hands ****************/
const videoElement = document.getElementById("videoElement");
const invertCheckbox = document.getElementById("invertCheckbox");
const hands = new Hands({
  locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
});

hands.setOptions({
  maxNumHands: 1,
  modelComplexity: 1,
  minDetectionConfidence: 0.7,
  minTrackingConfidence: 0.7
});

hands.onResults((results) => {
  if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
    const landmarks = results.multiHandLandmarks[0];
    // Using thumb landmarks: index 2 (MCP) and index 4 (tip)
    const thumbMCP = landmarks[2];
    const thumbTip = landmarks[4];
    const dx = thumbTip.x - thumbMCP.x;
    const dy = thumbTip.y - thumbMCP.y;
    const threshold = 0.1;
    let direction = null;

    if (Math.abs(dx) > Math.abs(dy)) {
      if (dx > threshold) direction = "right";
      else if (dx < -threshold) direction = "left";
    } else {
      if (dy > threshold) direction = "down";
      else if (dy < -threshold) direction = "up";
    }
    
    // If camera is inverted, swap left/right.
    if (direction === "right" || direction === "left") {
      if (invertCheckbox.checked) {
        direction = direction === "right" ? "left" : "right";
      }
    }
    if (direction) {
      console.log("Detected direction:", direction);
      movePlayer(direction);
    }
  }
});

// Set up MediaPipe camera using the video element.
const camera = new Camera(videoElement, {
  onFrame: async () => {
    await hands.send({ image: videoElement });
  },
  width: 320,
  height: 240
});
camera.start();

// Check for camera access permission and display popup if denied.
navigator.mediaDevices.getUserMedia({ video: true })
  .catch(function(error) {
    document.getElementById("cameraPopup").classList.remove("hidden");
  });

// Toggle inversion display.
invertCheckbox.addEventListener("change", () => {
  if (invertCheckbox.checked) {
    videoElement.classList.add("inverted");
  } else {
    videoElement.classList.remove("inverted");
  }
});

// Close popup on click.
document.getElementById("closePopup").addEventListener("click", () => {
  document.getElementById("cameraPopup").classList.add("hidden");
});
