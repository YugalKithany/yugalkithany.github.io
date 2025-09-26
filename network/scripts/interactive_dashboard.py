import json
import pandas as pd
import numpy as np
import networkx as nx
from collections import defaultdict, Counter
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
from datetime import datetime
import re

class InteractiveBarcelonaDashboard:
    """
    Creates an interactive HTML dashboard showing Barcelona's passing networks across the entire season
    """
    
    def __init__(self):
        self.events_data = None
        self.matches_data = None
        self.teams_data = None
        self.players_data = None
        self.barca_id = None
        self.all_match_data = []
        
    def fix_unicode_text(self, text):
        """Fix Unicode encoding issues in player names"""
        if not isinstance(text, str):
            return str(text)
        try:
            # Try to fix common encoding issues
            fixed = text.encode('utf-8').decode('unicode_escape')
            if '\\u' in fixed:
                # If still has unicode escapes, try another approach
                fixed = bytes(text, 'utf-8').decode('unicode_escape')
            return fixed
        except:
            # If all else fails, just remove problematic characters
            return re.sub(r'\\u[0-9a-fA-F]{4}', '', text)
    
    def get_clean_player_name(self, player_id):
        """Get clean, properly formatted player name"""
        for player in self.players_data:
            if player['wyId'] == player_id:
                name = player.get('shortName', player.get('firstName', f'Player_{player_id}'))
                
                # Fix Unicode issues
                name = self.fix_unicode_text(name)
                
                # Format name: Last name only, or F. Last for common names
                if ' ' in name.strip():
                    parts = name.strip().split()
                    if len(parts) >= 2:
                        # For well-known players, use just last name
                        famous_last_names = ['Messi', 'Suárez', 'Busquets', 'Piqué', 'Alba', 'Iniesta']
                        last_name = parts[-1]
                        if any(famous in last_name for famous in famous_last_names):
                            return last_name
                        else:
                            return f"{parts[0][0]}. {last_name}"  # F. Last
                    else:
                        return parts[-1]
                return name.strip()
        return f'Player_{player_id}'
    
    def load_data(self, events_path, matches_path, teams_path, players_path):
        """Load all data files"""
        try:
            with open(events_path, 'r', encoding='utf-8') as f:
                self.events_data = json.load(f)
            
            with open(matches_path, 'r', encoding='utf-8') as f:
                self.matches_data = json.load(f)
            
            with open(teams_path, 'r', encoding='utf-8') as f:
                self.teams_data = json.load(f)
            
            with open(players_path, 'r', encoding='utf-8') as f:
                self.players_data = json.load(f)
            
            # Find Barcelona
            for team in self.teams_data:
                if 'Barcelona' in team['name']:
                    self.barca_id = team['wyId']
                    print(f"Found Barcelona with ID: {self.barca_id}")
                    break
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def determine_match_outcome(self, match):
        """Determine if Barcelona won, lost, or drew"""
        # Get team data
        teams_data = match['teamsData']
        
        # Find Barcelona's data and opponent's data
        barca_score = None
        opponent_score = None
        
        for team_id, team_data in teams_data.items():
            if int(team_id) == self.barca_id:
                barca_score = team_data['score']
            else:
                opponent_score = team_data['score']
        
        if barca_score is None or opponent_score is None:
            return 'unknown'
        
        if barca_score > opponent_score:
            return 'win'
        elif barca_score < opponent_score:
            return 'loss'
        else:
            return 'draw'
    
    def process_all_matches(self):
        """Process all Barcelona matches and extract network data"""
        print("Processing all Barcelona matches...")
        
        # Find all Barcelona matches
        barca_matches = []
        for match in self.matches_data:
            teams_data = match.get('teamsData', {})
            if str(self.barca_id) in teams_data:
                outcome = self.determine_match_outcome(match)
                
                # Parse date for chronological ordering
                date_str = match.get('date', '')
                try:
                    match_date = datetime.strptime(date_str.split(' at ')[0], '%B %d, %Y')
                except:
                    match_date = datetime.now()
                
                barca_matches.append({
                    'match_id': match['wyId'],
                    'label': match['label'],
                    'outcome': outcome,
                    'date': date_str,
                    'date_obj': match_date,
                    'venue': match.get('venue', ''),
                    'gameweek': match.get('gameweek', 0)
                })
        
        # Sort matches by date
        barca_matches.sort(key=lambda x: x['date_obj'])
        
        print(f"Found {len(barca_matches)} Barcelona matches")
        
        # Process each match to get network data
        processed_matches = []
        for i, match_info in enumerate(barca_matches):
            print(f"Processing match {i+1}/{len(barca_matches)}: {match_info['label']}")
            
            network_data = self.extract_network_data(match_info['match_id'])
            if network_data:
                match_info.update(network_data)
                match_info['match_number'] = i + 1
                processed_matches.append(match_info)
        
        self.all_match_data = processed_matches
        print(f"Successfully processed {len(processed_matches)} matches with network data")
        
        return processed_matches
    
    def extract_network_data(self, match_id):
        """Extract passing network data for a match"""
        # Get Barcelona passes for this match
        match_passes = [
            event for event in self.events_data 
            if event['matchId'] == match_id 
            and event['teamId'] == self.barca_id 
            and event['eventName'] == 'Pass'
        ]
        
        if len(match_passes) < 10:  # Too few passes
            return None
        
        # Sort by time
        match_passes.sort(key=lambda x: (x['matchPeriod'], x['eventSec']))
        
        # Calculate player positions
        player_positions = defaultdict(list)
        for event in match_passes:
            if event['positions']:
                player_id = event['playerId']
                x, y = event['positions'][0]['x'], event['positions'][0]['y']
                player_positions[player_id].append((x, y))
        
        # Average positions
        avg_positions = {}
        for player_id, positions in player_positions.items():
            if len(positions) >= 3:  # Player must have at least 3 positions
                avg_x = np.mean([pos[0] for pos in positions])
                avg_y = np.mean([pos[1] for pos in positions])
                avg_positions[player_id] = (avg_x, avg_y)
        
        # Build passing network
        G = nx.Graph()
        passing_counts = defaultdict(int)
        
        for i in range(len(match_passes) - 1):
            current_pass = match_passes[i]
            next_pass = match_passes[i + 1]
            
            if next_pass['eventSec'] - current_pass['eventSec'] <= 30:
                passer = current_pass['playerId']
                receiver = next_pass['playerId']
                
                if (passer != receiver and 
                    passer in avg_positions and 
                    receiver in avg_positions):
                    passing_counts[(passer, receiver)] += 1
        
        # Add edges to graph
        for (passer, receiver), count in passing_counts.items():
            G.add_edge(passer, receiver, weight=count)
        
        if G.number_of_nodes() < 5:  # Too few players
            return None
        
        # Calculate metrics
        try:
            centrality = nx.betweenness_centrality(G)
            degree_centrality = nx.degree_centrality(G)
            density = nx.density(G)
        except:
            return None
        
        return {
            'graph': G,
            'positions': avg_positions,
            'passing_counts': dict(passing_counts),
            'centrality': centrality,
            'degree_centrality': degree_centrality,
            'density': density,
            'num_players': G.number_of_nodes(),
            'num_connections': G.number_of_edges(),
            'total_passes': len(match_passes)
        }
    
    def create_network_plot(self, match_data):
        """Create a Plotly network visualization for a single match"""
        if 'graph' not in match_data:
            return None
        
        G = match_data['graph']
        positions = match_data['positions']
        centrality = match_data['centrality']
        
        # Prepare node data
        node_x, node_y, node_text, node_size, node_color = [], [], [], [], []
        node_names = []
        
        for player_id in G.nodes():
            if player_id in positions:
                x, y = positions[player_id]
                node_x.append(x)
                node_y.append(y)
                
                player_name = self.get_clean_player_name(player_id)
                node_names.append(player_name)
                
                total_passes = sum(G[player_id][neighbor]['weight'] for neighbor in G[player_id])
                betweenness = centrality.get(player_id, 0)
                
                node_text.append(f"{player_name}<br>Total Passes: {total_passes}<br>Centrality: {betweenness:.3f}")
                node_size.append(max(15, total_passes * 0.5 + 20))
                node_color.append(betweenness)
        
        # Prepare edge data
        edge_x, edge_y = [], []
        for edge in G.edges():
            if edge[0] in positions and edge[1] in positions:
                x0, y0 = positions[edge[0]]
                x1, y1 = positions[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
        
        # Create the plot
        fig = go.Figure()
        
        # Add soccer pitch
        self.add_pitch_shapes(fig)
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.5, color='rgba(100,100,100,0.4)'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(
                size=node_size,
                color=node_color,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Centrality", x=1.05),
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            text=node_names,
            textposition="middle center",
            textfont=dict(size=14, color="black", family="Arial Black"),
            hovertext=node_text,
            hoverinfo='text',
            showlegend=False
        ))
        
        # Update layout
        outcome_colors = {'win': 'lightgreen', 'loss': 'lightcoral', 'draw': 'lightyellow'}
        bg_color = outcome_colors.get(match_data['outcome'], 'lightblue')
        
        fig.update_layout(
            title=dict(
                text=f"{match_data['label']} - {match_data['outcome'].title()}<br>"
                     f"Density: {match_data['density']:.3f} | Players: {match_data['num_players']} | Connections: {match_data['num_connections']}",
                x=0.5,
                font=dict(size=14)
            ),
            xaxis=dict(
                showgrid=False, 
                zeroline=False, 
                showticklabels=False, 
                range=[-2, 102],
                fixedrange=True
            ),
            yaxis=dict(
                showgrid=False, 
                zeroline=False, 
                showticklabels=False, 
                range=[-2, 102],
                fixedrange=True,
                scaleanchor="x",
                scaleratio=1
            ),
            plot_bgcolor=bg_color,
            paper_bgcolor='white',
            height=800,
            width=None,  # Let it be responsive
            autosize=True,
            # margin=dict(l=20, r=20, t=60, b=20)  # Smaller margins
            margin=dict(l=10, r=10, t=80, b=10)  # Tighter margins

        )
        
        return fig
    
    def add_pitch_shapes(self, fig):
        """Add soccer pitch shapes to the plot"""
        # Pitch outline
        fig.add_shape(
            type="rect", x0=0, y0=0, x1=100, y1=100,
            line=dict(color="white", width=3),
            fillcolor="rgba(0, 128, 0, 0.3)"
        )
        
        # Center line
        fig.add_shape(
            type="line", x0=50, y0=0, x1=50, y1=100,
            line=dict(color="white", width=2)
        )
        
        # Center circle
        fig.add_shape(
            type="circle", x0=40, y0=40, x1=60, y1=60,
            line=dict(color="white", width=2),
            fillcolor="rgba(0,0,0,0)"
        )
        
        # Penalty areas
        fig.add_shape(
            type="rect", x0=0, y0=21, x1=16, y1=79,
            line=dict(color="white", width=2),
            fillcolor="rgba(0,0,0,0)"
        )
        fig.add_shape(
            type="rect", x0=84, y0=21, x1=100, y1=79,
            line=dict(color="white", width=2),
            fillcolor="rgba(0,0,0,0)"
        )
    
    def create_metrics_timeline(self):
        """Create timeline showing network metrics across the season"""
        if not self.all_match_data:
            return None
        
        df = pd.DataFrame([
            {
                'match_number': match['match_number'],
                'label': match['label'][:30] + '...' if len(match['label']) > 30 else match['label'],
                'density': match['density'],
                'num_players': match['num_players'],
                'num_connections': match['num_connections'],
                'outcome': match['outcome'],
                'date': match['date']
            }
            for match in self.all_match_data
        ])
        
        # fig = make_subplots(
        #     rows=3, cols=1,
        #     subplot_titles=('Network Density', 'Number of Players', 'Number of Connections'),
        #     vertical_spacing=0.08
        # )
        
        # colors = {'win': 'green', 'loss': 'red', 'draw': 'orange', 'unknown': 'blue'}
        
        # for outcome in df['outcome'].unique():
        #     outcome_data = df[df['outcome'] == outcome]
            
        #     fig.add_trace(
        #         go.Scatter(
        #             x=outcome_data['match_number'],
        #             y=outcome_data['density'],
        #             mode='markers+lines',
        #             name=f'{outcome.title()}',
        #             marker=dict(color=colors.get(outcome, 'blue')),
        #             hovertemplate="%{text}<br>Density: %{y:.3f}<extra></extra>",
        #             text=outcome_data['label']
        #         ),
        #         row=1, col=1
        #     )
            
        #     fig.add_trace(
        #         go.Scatter(
        #             x=outcome_data['match_number'],
        #             y=outcome_data['num_players'],
        #             mode='markers+lines',
        #             showlegend=False,
        #             marker=dict(color=colors.get(outcome, 'blue')),
        #             hovertemplate="%{text}<br>Players: %{y}<extra></extra>",
        #             text=outcome_data['label']
        #         ),
        #         row=2, col=1
        #     )
            
        #     fig.add_trace(
        #         go.Scatter(
        #             x=outcome_data['match_number'],
        #             y=outcome_data['num_connections'],
        #             mode='markers+lines',
        #             showlegend=False,
        #             marker=dict(color=colors.get(outcome, 'blue')),
        #             hovertemplate="%{text}<br>Connections: %{y}<extra></extra>",
        #             text=outcome_data['label']
        #         ),
        #         row=3, col=1
        #     )
        
        # fig.update_layout(
        #     title="Barcelona Network Metrics Across the Season",
        #     height=800,
        #     hovermode='x unified'
        # )
        
        # fig.update_xaxes(title_text="Match Number", row=3, col=1)
        
        # return fig
    
    def create_interactive_dashboard(self, output_file='barcelona_dashboard.html'):
        """Create the complete interactive dashboard"""
        if not self.all_match_data:
            print("No match data available!")
            return
        
        # Create individual match plots
        match_plots = []
        for match_data in self.all_match_data:
            plot = self.create_network_plot(match_data)
            if plot:
                match_plots.append(plot)
        
        # Create metrics timeline
        timeline_plot = self.create_metrics_timeline()
        
        # Create HTML with all plots
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>FC Barcelona Season Network Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            color: #1e293b;
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            color: white;
            padding: 1.5rem;
            margin: 0;
            border-radius: 0;
        }}
        .header h1 {{
            margin: 0 0 0.5rem 0;
            font-size: 1.8rem;
            font-weight: 600;
        }}
        .header h2 {{
            margin: 0;
            font-size: 1.1rem;
            font-weight: 400;
            opacity: 0.9;
        }}
        .controls {{
            text-align: center;
            margin: 0;
            padding: 1.5rem;
            background: white;
            border-bottom: 1px solid #e2e8f0;
        }}
        .controls h3 {{
            margin: 0 0 1rem 0;
            font-size: 1.2rem;
            font-weight: 500;
            color: #374151;
        }}
        .match-display {{
            margin: 0;
            padding: 10px;
            background: white;
        }}
        .stats-summary {{
            display: flex;
            justify-content: space-around;
            margin: 1rem 0 0 0;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .stat-box {{
            text-align: center;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
            min-width: 100px;
            flex: 1;
        }}
        .stat-box div:first-child {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }}
        .stat-box div:last-child {{
            font-size: 0.85rem;
            color: #6b7280;
            font-weight: 500;
        }}
        #matchSlider {{
            width: 70%;
            margin: 1rem;
            height: 6px;
            background: #e2e8f0;
            border-radius: 3px;
            outline: none;
        }}
        #matchSlider::-webkit-slider-thumb {{
            appearance: none;
            width: 18px;
            height: 18px;
            background: #3b82f6;
            border-radius: 50%;
            cursor: pointer;
        }}
        #matchSlider::-moz-range-thumb {{
            width: 18px;
            height: 18px;
            background: #3b82f6;
            border-radius: 50%;
            cursor: pointer;
            border: none;
        }}
        #matchInfo {{
            margin-top: 1rem;
            font-size: 1.1rem;
            font-weight: 600;
            color: #1e293b;
        }}

        #timelinePlot {{
            height: 300px;
        }}
       
        @media (max-width: 768px) {{
            .stats-summary {{
                flex-direction: column;
            }}
            .stat-box {{
                margin-bottom: 0.5rem;
            }}
            #matchSlider {{
                width: 85%;
            }}
            .header h1 {{
                font-size: 1.5rem;
            }}
            .header h2 {{
                font-size: 1rem;
            }}
        }}
    </style>
    

</head>
<body>
    
    <div class="controls">
        <h3>Select Match to Analyze</h3>
        <input type="range" id="matchSlider" min="1" max="{len(self.all_match_data)}" 
               value="1" oninput="updateMatch(this.value)">
        <div id="matchInfo" style="margin-top: 15px; font-size: 18px; font-weight: bold;"></div>
        <div class="stats-summary" id="statsDisplay"></div>
    </div>
    
    <div class="match-display">
        <div id="networkPlot"></div>
    </div>
    
    <div class="match-display">
        <div id="timelinePlot"></div>
    </div>

    <script>
        const matchData = {json.dumps([{
            'match_number': m['match_number'],
            'label': m['label'],
            'outcome': m['outcome'],
            'density': round(m['density'], 3),
            'num_players': m['num_players'],
            'num_connections': m['num_connections'],
            'total_passes': m.get('total_passes', 0)
        } for m in self.all_match_data])};
        
        const networkPlots = {json.dumps([fig.to_json() for fig in match_plots])};
        
        function updateMatch(matchIndex) {{
            const match = matchData[matchIndex - 1];
            const plot = JSON.parse(networkPlots[matchIndex - 1]);
            
            // Update match info
            document.getElementById('matchInfo').innerHTML = 
                `Match ${{matchIndex}}: ${{match.label}} (${{match.outcome.toUpperCase()}})`;
            
            // Update stats display
            const outcomeColors = {{
                'win': '#4CAF50',
                'loss': '#f44336', 
                'draw': '#ff9800',
                'unknown': '#2196F3'
            }};
            
            document.getElementById('statsDisplay').innerHTML = `
                <div class="stat-box" style="border-left-color: ${{outcomeColors[match.outcome]}}">
                    <div style="font-size: 20px; font-weight: bold; color: ${{outcomeColors[match.outcome]}}">
                        ${{match.outcome.toUpperCase()}}
                    </div>
                    <div>Match Result</div>
                </div>
                <div class="stat-box">
                    <div style="font-size: 20px; font-weight: bold;">${{match.density}}</div>
                    <div>Network Density</div>
                </div>
                <div class="stat-box">
                    <div style="font-size: 20px; font-weight: bold;">${{match.num_players}}</div>
                    <div>Players Involved</div>
                </div>
                <div class="stat-box">
                    <div style="font-size: 20px; font-weight: bold;">${{match.num_connections}}</div>
                    <div>Pass Connections</div>
                </div>
                <div class="stat-box">
                    <div style="font-size: 20px; font-weight: bold;">${{match.total_passes}}</div>
                    <div>Total Passes</div>
                </div>
            `;
            
            // Update network plot
            Plotly.newPlot('networkPlot', plot.data, plot.layout);
        }}
        
        // Initialize with first match
        updateMatch(1);
        
        // Add timeline plot
        const timelinePlot = {timeline_plot.to_json() if timeline_plot else 'null'};
        if (timelinePlot) {{
            Plotly.newPlot('timelinePlot', timelinePlot.data, timelinePlot.layout);
        }}
    </script>
</body>
</html>
        """
        
        # Save HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Interactive dashboard saved as {output_file}")
        print(f"Open {output_file} in your browser to explore the data!")

def main():
    """Main function to create the interactive dashboard"""
    import os
    
    # Initialize dashboard
    dashboard = InteractiveBarcelonaDashboard()
    
    # Define file paths
    network_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    events_path = os.path.join(network_dir, 'data', 'events', 'events_Spain.json')
    matches_path = os.path.join(network_dir, 'data', 'matches', 'matches_Spain.json')
    teams_path = os.path.join(network_dir, 'data', 'teams.json')
    players_path = os.path.join(network_dir, 'data', 'players.json')
    
    # Load data
    if not dashboard.load_data(events_path, matches_path, teams_path, players_path):
        print("Failed to load data files!")
        return
    
    # Process all matches
    dashboard.process_all_matches()
    
    # Create interactive dashboard
    output_file = os.path.join(network_dir, 'barcelona_interactive_dashboard.html')
    dashboard.create_interactive_dashboard(output_file)

if __name__ == '__main__':
    main()