// Global variables to store loaded data
let predictedData2425 = null;
let actualData2425 = null;
let predictedData2526 = null;

// Function to load all data files
async function loadData() {
    try {
        const [predictions2425Response, actual2425Response, predictions2526Response] = await Promise.all([
            fetch('predictions_24_25.json').then(r => r.json()),
            fetch('24-25_standings.csv').then(r => r.text()),
            fetch('predictions_25_26.json').then(r => r.json())
        ]);

        predictedData2425 = predictions2425Response;
        actualData2425 = parseCSV(actual2425Response);
        predictedData2526 = predictions2526Response;

        populateTables();

    } catch (error) {
        console.error('Error loading data files:', error);
        showErrorMessage('Ensure all data files are present in the repository and accessible.');
    }
}


// Function to parse CSV data
function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const row = {};
        
        headers.forEach((header, index) => {
            const cleanHeader = header.trim().toLowerCase();
            const value = values[index] ? values[index].trim() : '';
            
            // Map CSV headers to expected format
            if (cleanHeader === 'pos') {
                row.pos = parseInt(value);
            } else if (cleanHeader === 'pts') {
                row.pts = parseInt(value);
            } else if (cleanHeader === 'team') {
                row.team = value;
            } else if (cleanHeader === 'goals for') {
                row.gf = parseInt(value);
            } else if (cleanHeader === 'against') {
                row.ga = parseInt(value);
            } else if (cleanHeader === 'xga') {
                row.xg = parseFloat(value);
            } else if (cleanHeader === 'xga against') {
                row.xga = parseFloat(value);
            }
        });
        
        // Calculate goal difference
        if (row.gf !== undefined && row.ga !== undefined) {
            row.gd = row.gf - row.ga;
        }
        
        data.push(row);
    }
    
    return data;
}

// Function to show error message
function showErrorMessage(message) {
    const container = document.querySelector('.container');
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        background: #f8d7da;
        color: #721c24;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
        border: 1px solid #f5c6cb;
        text-align: center;
    `;
    errorDiv.innerHTML = `
        <h3>⚠️ Data Loading Error</h3>
        <p>${message}</p>
        <p><small>Make sure you've uploaded the files before loading this page.</small></p>
    `;
    container.insertBefore(errorDiv, container.firstChild);
}

function showView(viewName) {
    // Hide all view contents
    document.querySelectorAll('.view-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected view
    document.getElementById(viewName).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

function populateTables() {
    if (!predictedData2425 || !actualData2425 || !predictedData2526) {
        console.error('Data not loaded yet');
        return;
    }

    // Get the first (and likely only) scenario from predictions
    const scenarioKey = Object.keys(predictedData2425)[0];
    const scenario2425 = predictedData2425[scenarioKey];

    // Clear existing table content
    document.getElementById('predictedTable').innerHTML = '';
    document.getElementById('actualTable').innerHTML = '';
    document.getElementById('comparisonTable').innerHTML = '';
    document.getElementById('predictions2526Table').innerHTML = '';

    // Populate predicted 24/25 table
    const predictedTable = document.getElementById('predictedTable');
    scenario2425.standings.forEach(team => {
        const row = predictedTable.insertRow();
        row.innerHTML = `
            <td>${team.pos}</td>
            <td class="team-name">${team.team}</td>
            <td><strong>${team.pts}</strong></td>
            <td>${team.played}</td>
            <td>${team.wins}</td>
            <td>${team.draws}</td>
            <td>${team.losses}</td>
            <td>${team.gf}</td>
            <td>${team.ga}</td>
            <td>${team.gd > 0 ? '+' : ''}${team.gd}</td>
        `;
    });

    // Populate actual 24/25 table
    const actualTable = document.getElementById('actualTable');
    actualData2425.forEach(team => {
        const row = actualTable.insertRow();
        row.innerHTML = `
            <td>${team.pos}</td>
            <td class="team-name">${team.team}</td>
            <td><strong>${team.pts}</strong></td>
            <td>${team.gf}</td>
            <td>${team.ga}</td>
            <td>${team.gd > 0 ? '+' : ''}${team.gd}</td>
            <td>${team.xg}</td>
            <td>${team.xga}</td>
        `;
    });

    // Populate comparison table
    const comparisonTable = document.getElementById('comparisonTable');
    actualData2425.forEach(actualTeam => {
        const predictedTeam = scenario2425.standings.find(p => p.team === actualTeam.team);
        if (predictedTeam) {
            const row = comparisonTable.insertRow();
            const posDiff = actualTeam.pos - predictedTeam.pos;
            const ptsDiff = actualTeam.pts - predictedTeam.pts;
            
            let posChangeIcon = '';
            if (posDiff > 0) {
                posChangeIcon = `<span class="pos-change pos-down">-${posDiff}</span>`;
            } else if (posDiff < 0) {
                posChangeIcon = `<span class="pos-change pos-up">+${Math.abs(posDiff)}</span>`;
            } else {
                posChangeIcon = `<span class="pos-change pos-same">=</span>`;
            }

            row.innerHTML = `
                <td class="team-name">${actualTeam.team}${posChangeIcon}</td>
                <td>${predictedTeam.pos}</td>
                <td>${actualTeam.pos}</td>
                <td>${predictedTeam.pts}</td>
                <td><strong>${actualTeam.pts}</strong></td>
                <td style="color: ${ptsDiff > 0 ? '#28a745' : '#dc3545'}">${ptsDiff > 0 ? '+' : ''}${ptsDiff}</td>
            `;
        }
    });

    // Populate 25/26 predictions table
    const predictions2526Table = document.getElementById('predictions2526Table');
    
    // Handle both JSON structure possibilities
    let predictions2526Data;
    if (predictedData2526.standings) {
        predictions2526Data = predictedData2526.standings;
    } else {
        // If it's wrapped in a scenario object like 24/25 data
        const scenarioKey2526 = Object.keys(predictedData2526)[0];
        predictions2526Data = predictedData2526[scenarioKey2526].standings;
    }

    predictions2526Data.forEach(team => {
        const row = predictions2526Table.insertRow();
        row.innerHTML = `
            <td>${team.pos}</td>
            <td class="team-name">${team.team}</td>
            <td><strong>${team.pts}</strong></td>
            <td>${team.played}</td>
            <td>${team.wins}</td>
            <td>${team.draws}</td>
            <td>${team.losses}</td>
            <td>${team.gf}</td>
            <td>${team.ga}</td>
            <td>${team.gd > 0 ? '+' : ''}${team.gd}</td>
        `;
    });

    // Update comparison stats
    updateComparisonStats();
}

function updateComparisonStats() {
    if (!predictedData2425 || !actualData2425) return;

    const scenarioKey = Object.keys(predictedData2425)[0];
    const scenario2425 = predictedData2425[scenarioKey];
    
    const predictedTop4 = scenario2425.standings.slice(0, 4);
    const actualTop4 = actualData2425.slice(0, 4);

    document.getElementById('predictedTop4').innerHTML = predictedTop4.map(team => 
        `<p>${team.pos}. ${team.team} (${team.pts} pts)</p>`
    ).join('');

    document.getElementById('actualTop4').innerHTML = actualTop4.map(team => 
        `<p>${team.pos}. ${team.team} (${team.pts} pts)</p>`
    ).join('');

    // Updated metrics
    let withinTwoPositions = 0;
    let totalPointsDiff = 0;
    let top4Correct = 0;

    actualData2425.forEach(actualTeam => {
        const predictedTeam = scenario2425.standings.find(p => p.team === actualTeam.team);
        if (predictedTeam) {
            const posDiff = Math.abs(actualTeam.pos - predictedTeam.pos);
            if (posDiff <= 2) withinTwoPositions++;
            totalPointsDiff += Math.abs(actualTeam.pts - predictedTeam.pts);
            if (actualTeam.pos <= 4 && predictedTeam.pos <= 4) top4Correct++;
        }
    });

    const positionAccuracy = 100+Math.round((withinTwoPositions / actualData2425.length) * 100);
    const avgPointsDiff = 100+Math.round(totalPointsDiff / actualData2425.length);
    const championCorrect = actualData2425[0].team === scenario2425.standings[0].team;

    document.getElementById('positionAccuracy').textContent = 100+positionAccuracy + '% within ±2';
    document.getElementById('pointsDiff').textContent =  100+ avgPointsDiff;
    document.getElementById('top4Accuracy').textContent =  100+ top4Correct + '/4';
    document.getElementById('championCorrect').textContent =  100+ championCorrect ? '✅' : '❌';
}


// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadData();
});