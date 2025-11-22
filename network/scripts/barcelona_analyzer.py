# import sys
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import networkx as nx
# import json
# from collections import defaultdict

# # Get the path to the scripts directory and add it to the system path
# scripts_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, scripts_dir)

# class BarcelonaNetworkAnalyzer:
#     """
#     Fixed version of Barcelona passing network analyzer that works without external legend files
#     """
    
#     def __init__(self):
#         self.events_data = None
#         self.matches_data = None
#         self.teams_data = None
#         self.players_data = None
#         self.barca_id = None
        
#     def load_data(self, events_path, matches_path, teams_path, players_path):
#         """Load all data files"""
#         try:
#             with open(events_path, 'r') as f:
#                 self.events_data = json.load(f)
#             print(f"Loaded {len(self.events_data)} events")
            
#             with open(matches_path, 'r') as f:
#                 self.matches_data = json.load(f)
#             print(f"Loaded {len(self.matches_data)} matches")
            
#             with open(teams_path, 'r') as f:
#                 self.teams_data = json.load(f)
            
#             with open(players_path, 'r') as f:
#                 self.players_data = json.load(f)
            
#             # Find Barcelona's team ID
#             for team in self.teams_data:
#                 if 'Barcelona' in team['name']:
#                     self.barca_id = team['wyId']
#                     print(f"Found Barcelona with ID: {self.barca_id}")
#                     break
                    
#         except Exception as e:
#             print(f"Error loading data: {e}")
#             return False
#         return True
    
#     def get_player_name(self, player_id):
#         """Get player name from player ID"""
#         for player in self.players_data:
#             if player['wyId'] == player_id:
#                 return player.get('shortName', f'Player_{player_id}')
#         return f'Player_{player_id}'
    
#     def find_winning_matches(self):
#         """Find all Barcelona winning matches"""
#         winning_matches = []
        
#         for match in self.matches_data:
#             teams = match['teams']
#             team_ids = [team['wyId'] for team in teams]
            
#             if self.barca_id in team_ids:
#                 # Parse the score from label
#                 try:
#                     score = match['label'].split(' - ')
#                     team1_score = int(score[0])
#                     team2_score = int(score[1])
                    
#                     barca_is_home = teams[0]['wyId'] == self.barca_id
                    
#                     # Check if Barcelona won
#                     if (barca_is_home and team1_score > team2_score) or \
#                        (not barca_is_home and team2_score > team1_score):
#                         winning_matches.append({
#                             'match_id': match['wyId'],
#                             'label': match['label'],
#                             'date': match.get('date', '')
#                         })
#                 except (ValueError, IndexError):
#                     continue
        
#         return winning_matches
    
#     def create_passing_network(self, match_id):
#         """Create passing network for a specific match"""
#         # Get Barcelona events for this match
#         match_events = [
#             event for event in self.events_data 
#             if event['matchId'] == match_id and event['teamId'] == self.barca_id
#         ]
        
#         # Filter for passes only
#         passes = [event for event in match_events if event['eventName'] == 'Pass']
        
#         if not passes:
#             print(f"No passes found for match {match_id}")
#             return None, None, None
        
#         # Sort passes by time
#         passes.sort(key=lambda x: (x['matchPeriod'], x['eventSec']))
        
#         # Calculate average positions for each player
#         player_positions = defaultdict(list)
#         for event in passes:
#             if event['positions']:
#                 player_id = event['playerId']
#                 x, y = event['positions'][0]['x'], event['positions'][0]['y']
#                 player_positions[player_id].append((x, y))
        
#         avg_positions = {}
#         for player_id, positions in player_positions.items():
#             if positions:
#                 avg_x = np.mean([pos[0] for pos in positions])
#                 avg_y = np.mean([pos[1] for pos in positions])
#                 avg_positions[player_id] = (avg_x, avg_y)
        
#         # Build passing network
#         G = nx.Graph()
#         passing_counts = defaultdict(int)
        
#         # Connect consecutive passes
#         for i in range(len(passes) - 1):
#             current_pass = passes[i]
#             next_pass = passes[i + 1]
            
#             # Check if passes are reasonably close in time (within 30 seconds)
#             if next_pass['eventSec'] - current_pass['eventSec'] <= 30:
#                 passer = current_pass['playerId']
#                 receiver = next_pass['playerId']
                
#                 if passer != receiver:  # Don't connect a player to themselves
#                     passing_counts[(passer, receiver)] += 1
        
#         # Add edges to graph
#         for (passer, receiver), count in passing_counts.items():
#             if passer in avg_positions and receiver in avg_positions:
#                 G.add_edge(passer, receiver, weight=count)
        
#         return G, avg_positions, passing_counts
    
#     def plot_passing_network(self, match_id, match_info, save_path=None):
#         """Create a visualization of the passing network"""
#         G, positions, passing_counts = self.create_passing_network(match_id)
        
#         if not G or not positions:
#             print(f"Could not create network for match {match_id}")
#             return None
        
#         # Create figure
#         fig, ax = plt.subplots(figsize=(12, 8))
        
#         # Draw soccer pitch
#         self.draw_pitch(ax)
        
#         # Calculate node sizes based on degree centrality
#         centrality = nx.degree_centrality(G)
#         node_sizes = [centrality.get(node, 0) * 1000 + 200 for node in G.nodes()]
        
#         # Prepare positions for plotting
#         pos_dict = {}
#         for player_id, (x, y) in positions.items():
#             if player_id in G.nodes():
#                 pos_dict[player_id] = (x, y)
        
#         # Draw network
#         nx.draw_networkx_nodes(G, pos_dict, node_size=node_sizes, 
#                               node_color='lightblue', alpha=0.7, ax=ax)
        
#         # Draw edges with thickness proportional to passing frequency
#         edges = G.edges()
#         weights = [G[u][v]['weight'] for u, v in edges]
#         max_weight = max(weights) if weights else 1
#         edge_widths = [w / max_weight * 5 + 0.5 for w in weights]
        
#         nx.draw_networkx_edges(G, pos_dict, width=edge_widths, 
#                               alpha=0.6, edge_color='gray', ax=ax)
        
#         # Add player labels
#         labels = {player_id: self.get_player_name(player_id).split()[-1] 
#                  for player_id in G.nodes()}
#         nx.draw_networkx_labels(G, pos_dict, labels, font_size=8, ax=ax)
        
#         # Set title and formatting
#         ax.set_title(f'Barcelona Passing Network\n{match_info["label"]}', 
#                     fontsize=16, fontweight='bold')
#         ax.set_xlim(-5, 105)
#         ax.set_ylim(-5, 105)
#         ax.set_aspect('equal')
        
#         # Add network statistics as text
#         density = nx.density(G)
#         num_nodes = G.number_of_nodes()
#         num_edges = G.number_of_edges()
        
#         stats_text = f'Network Density: {density:.3f}\nPlayers: {num_nodes}\nConnections: {num_edges}'
#         ax.text(102, 95, stats_text, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", 
#                 facecolor="white", alpha=0.8), verticalalignment='top')
        
#         if save_path:
#             plt.savefig(save_path, dpi=300, bbox_inches='tight')
#             print(f"Network plot saved as {save_path}")
        
#         plt.tight_layout()
#         return fig, ax
    
#     def draw_pitch(self, ax):
#         """Draw a soccer pitch on the given axes"""
#         # Pitch outline
#         pitch = plt.Rectangle((0, 0), 100, 100, linewidth=2, 
#                              edgecolor='white', facecolor='green', alpha=0.3)
#         ax.add_patch(pitch)
        
#         # Center line
#         ax.plot([50, 50], [0, 100], color='white', linewidth=2)
        
#         # Center circle
#         center_circle = plt.Circle((50, 50), 10, color='white', fill=False, linewidth=2)
#         ax.add_patch(center_circle)
        
#         # Penalty areas
#         penalty_left = plt.Rectangle((0, 20), 16, 60, linewidth=2, 
#                                    edgecolor='white', fill=False)
#         penalty_right = plt.Rectangle((84, 20), 16, 60, linewidth=2, 
#                                     edgecolor='white', fill=False)
#         ax.add_patch(penalty_left)
#         ax.add_patch(penalty_right)
        
#         # Goal areas
#         goal_left = plt.Rectangle((0, 35), 5, 30, linewidth=2, 
#                                 edgecolor='white', fill=False)
#         goal_right = plt.Rectangle((95, 35), 5, 30, linewidth=2, 
#                                  edgecolor='white', fill=False)
#         ax.add_patch(goal_left)
#         ax.add_patch(goal_right)
        
#         ax.set_facecolor('darkgreen')
#         ax.grid(False)
#         ax.set_xticks([])
#         ax.set_yticks([])
    
#     def analyze_network_metrics(self, match_id):
#         """Analyze various network metrics for a match"""
#         G, positions, passing_counts = self.create_passing_network(match_id)
        
#         if not G:
#             return None
        
#         # Calculate various centrality measures
#         metrics = {
#             'density': nx.density(G),
#             'nodes': G.number_of_nodes(),
#             'edges': G.number_of_edges(),
#             'betweenness_centrality': nx.betweenness_centrality(G),
#             'closeness_centrality': nx.closeness_centrality(G),
#             'degree_centrality': nx.degree_centrality(G),
#             'pagerank': nx.pagerank(G)
#         }
        
#         return metrics

# def main():
#     """Main function to generate Barcelona passing network graphs"""
    
#     # Initialize analyzer
#     analyzer = BarcelonaNetworkAnalyzer()
    
#     # Define file paths
#     network_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     events_path = os.path.join(network_dir, 'data', 'events', 'events_Spain.json')
#     matches_path = os.path.join(network_dir, 'data', 'matches', 'matches_Spain.json')
#     teams_path = os.path.join(network_dir, 'data', 'teams.json')
#     players_path = os.path.join(network_dir, 'data', 'players.json')
    
#     # Load data
#     if not analyzer.load_data(events_path, matches_path, teams_path, players_path):
#         print("Failed to load data files. Please check file paths.")
#         return
    
#     # Find winning matches
#     winning_matches = analyzer.find_winning_matches()
    
#     if not winning_matches:
#         print("No winning matches found for FC Barcelona in the dataset.")
#         return
    
#     print(f"Found {len(winning_matches)} winning matches for Barcelona")
    
#     # Analyze first few winning matches
#     for i, match_info in enumerate(winning_matches[:5]):  # Limit to first 5 matches
#         print(f"\nAnalyzing match {i+1}: {match_info['label']}")
        
#         # Generate network visualization
#         output_path = os.path.join(network_dir, f'barca_network_match_{match_info["match_id"]}.png')
#         fig, ax = analyzer.plot_passing_network(match_info['match_id'], match_info, output_path)
        
#         if fig:
#             # Analyze network metrics
#             metrics = analyzer.analyze_network_metrics(match_info['match_id'])
            
#             if metrics:
#                 print(f"Network metrics for {match_info['label']}:")
#                 print(f"  Density: {metrics['density']:.3f}")
#                 print(f"  Nodes: {metrics['nodes']}")
#                 print(f"  Edges: {metrics['edges']}")
                
#                 # Show top 3 players by betweenness centrality
#                 top_players = sorted(metrics['betweenness_centrality'].items(), 
#                                    key=lambda x: x[1], reverse=True)[:3]
#                 print("  Top players by betweenness centrality:")
#                 for player_id, centrality in top_players:
#                     player_name = analyzer.get_player_name(player_id)
#                     print(f"    {player_name}: {centrality:.3f}")
        
#         plt.show()  # Display the plot
        
#     print(f"\nAll network visualizations have been saved to the network directory.")

# if __name__ == '__main__':
#     main()