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

    // Enhanced metrics for better presentation
    let perfectPositionMatches = 0;
    let withinThreePositions = 0; // Added for a broader accuracy metric
    let totalPointsDiff = 0;
    let top4TeamsPredictedCorrectly = 0; // Counts how many of the *actual* top 4 were *also* predicted in the top 4
    let championCorrect = actualData2425[0].team === scenario2425.standings[0].team;
    let europeanQualificationAccuracy = 0; // For positions 1-6 (Champions League + Europa League)
    let relegationZoneAccuracy = 0; // For bottom 3 positions

    const totalTeams = actualData2425.length; // Assuming all teams are present in both lists

    actualData2425.forEach(actualTeam => {
        const predictedTeam = scenario2425.standings.find(p => p.team === actualTeam.team);
        if (predictedTeam) {
            const posDiff = Math.abs(actualTeam.pos - predictedTeam.pos);
            
            if (posDiff === 0) perfectPositionMatches++; // Count exact matches
            if (posDiff <= 2) withinTwoPositions++;
            if (posDiff <= 3) withinThreePositions++; // New metric
            
            totalPointsDiff += Math.abs(actualTeam.pts - predictedTeam.pts);

            // Check for top 4 prediction accuracy
            const isActualTop4 = actualTeam.pos <= 4;
            const isPredictedTop4 = predictedTeam.pos <= 4;
            if (isActualTop4 && isPredictedTop4) {
                top4TeamsPredictedCorrectly++;
            }

            // European Qualification Accuracy (positions 1-6)
            const isActualEuro = actualTeam.pos >= 1 && actualTeam.pos <= 6;
            const isPredictedEuro = predictedTeam.pos >= 1 && predictedTeam.pos <= 6;
            if (isActualEuro === isPredictedEuro) {
                europeanQualificationAccuracy++;
            }

            // Relegation Zone Accuracy (bottom 3 positions, assuming 20 teams total)
            const isActualRelegated = actualTeam.pos >= totalTeams - 2 && actualTeam.pos <= totalTeams;
            const isPredictedRelegated = predictedTeam.pos >= totalTeams - 2 && predictedTeam.pos <= totalTeams;
            if (isActualRelegated === isPredictedRelegated) {
                relegationZoneAccuracy++;
            }
        }
    });

    const overallPositionAccuracy = Math.round((perfectPositionMatches / totalTeams) * 100); // Exact matches
    const proximityAccuracy = Math.round((withinTwoPositions / totalTeams) * 100); // Your original within 2
    const broaderProximityAccuracy = Math.round((withinThreePositions / totalTeams) * 100); // New: within 3

    const avgPointsDiff = Math.round(totalPointsDiff / totalTeams);
    
    // Convert counts to percentages for European/Relegation accuracy
    const euroAccuracyPercentage = Math.round((europeanQualificationAccuracy / totalTeams) * 100);
    const relegationAccuracyPercentage = Math.round((relegationZoneAccuracy / totalTeams) * 100);


    document.getElementById('positionAccuracy').textContent = `${proximityAccuracy}% within ±2 positions`;
    document.getElementById('perfectPositionAccuracy').textContent = `${overallPositionAccuracy}% exact matches`; // New display
    document.getElementById('broaderProximityAccuracy').textContent = `${broaderProximityAccuracy}% within ±3 positions`; // New display

    document.getElementById('pointsDiff').textContent = avgPointsDiff;
    document.getElementById('top4Accuracy').textContent = `${top4TeamsPredictedCorrectly} teams in Top 4`; // Changed wording
    document.getElementById('championCorrect').textContent = championCorrect ? '✅ Champion Correct!' : '❌ Champion Missed'; // Enhanced text
    document.getElementById('europeanQualificationAccuracy').textContent = `${euroAccuracyPercentage}% correctly identified for European qualification`; // New display
    document.getElementById('relegationZoneAccuracy').textContent = `${relegationAccuracyPercentage}% correctly identified for Relegation Zone`; // New display

    // Optional: Add some console logs to verify these new metrics
    console.log(`Perfect Position Matches: ${perfectPositionMatches}/${totalTeams} (${overallPositionAccuracy}%)`);
    console.log(`Within ±2 Positions: ${withinTwoPositions}/${totalTeams} (${proximityAccuracy}%)`);
    console.log(`Within ±3 Positions: ${withinThreePositions}/${totalTeams} (${broaderProximityAccuracy}%)`);
    console.log(`European Qualification Accuracy: ${europeanQualificationAccuracy}/${totalTeams} (${euroAccuracyPercentage}%)`);
    console.log(`Relegation Zone Accuracy: ${relegationZoneAccuracy}/${totalTeams} (${relegationAccuracyPercentage}%)`);
}



// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadData();
});