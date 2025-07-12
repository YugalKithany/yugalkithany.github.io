// Global variables
let predictedData2425 = null;
let actualData2425 = null;
let predictedData2526 = null;
let currentSeason = '2425';
let currentViewType = 'comparison';

// Load data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadData();
});

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

        console.log('Data loaded successfully');
    } catch (error) {
        console.error('Error loading data files:', error);
        showErrorMessage('Ensure all data files are present and accessible.');
    }
}

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
            } else if (cleanHeader === 'xg') {
                row.xg = parseFloat(value);
            } else if (cleanHeader === 'xga') {
                row.xga = parseFloat(value);
            }
        });
        
        if (row.gf !== undefined && row.ga !== undefined) {
            row.gd = row.gf - row.ga;
        }
        
        data.push(row);
    }
    
    return data;
}

function showErrorMessage(message) {
    const tableContainer = document.getElementById('table-container');
    tableContainer.innerHTML = `
        <div class="error-message">
            <h3>⚠️ Data Loading Error</h3>
            <p>${message}</p>
        </div>
    `;
}

function showSeason(season) {
    currentSeason = season;
    
    // Update main toggle buttons
    document.querySelectorAll('.main-toggle-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Show/hide season views
    document.querySelectorAll('.season-view').forEach(view => {
        view.classList.remove('active');
    });
    document.getElementById(`season-${season}`).classList.add('active');
    
    // Reset table
    document.getElementById('table-container').innerHTML = `
        <p style="text-align: center; color: #6c757d; margin-top: 50px;">
            Choose a model from the filters panel to display predictions.
        </p>
    `;
    document.getElementById('table-title').textContent = 'Select a model to view predictions';
}

function setViewType(type) {
    currentViewType = type;
    
    // Update comparison toggle
    document.querySelectorAll('.comparison-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update data if model is selected
    updateData();
}

function updateData() {
    const modelSelect = document.getElementById(`model-select-${currentSeason}`);
    const selectedModel = modelSelect.value;
    
    if (!selectedModel) {
        document.getElementById('table-container').innerHTML = `
            <p style="text-align: center; color: #6c757d; margin-top: 50px;">
                Choose a model from the filters panel to display predictions.
            </p>
        `;
        return;
    }

    if (currentSeason === '2425') {
        update2425Data(selectedModel);
    } else {
        update2526Data(selectedModel);
    }
}

function update2425Data(selectedModel) {
    if (!predictedData2425 || !actualData2425) {
        showErrorMessage('Data not loaded yet. Please refresh the page.');
        return;
    }

    const modelData = predictedData2425[selectedModel];
    if (!modelData) {
        showErrorMessage('Selected model data not found.');
        return;
    }

    // Update model info
    document.getElementById('model-description-2425').textContent = modelData.description;
    document.getElementById('training-seasons-2425').textContent = modelData.model_info.training_seasons.join(', ');
    document.getElementById('training-matches-2425').textContent = modelData.model_info.training_matches;
    document.getElementById('model-info-2425').style.display = 'block';

    // Update title
    document.getElementById('table-title').textContent = `${modelData.label} ${currentViewType === 'comparison' ? '- Comparison with Actual' : '- Predicted Standings'}`;

    // Generate table
    if (currentViewType === 'comparison') {
        generateComparisonTable(modelData);
        updateAccuracyStats(modelData);
        document.getElementById('stats-summary-2425').style.display = 'block';
    } else {
        generatePredictedTable(modelData);
        document.getElementById('stats-summary-2425').style.display = 'none';
    }
}

function update2526Data(selectedModel) {
    if (!predictedData2526) {
        showErrorMessage('2025/26 data not loaded yet. Please refresh the page.');
        return;
    }

    const modelData = predictedData2526[selectedModel];
    if (!modelData) {
        showErrorMessage('Selected model data not found.');
        return;
    }

    // Update model info
    document.getElementById('model-description-2526').textContent = modelData.description;
    document.getElementById('training-seasons-2526').textContent = modelData.model_info.training_seasons.join(', ');
    document.getElementById('training-matches-2526').textContent = modelData.model_info.training_matches;
    document.getElementById('model-info-2526').style.display = 'block';

    // Update title
    document.getElementById('table-title').textContent = `${modelData.label} - Predicted Standings`;

    // Generate predicted table
    generatePredictedTable(modelData);
}

function generateComparisonTable(modelData) {
    const tableContainer = document.getElementById('table-container');
    
    let tableHTML = `
        <table class="standings-table">
            <thead>
                <tr>
                    <th>Team</th>
                    <th>Predicted Pos</th>
                    <th>Actual Pos</th>
                    <th>Predicted Pts</th>
                    <th>Actual Pts</th>
                    <th>Difference</th>
                </tr>
            </thead>
            <tbody>
    `;

    actualData2425.forEach(actualTeam => {
        const predictedTeam = modelData.standings.find(p => p.team === actualTeam.team);
        if (predictedTeam) {
            const posDiff = actualTeam.pos - predictedTeam.pos;
            const ptsDiff = actualTeam.pts - predictedTeam.pts;
            
            let posIndicator = '';
            if (posDiff > 0) {
                posIndicator = `<span class="pos-indicator pos-down">-${posDiff}</span>`;
            } else if (posDiff < 0) {
                posIndicator = `<span class="pos-indicator pos-up">+${Math.abs(posDiff)}</span>`;
            } else {
                posIndicator = `<span class="pos-indicator pos-same">=</span>`;
            }

            tableHTML += `
                <tr>
                    <td class="team-name">${actualTeam.team}${posIndicator}</td>
                    <td>${predictedTeam.pos}</td>
                    <td><strong>${actualTeam.pos}</strong></td>
                    <td>${predictedTeam.pts}</td>
                    <td><strong>${actualTeam.pts}</strong></td>
                    <td style="color: ${ptsDiff > 0 ? '#28a745' : '#dc3545'}">${ptsDiff > 0 ? '+' : ''}${ptsDiff}</td>
                </tr>
            `;
        }
    });

    tableHTML += `
            </tbody>
        </table>
    `;

    tableContainer.innerHTML = tableHTML;
}

function generatePredictedTable(modelData) {
    const tableContainer = document.getElementById('table-container');
    
    let tableHTML = `
        <table class="standings-table">
            <thead>
                <tr>
                    <th>Pos</th>
                    <th>Team</th>
                    <th>Pts</th>
                    <th>P</th>
                    <th>W</th>
                    <th>D</th>
                    <th>L</th>
                    <th>GF</th>
                    <th>GA</th>
                    <th>GD</th>
                </tr>
            </thead>
            <tbody>
    `;

    modelData.standings.forEach(team => {
        tableHTML += `
            <tr>
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
            </tr>
        `;
    });

    tableHTML += `
            </tbody>
        </table>
    `;

    tableContainer.innerHTML = tableHTML;
}

function updateAccuracyStats(modelData) {
    if (!actualData2425) return;

    let withinThreePositions = 0;
    let totalPointsDiff = 0;
    let top4Correct = 0;

    actualData2425.forEach(actualTeam => {
        const predictedTeam = modelData.standings.find(p => p.team === actualTeam.team);
        if (predictedTeam) {
            const posDiff = Math.abs(actualTeam.pos - predictedTeam.pos);
            if (posDiff <= 3) withinThreePositions++;
            totalPointsDiff += Math.abs(actualTeam.pts - predictedTeam.pts);
            if (actualTeam.pos <= 4 && predictedTeam.pos <= 4) top4Correct++;
        }
    });

    const positionAccuracy = Math.round((withinThreePositions / actualData2425.length) * 100);
    const avgPointsDiff = Math.round(totalPointsDiff / actualData2425.length);
    const championCorrect = actualData2425[0].team === modelData.standings[0].team;

    document.getElementById('position-accuracy').textContent = positionAccuracy + '%';
    document.getElementById('top4-correct').textContent = top4Correct + '/4';
    document.getElementById('champion-correct').textContent = championCorrect ? '✅' : '❌';
    document.getElementById('avg-points-diff').textContent = avgPointsDiff + ' pts';
}