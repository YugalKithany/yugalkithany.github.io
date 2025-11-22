import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import json
from collections import defaultdict, Counter
import warnings
warnings.filterwarnings('ignore')

class BarcelonaNetworkAnalyzer:
    """
    Complete Barcelona passing network analyzer that works with your actual data structure
    """
    
    def __init__(self):
        self.events_data = None
        self.matches_data = None
        self.teams_data = None
        self.players_data = None
        self.barca_id = None
        
    def load_data(self, events_path, matches_path, teams_path, players_path):
        """Load all data files and inspect structure"""
        try:
            with open(events_path, 'r') as f:
                self.events_data = json.load(f)
            print(f"Loaded {len(self.events_data)} events")
            
            with open(matches_path, 'r') as f:
                self.matches_data = json.load(f)
            print(f"Loaded {len(self.matches_data)} matches")
            
            with open(teams_path, 'r') as f:
                self.teams_data = json.load(f)
            
            with open(players_path, 'r') as f:
                self.players_data = json.load(f)
            
            # Debug: Print structure of first match
            if self.matches_data:
                print("Sample match structure:", list(self.matches_data[0].keys()))
                print("Sample match data:", self.matches_data[0])
            
            # Find Barcelona's team ID - try different possible name variations
            barca_names = ['Barcelona', 'FC Barcelona', 'Barça', 'Barca']
            for team in self.teams_data:
                for barca_name in barca_names:
                    if barca_name.lower() in team['name'].lower():
                        self.barca_id = team['wyId']
                        print(f"Found Barcelona ({team['name']}) with ID: {self.barca_id}")
                        return True
            
            print("Available teams:")
            for team in self.teams_data[:10]:  # Show first 10 teams
                print(f"  {team['name']} (ID: {team['wyId']})")
            
            return False
                    
        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()
            return False

    def get_player_name(self, player_id):
        """Get player name from player ID with proper Unicode handling"""
        for player in self.players_data:
            if player['wyId'] == player_id:
                # Get the name, prioritizing 'shortName'
                name = player.get('shortName', player.get('firstName', f'Player_{player_id}'))
                
                # Ensure the name is a string, and remove any leading/trailing whitespace
                if isinstance(name, str):
                    name = name.strip()
                    
                    # Split the name and return a formatted version
                    if ' ' in name:
                        parts = name.split()
                        # Return 'F. Last' format if there are multiple parts
                        return f"{parts[0][0]}. {parts[-1]}"
                    else:
                        return name
                
                # If name isn't a string or is empty, return a default
                return f'Player_{player_id}'

        # If player ID is not found, return a default
        return f'Player_{player_id}'
    
    def find_barca_matches(self):
        """Find all Barcelona matches - flexible approach to handle different data structures"""
        if not self.barca_id:
            print("Barcelona team ID not found!")
            return []
        
        barca_matches = []
        
        for match in self.matches_data:
            # Handle different possible structures
            teams_info = None
            
            # Try different ways to access team information
            if 'teams' in match:
                teams_info = match['teams']
            elif 'teamsData' in match:
                teams_info = match['teamsData']
            else:
                # If no teams field, try to infer from other fields
                continue
            
            # Check if Barcelona is in this match
            team_ids = []
            if isinstance(teams_info, dict):
                team_ids = list(teams_info.keys())
            elif isinstance(teams_info, list):
                team_ids = [str(team['wyId']) if 'wyId' in team else team.get('teamId', '') for team in teams_info]
            
            # Convert team IDs to match our Barcelona ID
            if str(self.barca_id) in team_ids or self.barca_id in team_ids:
                # Parse score from label if available
                outcome = 'unknown'
                if 'label' in match and ' - ' in match['label']:
                    try:
                        score_parts = match['label'].split(' - ')
                        score1 = int(score_parts[0])
                        score2 = int(score_parts[1])
                        
                        # We need to determine which team is which
                        # This is a simplified approach - you may need to adjust based on your data
                        if score1 > score2:
                            outcome = 'win'  # Assume Barcelona is first team if they won
                        elif score1 < score2:
                            outcome = 'loss'
                        else:
                            outcome = 'draw'
                    except (ValueError, IndexError):
                        outcome = 'unknown'
                
                barca_matches.append({
                    'match_id': match['wyId'],
                    'label': match.get('label', f"Match {match['wyId']}"),
                    'date': match.get('date', ''),
                    'outcome': outcome
                })
        
        return barca_matches
    
    def create_passing_network(self, match_id):
        """Create passing network for a specific match"""
        # Get Barcelona events for this match
        match_events = [
            event for event in self.events_data 
            if event['matchId'] == match_id and event['teamId'] == self.barca_id
        ]
        
        # Filter for passes only
        passes = [event for event in match_events if event['eventName'] == 'Pass']
        
        if not passes:
            print(f"No passes found for Barcelona in match {match_id}")
            # Check if we have any events at all for this match
            all_match_events = [e for e in self.events_data if e['matchId'] == match_id]
            print(f"Total events in match: {len(all_match_events)}")
            if all_match_events:
                unique_teams = set(e['teamId'] for e in all_match_events)
                print(f"Teams in match: {unique_teams}")
                print(f"Looking for Barcelona team ID: {self.barca_id}")
            return None, None, None
        
        print(f"Found {len(passes)} passes for Barcelona in match {match_id}")
        
        # Sort passes by time
        passes.sort(key=lambda x: (x['matchPeriod'], x['eventSec']))
        
        # Calculate average positions for each player
        player_positions = defaultdict(list)
        for event in passes:
            if event['positions']:
                player_id = event['playerId']
                x, y = event['positions'][0]['x'], event['positions'][0]['y']
                player_positions[player_id].append((x, y))
        
        avg_positions = {}
        for player_id, positions in player_positions.items():
            if positions:
                avg_x = np.mean([pos[0] for pos in positions])
                avg_y = np.mean([pos[1] for pos in positions])
                avg_positions[player_id] = (avg_x, avg_y)
        
        # Build passing network
        G = nx.Graph()
        passing_counts = defaultdict(int)
        
        # Connect consecutive passes
        for i in range(len(passes) - 1):
            current_pass = passes[i]
            next_pass = passes[i + 1]
            
            # Check if passes are reasonably close in time (within 45 seconds)
            if next_pass['eventSec'] - current_pass['eventSec'] <= 45:
                passer = current_pass['playerId']
                receiver = next_pass['playerId']
                
                if passer != receiver:  # Don't connect a player to themselves
                    passing_counts[(passer, receiver)] += 1
        
        # Add edges to graph
        for (passer, receiver), count in passing_counts.items():
            if passer in avg_positions and receiver in avg_positions:
                G.add_edge(passer, receiver, weight=count)
        
        return G, avg_positions, passing_counts
    
    def plot_passing_network(self, match_id, match_info, save_path=None):
        """Create a visualization of the passing network"""
        G, positions, passing_counts = self.create_passing_network(match_id)
        
        if not G or not positions:
            print(f"Could not create network for match {match_id}")
            return None, None
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Draw soccer pitch
        self.draw_pitch(ax)
        
        # Calculate centrality measures
        try:
            centrality = nx.betweenness_centrality(G)
            degree_centrality = nx.degree_centrality(G)
        except:
            centrality = {node: 0 for node in G.nodes()}
            degree_centrality = {node: 0 for node in G.nodes()}
        
        # Node sizes based on degree centrality
        node_sizes = [degree_centrality.get(node, 0) * 2000 + 300 for node in G.nodes()]
        
        # Node colors based on betweenness centrality
        node_colors = [centrality.get(node, 0) for node in G.nodes()]
        
        # Prepare positions for plotting
        pos_dict = {}
        for player_id, (x, y) in positions.items():
            if player_id in G.nodes():
                pos_dict[player_id] = (x, y)
        
        # Draw network
        nodes = nx.draw_networkx_nodes(G, pos_dict, node_size=node_sizes, 
                                      node_color=node_colors, alpha=0.8, 
                                      cmap='viridis', ax=ax)
        
        # Draw edges with thickness proportional to passing frequency
        edges = G.edges()
        if edges:
            weights = [G[u][v]['weight'] for u, v in edges]
            max_weight = max(weights) if weights else 1
            edge_widths = [w / max_weight * 8 + 1 for w in weights]
            
            nx.draw_networkx_edges(G, pos_dict, width=edge_widths, 
                                  alpha=0.6, edge_color='darkblue', ax=ax)
        
        # Add player labels
        labels = {player_id: self.get_player_name(player_id).split()[-1] 
                 for player_id in G.nodes()}
        nx.draw_networkx_labels(G, pos_dict, labels, font_size=10, 
                               font_weight='bold', ax=ax)
        
        # Add colorbar for centrality
        if nodes:
            plt.colorbar(nodes, ax=ax, label='Betweenness Centrality', shrink=0.8)
        
        # Set title and formatting
        ax.set_title(f'FC Barcelona Passing Network\n{match_info["label"]} ({match_info["outcome"].title()})', 
                    fontsize=18, fontweight='bold', pad=20)
        ax.set_xlim(-5, 105)
        ax.set_ylim(-5, 105)
        ax.set_aspect('equal')
        
        # Add network statistics as text
        density = nx.density(G)
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        
        stats_text = f'Network Density: {density:.3f}\nPlayers: {num_nodes}\nConnections: {num_edges}'
        ax.text(102, 95, stats_text, fontsize=12, 
                bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9), 
                verticalalignment='top')
        
        # Add top players by centrality
        if centrality:
            top_players = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:3]
            top_text = "Most Influential Players:\n"
            for i, (player_id, cent) in enumerate(top_players):
                name = self.get_player_name(player_id)
                top_text += f"{i+1}. {name} ({cent:.3f})\n"
            
            ax.text(2, 95, top_text, fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9),
                   verticalalignment='top')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"Network plot saved as {save_path}")
        
        plt.tight_layout()
        return fig, ax
    
    def draw_pitch(self, ax):
        """Draw a soccer pitch on the given axes"""
        # Pitch outline
        pitch = plt.Rectangle((0, 0), 100, 100, linewidth=3, 
                             edgecolor='white', facecolor='darkgreen', alpha=0.8)
        ax.add_patch(pitch)
        
        # Center line
        ax.plot([50, 50], [0, 100], color='white', linewidth=3)
        
        # Center circle
        center_circle = plt.Circle((50, 50), 9.15, color='white', fill=False, linewidth=2)
        ax.add_patch(center_circle)
        
        # Center spot
        center_spot = plt.Circle((50, 50), 0.5, color='white', fill=True)
        ax.add_patch(center_spot)
        
        # Penalty areas
        penalty_left = plt.Rectangle((0, 21.1), 16.5, 57.8, linewidth=2, 
                                   edgecolor='white', fill=False)
        penalty_right = plt.Rectangle((83.5, 21.1), 16.5, 57.8, linewidth=2, 
                                    edgecolor='white', fill=False)
        ax.add_patch(penalty_left)
        ax.add_patch(penalty_right)
        
        # Goal areas
        goal_left = plt.Rectangle((0, 36.8), 5.5, 26.4, linewidth=2, 
                                edgecolor='white', fill=False)
        goal_right = plt.Rectangle((94.5, 36.8), 5.5, 26.4, linewidth=2, 
                                 edgecolor='white', fill=False)
        ax.add_patch(goal_left)
        ax.add_patch(goal_right)
        
        # Penalty spots
        pen_spot_left = plt.Circle((11, 50), 0.5, color='white', fill=True)
        pen_spot_right = plt.Circle((89, 50), 0.5, color='white', fill=True)
        ax.add_patch(pen_spot_left)
        ax.add_patch(pen_spot_right)
        
        ax.set_facecolor('darkgreen')
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
    
    def analyze_network_metrics(self, match_id):
        """Analyze various network metrics for a match"""
        G, positions, passing_counts = self.create_passing_network(match_id)
        
        if not G or G.number_of_nodes() == 0:
            return None
        
        # Calculate various centrality measures
        try:
            metrics = {
                'density': nx.density(G),
                'nodes': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'betweenness_centrality': nx.betweenness_centrality(G),
                'closeness_centrality': nx.closeness_centrality(G),
                'degree_centrality': nx.degree_centrality(G),
            }
            
            # Only calculate PageRank for directed graphs, skip for now
            # metrics['pagerank'] = nx.pagerank(G)
            
        except Exception as e:
            print(f"Error calculating metrics: {e}")
            return None
        
        return metrics
    
    def compare_match_outcomes(self):
        """Compare network metrics between wins, losses, and draws"""
        matches = self.find_barca_matches()
        
        outcomes_metrics = {'win': [], 'loss': [], 'draw': []}
        
        for match in matches:
            if match['outcome'] != 'unknown':
                metrics = self.analyze_network_metrics(match['match_id'])
                if metrics:
                    outcomes_metrics[match['outcome']].append(metrics)
        
        # Calculate average metrics by outcome
        summary = {}
        for outcome, metric_list in outcomes_metrics.items():
            if metric_list:
                summary[outcome] = {
                    'avg_density': np.mean([m['density'] for m in metric_list]),
                    'avg_nodes': np.mean([m['nodes'] for m in metric_list]),
                    'avg_edges': np.mean([m['edges'] for m in metric_list]),
                    'count': len(metric_list)
                }
        
        return summary

def main():
    """Main function to generate Barcelona passing network graphs"""
    
    # Initialize analyzer
    analyzer = BarcelonaNetworkAnalyzer()
    
    # Define file paths
    network_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    events_path = os.path.join(network_dir, 'data', 'events', 'events_Spain.json')
    matches_path = os.path.join(network_dir, 'data', 'matches', 'matches_Spain.json')
    teams_path = os.path.join(network_dir, 'data', 'teams.json')
    players_path = os.path.join(network_dir, 'data', 'players.json')
    
    print("Loading data files...")
    print(f"Events: {events_path}")
    print(f"Matches: {matches_path}")
    print(f"Teams: {teams_path}")
    print(f"Players: {players_path}")
    
    # Load data
    if not analyzer.load_data(events_path, matches_path, teams_path, players_path):
        print("Failed to load data files or find Barcelona. Please check file paths and team name.")
        return
    
    # Find Barcelona matches
    barca_matches = analyzer.find_barca_matches()
    
    if not barca_matches:
        print("No Barcelona matches found in the dataset.")
        return
    
    print(f"\nFound {len(barca_matches)} Barcelona matches")
    
    # Show outcome distribution
    outcomes = Counter(match['outcome'] for match in barca_matches)
    print(f"Match outcomes: {dict(outcomes)}")
    
    # Focus on winning matches for detailed analysis
    winning_matches = [m for m in barca_matches if m['outcome'] == 'win']
    
    if not winning_matches:
        # If no explicit wins, analyze first few matches
        print("No clear winning matches found. Analyzing first few matches...")
        matches_to_analyze = barca_matches[:3]
    else:
        print(f"Found {len(winning_matches)} winning matches")
        matches_to_analyze = winning_matches[:5]  # Analyze first 5 wins
    
    # Analyze selected matches
    successful_analyses = 0
    for i, match_info in enumerate(matches_to_analyze):
        print(f"\n{'='*50}")
        print(f"Analyzing match {i+1}: {match_info['label']}")
        print(f"Outcome: {match_info['outcome']}")
        
        # Generate network visualization
        output_path = os.path.join(network_dir, f'barca_network_match_{match_info["match_id"]}.png')
        fig, ax = analyzer.plot_passing_network(match_info['match_id'], match_info, output_path)
        
        if fig:
            successful_analyses += 1
            
            # Analyze network metrics
            metrics = analyzer.analyze_network_metrics(match_info['match_id'])
            
            if metrics:
                print(f"Network metrics:")
                print(f"  Density: {metrics['density']:.3f}")
                print(f"  Players: {metrics['nodes']}")
                print(f"  Passing connections: {metrics['edges']}")
                
                # Show top 3 players by betweenness centrality
                top_players = sorted(metrics['betweenness_centrality'].items(), 
                                   key=lambda x: x[1], reverse=True)[:3]
                print("  Most influential players (by betweenness centrality):")
                for j, (player_id, centrality) in enumerate(top_players):
                    player_name = analyzer.get_player_name(player_id)
                    print(f"    {j+1}. {player_name}: {centrality:.3f}")
        
        plt.show()  # Display the plot
        
    print(f"\n{'='*50}")
    print(f"Analysis complete! Successfully analyzed {successful_analyses} matches.")
    print(f"Network visualizations saved to: {network_dir}")
    
    # Compare outcomes if we have enough data
    if len(barca_matches) > 5:
        print("\nComparing network metrics across match outcomes...")
        comparison = analyzer.compare_match_outcomes()
        for outcome, stats in comparison.items():
            print(f"\n{outcome.upper()} matches ({stats['count']} games):")
            print(f"  Average network density: {stats['avg_density']:.3f}")
            print(f"  Average players involved: {stats['avg_nodes']:.1f}")
            print(f"  Average connections: {stats['avg_edges']:.1f}")

if __name__ == '__main__':
    main()