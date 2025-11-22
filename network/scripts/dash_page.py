# import dash
# from dash import dcc, html, Input, Output, dash_table
# import plotly.graph_objects as go
# import plotly.express as px
# from plotly.subplots import make_subplots
# import pandas as pd
# import numpy as np
# import networkx as nx
# from firstscript import BarcelonaPassingAnalyzer  # Import our analyzer class

# class BarcelonaDashboard:
#     def __init__(self, data_dir):
#         self.analyzer = BarcelonaPassingAnalyzer(data_dir)
#         self.app = dash.Dash(__name__)
#         self.barca_matches = self.analyzer.get_barca_matches()
#         self.setup_layout()
#         self.setup_callbacks()
    
#     def setup_layout(self):
#         """Set up the dashboard layout"""
#         # Prepare match data for the table
#         matches_df = pd.DataFrame(self.barca_matches)
        
#         self.app.layout = html.Div([
#             html.H1("FC Barcelona Passing Network Analysis", 
#                    style={'textAlign': 'center', 'marginBottom': 30}),
            
#             # Match selection and statistics panel
#             html.Div([
#                 html.Div([
#                     html.H3("Match Selection"),
#                     html.Label("Filter by outcome:"),
#                     dcc.Dropdown(
#                         id='outcome-filter',
#                         options=[
#                             {'label': 'All Matches', 'value': 'all'},
#                             {'label': 'Wins Only', 'value': 'win'},
#                             {'label': 'Losses Only', 'value': 'loss'},
#                             {'label': 'Draws Only', 'value': 'draw'}
#                         ],
#                         value='win',
#                         style={'marginBottom': 20}
#                     ),
                    
#                     html.Label("Select a match:"),
#                     dcc.Dropdown(
#                         id='match-dropdown',
#                         style={'marginBottom': 20}
#                     ),
                    
#                     html.Div(id='match-stats')
#                 ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 
#                          'padding': '20px'}),
                
#                 # Network visualization
#                 html.Div([
#                     dcc.Graph(id='network-graph', style={'height': '600px'})
#                 ], style={'width': '68%', 'display': 'inline-block', 'marginLeft': '2%'})
#             ]),
            
#             # Analysis panels
#             html.Div([
#                 html.Div([
#                     html.H3("Top Players by Centrality"),
#                     html.Div(id='top-players-table')
#                 ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),
                
#                 html.Div([
#                     html.H3("Network Metrics Comparison"),
#                     dcc.Graph(id='metrics-comparison')
#                 ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%', 'padding': '20px'})
#             ]),
            
#             # Match results table
#             html.Div([
#                 html.H3("All Matches Overview"),
#                 dash_table.DataTable(
#                     id='matches-table',
#                     columns=[
#                         {'name': 'Match', 'id': 'label'},
#                         {'name': 'Outcome', 'id': 'outcome'},
#                         {'name': 'Date', 'id': 'date'}
#                     ],
#                     data=matches_df.to_dict('records'),
#                     style_cell={'textAlign': 'left'},
#                     style_data_conditional=[
#                         {
#                             'if': {'filter_query': '{outcome} = win'},
#                             'backgroundColor': '#d4edda',
#                             'color': 'black',
#                         },
#                         {
#                             'if': {'filter_query': '{outcome} = loss'},
#                             'backgroundColor': '#f8d7da',
#                             'color': 'black',
#                         },
#                         {
#                             'if': {'filter_query': '{outcome} = draw'},
#                             'backgroundColor': '#fff3cd',
#                             'color': 'black',
#                         }
#                     ],
#                     page_size=10,
#                     style_table={'height': '400px', 'overflowY': 'auto'}
#                 )
#             ], style={'padding': '20px'})
#         ])
    
#     def setup_callbacks(self):
#         """Set up all the callback functions"""
        
#         @self.app.callback(
#             Output('match-dropdown', 'options'),
#             Output('match-dropdown', 'value'),
#             Input('outcome-filter', 'value')
#         )
#         def update_match_dropdown(outcome_filter):
#             """Update match dropdown based on outcome filter"""
#             if outcome_filter == 'all':
#                 filtered_matches = self.barca_matches
#             else:
#                 filtered_matches = [m for m in self.barca_matches if m['outcome'] == outcome_filter]
            
#             options = [
#                 {'label': f"{match['label']} ({match['outcome'].title()})", 'value': match['match_id']}
#                 for match in filtered_matches
#             ]
            
#             value = options[0]['value'] if options else None
#             return options, value
        
#         @self.app.callback(
#             Output('network-graph', 'figure'),
#             Output('match-stats', 'children'),
#             Output('top-players-table', 'children'),
#             Input('match-dropdown', 'value')
#         )
#         def update_network_visualization(selected_match_id):
#             """Update the network visualization and related stats"""
#             if not selected_match_id:
#                 empty_fig = go.Figure()
#                 empty_fig.add_annotation(text="No match selected", xref="paper", yref="paper",
#                                        x=0.5, y=0.5, xanchor='center', yanchor='middle',
#                                        showarrow=False, font=dict(size=20))
#                 return empty_fig, "No match selected", "No data available"
            
#             # Find match info
#             match_info = next((m for m in self.barca_matches if m['match_id'] == selected_match_id), None)
#             if not match_info:
#                 return go.Figure(), "Match not found", "No data available"
            
#             # Create network visualization
#             fig, metrics = self.analyzer.create_network_visualization(selected_match_id, match_info)
            
#             if not fig:
#                 empty_fig = go.Figure()
#                 empty_fig.add_annotation(text="No passing data available for this match", 
#                                        xref="paper", yref="paper", x=0.5, y=0.5, 
#                                        xanchor='center', yanchor='middle', showarrow=False)
#                 return empty_fig, "No data available", "No data available"
            
#             # Match statistics
#             G = metrics['graph']
#             stats_div = html.Div([
#                 html.P(f"Network Density: {nx.density(G):.3f}"),
#                 html.P(f"Number of Players: {G.number_of_nodes()}"),
#                 html.P(f"Passing Connections: {G.number_of_edges()}"),
#                 html.P(f"Outcome: {match_info['outcome'].title()}"),
#             ])
            
#             # Top players table
#             top_betweenness = sorted(metrics['betweenness'].items(), 
#                                    key=lambda x: x[1], reverse=True)[:5]
            
#             players_data = []
#             for player_id, centrality in top_betweenness:
#                 player_name = self.analyzer.get_player_name(player_id)
#                 degree = metrics['degree'].get(player_id, 0)
#                 pagerank = metrics['pagerank'].get(player_id, 0)
                
#                 players_data.append({
#                     'Player': player_name,
#                     'Betweenness': f"{centrality:.3f}",
#                     'Degree': f"{degree}",
#                     'PageRank': f"{pagerank:.3f}"
#                 })
            
#             top_players_table = dash_table.DataTable(
#                 columns=[
#                     {'name': 'Player', 'id': 'Player'},
#                     {'name': 'Betweenness', 'id': 'Betweenness'},
#                     {'name': 'Degree', 'id': 'Degree'},
#                     {'name': 'PageRank', 'id': 'PageRank'}
#                 ],
#                 data=players_data,
#                 style_cell={'textAlign': 'left'},
#                 style_header={'backgroundColor': 'lightblue'}
#             )
            
#             return fig, stats_div, top_players_table
        
#         @self.app.callback(
#             Output('metrics-comparison', 'figure'),
#             Input('outcome-filter', 'value')
#         )
#         def update_metrics_comparison(outcome_filter):
#             """Create comparison chart of network metrics across matches"""
#             if outcome_filter == 'all':
#                 filtered_matches = self.barca_matches
#             else:
#                 filtered_matches = [m for m in self.barca_matches if m['outcome'] == outcome_filter]
            
#             # Calculate metrics for each match
#             metrics_data = []
#             for match in filtered_matches[:10]:  # Limit to first 10 for performance
#                 _, _, player_stats = self.analyzer.extract_passing_network(match['match_id'])
#                 if player_stats:
#                     metrics = self.analyzer.calculate_network_metrics({}, player_stats)
#                     if 'graph' in metrics:
#                         G = metrics['graph']
#                         metrics_data.append({
#                             'match': match['label'][:20] + '...' if len(match['label']) > 20 else match['label'],
#                             'density': nx.density(G),
#                             'nodes': G.number_of_nodes(),
#                             'edges': G.number_of_edges(),
#                             'outcome': match['outcome']
#                         })
            
#             if not metrics_data:
#                 fig = go.Figure()
#                 fig.add_annotation(text="No data available", xref="paper", yref="paper",
#                                  x=0.5, y=0.5, xanchor='center', yanchor='middle', showarrow=False)
#                 return fig
            
#             df = pd.DataFrame(metrics_data)
            
#             fig = make_subplots(
#                 rows=2, cols=2,
#                 subplot_titles=('Network Density', 'Number of Nodes', 'Number of Edges', 'Metrics by Outcome'),
#                 specs=[[{"secondary_y": False}, {"secondary_y": False}],
#                        [{"secondary_y": False}, {"secondary_y": False}]]
#             )
            
#             # Density plot
#             colors = {'win': 'green', 'loss': 'red', 'draw': 'orange'}
#             for outcome in df['outcome'].unique():
#                 outcome_data = df[df['outcome'] == outcome]
#                 fig.add_trace(
#                     go.Scatter(x=outcome_data['match'], y=outcome_data['density'], 
#                              mode='markers', name=f'{outcome.title()} - Density',
#                              marker=dict(color=colors.get(outcome, 'blue'))),
#                     row=1, col=1
#                 )
            
#             # Nodes plot
#             fig.add_trace(
#                 go.Bar(x=df['match'], y=df['nodes'], name='Nodes', marker_color='lightblue'),
#                 row=1, col=2
#             )
            
#             # Edges plot
#             fig.add_trace(
#                 go.Bar(x=df['match'], y=df['edges'], name='Edges', marker_color='lightcoral'),
#                 row=2, col=1
#             )
            
#             # Box plot by outcome
#             for outcome in df['outcome'].unique():
#                 outcome_data = df[df['outcome'] == outcome]
#                 fig.add_trace(
#                     go.Box(y=outcome_data['density'], name=f'{outcome.title()}',
#                           marker=dict(color=colors.get(outcome, 'blue'))),
#                     row=2, col=2
#                 )
            
#             fig.update_layout(height=600, showlegend=True, title_text="Network Metrics Analysis")
#             return fig
    
#     def run(self, debug=True, port=8050):
#         """Run the dashboard"""
#         self.app.run_server(debug=debug, port=port)

# def main():
#     """Main function to run the dashboard"""
#     data_dir = '../data'
#     dashboard = BarcelonaDashboard(data_dir)
    
#     print("Starting Barcelona Passing Network Dashboard...")
#     print("Open http://localhost:8050 in your browser")
#     dashboard.run()

# if __name__ == '__main__':
#     main()