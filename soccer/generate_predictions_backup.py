import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import soccerdata as sd
import json
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# --- Configuration ---
LEAGUE = 'ESP-La Liga'
TRAIN_SEASON = "23/24"  # Single season for training
PREDICT_SEASON = "24/25"  # Season for prediction
OUTPUT_JSON_FILE = "predictions_dashboard_data.json"



TEAM_NAME_FIXES = {
    "Athletic Club": "Athletic Club",
    "Getafe CF": "Getafe",
    "Real Betis": "Betis",
    "Girona FC": "Girona",
    "RC Celta": "Celta Vigo",
    "Deportivo Alavés": "Alavés",
    "UD Las Palmas": "Las Palmas",
    "Sevilla FC": "Sevilla",
    "CA Osasuna": "Osasuna",
    "Leganés": "Leganés",
    "Valencia CF": "Valencia",
    "FC Barcelona": "Barcelona",
    "Real Sociedad": "Real Sociedad",
    "Rayo Vallecano": "Rayo Vallecano",
    "RCD Mallorca": "Mallorca",
    "Real Madrid": "Real Madrid",
    "Real Valladolid CF": "Valladolid",
    "RCD Espanyol": "Espanyol",
    "Villarreal CF": "Villarreal",
    "Atlético de Madrid": "Atlético Madrid"
}




def convert_season_format(season_str):
    """Convert season format from 'YYYY' to 'YY/YY' format"""
    if len(season_str) == 4:  # e.g., "2324" -> "23/24"
        return f"{season_str[:2]}/{season_str[2:]}"
    return season_str

def get_and_prepare_data(seasons):
    print(f"Fetching data for seasons: {seasons}...")
    
    fbref = sd.FBref(leagues=[LEAGUE], seasons=seasons)
    matches = fbref.read_schedule()
    
    print(f"[DEBUG] DataFrame size after fbref.read_schedule(): {len(matches)} rows.")
    
    # Reset index to get season as column
    matches = matches.reset_index()
    
    # Convert season format for matching
    matches['season_formatted'] = matches['season'].apply(convert_season_format)
    
    print(f"[DEBUG] Unique seasons in data: {matches['season_formatted'].unique()}")
    print(f"[DEBUG] Looking for training season: {TRAIN_SEASON}")
    
    # Ensure date is datetime
    matches['date'] = pd.to_datetime(matches['date'])
    matches = matches.sort_values(by='date')
    
    # Extract scores - handle different dash types
    matches['score'] = matches['score'].astype(str)
    score_pattern = r'(\d+)[–\-—](\d+)'
    score_extracted = matches['score'].str.extract(score_pattern)
    
    # Only keep matches with valid scores (completed matches)
    valid_scores = ~score_extracted.isna().any(axis=1)
    matches = matches[valid_scores].copy()
    
    matches[['home_score', 'away_score']] = score_extracted[valid_scores].astype(float)
    
    print(f"[DEBUG] DataFrame size after score extraction: {len(matches)} rows.")
    
    # Define match outcome
    def get_match_outcome(row):
        if row['home_score'] > row['away_score']:
            return 0  # Home Win
        elif row['home_score'] == row['away_score']:
            return 1  # Draw
        else:
            return 2  # Away Win
    
    matches['outcome'] = matches.apply(get_match_outcome, axis=1)
    
    print(f"[DEBUG] Sample matches with outcomes:")
    print(matches[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'outcome', 'season_formatted']].head())
    
    # Get unique teams
    teams = pd.concat([matches['home_team'], matches['away_team']]).unique()
    print(f"[DEBUG] Found {len(teams)} unique teams")
    
    # Simple feature engineering - use season averages
    features = []
    
    # Group by season and team to calculate averages
    for season in matches['season_formatted'].unique():
        season_matches = matches[matches['season_formatted'] == season]
        
        # Calculate team stats for this season
        team_stats = {}
        for team in teams:
            home_matches = season_matches[season_matches['home_team'] == team]
            away_matches = season_matches[season_matches['away_team'] == team]
            
            # Goals for/against
            home_gf = home_matches['home_score'].sum()
            home_ga = home_matches['away_score'].sum()
            away_gf = away_matches['away_score'].sum()
            away_ga = away_matches['home_score'].sum()
            
            total_gf = home_gf + away_gf
            total_ga = home_ga + away_ga
            total_matches = len(home_matches) + len(away_matches)
            
            # Points
            home_wins = len(home_matches[home_matches['outcome'] == 0])
            home_draws = len(home_matches[home_matches['outcome'] == 1])
            away_wins = len(away_matches[away_matches['outcome'] == 2])
            away_draws = len(away_matches[away_matches['outcome'] == 1])
            
            total_points = (home_wins + away_wins) * 3 + (home_draws + away_draws) * 1
            
            team_stats[team] = {
                'gf_avg': total_gf / max(total_matches, 1),
                'ga_avg': total_ga / max(total_matches, 1),
                'pts_avg': total_points / max(total_matches, 1)
            }
        
        # Create features for each match in this season
        for _, match in season_matches.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            
            # Use previous season stats if available, otherwise use current season partial stats
            home_stats = team_stats.get(home_team, {'gf_avg': 1.0, 'ga_avg': 1.0, 'pts_avg': 1.0})
            away_stats = team_stats.get(away_team, {'gf_avg': 1.0, 'ga_avg': 1.0, 'pts_avg': 1.0})
            
            features.append({
                'home_team': home_team,
                'away_team': away_team,
                'home_gf_avg': home_stats['gf_avg'],
                'home_ga_avg': home_stats['ga_avg'],
                'home_pts_avg': home_stats['pts_avg'],
                'away_gf_avg': away_stats['gf_avg'],
                'away_ga_avg': away_stats['ga_avg'],
                'away_pts_avg': away_stats['pts_avg'],
                'outcome': match['outcome'],
                'season': season,
                'date': match['date']
            })
    
    processed_data = pd.DataFrame(features)
    
    print(f"[DEBUG] Processed DataFrame size: {len(processed_data)} rows.")
    print(f"[DEBUG] Seasons in processed data: {processed_data['season'].unique()}")
    
    return processed_data, teams

def create_fixtures_from_schedule(schedule_df, season_stats, season_label):
    """Create fixture list using actual season schedule"""
    print("Creating fixtures using real schedule...")

    all_teams_in_schedule = set(schedule_df['home_team']) | set(schedule_df['away_team'])
    missing_stats = [team for team in all_teams_in_schedule if team not in season_stats]
    print("Teams missing from season_stats:", missing_stats)



    def normalize_team_name(name):
        return TEAM_NAME_FIXES.get(name, name)

    schedule_df['home_team'] = schedule_df['home_team'].apply(normalize_team_name)
    schedule_df['away_team'] = schedule_df['away_team'].apply(normalize_team_name)

    fixtures = []

    for _, row in schedule_df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']

        # Get season stats or use fallback
        home_stats = season_stats.get(home_team, {'gf_avg': 1.5, 'ga_avg': 1.0, 'pts_avg': 1.5})
        away_stats = season_stats.get(away_team, {'gf_avg': 1.2, 'ga_avg': 1.2, 'pts_avg': 1.2})

        fixture = {
            'home_team': home_team,
            'away_team': away_team,
            'home_gf_avg': home_stats['gf_avg'],
            'home_ga_avg': home_stats['ga_avg'],
            'home_pts_avg': home_stats['pts_avg'],
            'away_gf_avg': away_stats['gf_avg'],
            'away_ga_avg': away_stats['ga_avg'],
            'away_pts_avg': away_stats['pts_avg'],
            'season': season_label
        }

        # Optionally include match date or matchday if available
        if 'date' in row:
            fixture['date'] = row['date']
        if 'matchday' in row:
            fixture['matchday'] = row['matchday']

        fixtures.append(fixture)

    print(f"Created {len(fixtures)} fixtures from schedule")
    return pd.DataFrame(fixtures)


def simulate_league_standings(predictions_df, teams):
    """Simulate league standings based on predictions"""
    team_stats = {team: {'points': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'gf': 0, 'ga': 0, 'played': 0} 
                  for team in teams}
    
    for _, row in predictions_df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        predicted_outcome = row['predicted_outcome']
        
        # Update matches played
        team_stats[home_team]['played'] += 1
        team_stats[away_team]['played'] += 1
        
        # Simulate realistic scores based on team averages
        home_gf_avg = row.get('home_gf_avg', 1.3)
        away_gf_avg = row.get('away_gf_avg', 1.1)
        
        if predicted_outcome == 0:  # Home Win
            team_stats[home_team]['points'] += 3
            team_stats[home_team]['wins'] += 1
            team_stats[away_team]['losses'] += 1
            home_goals = max(1, min(4, int(home_gf_avg * 1.2)))
            away_goals = max(0, min(2, int(away_gf_avg * 0.8)))
        elif predicted_outcome == 1:  # Draw
            team_stats[home_team]['points'] += 1
            team_stats[away_team]['points'] += 1
            team_stats[home_team]['draws'] += 1
            team_stats[away_team]['draws'] += 1
            home_goals = max(1, min(3, int(home_gf_avg)))
            away_goals = home_goals
        else:  # Away Win
            team_stats[away_team]['points'] += 3
            team_stats[away_team]['wins'] += 1
            team_stats[home_team]['losses'] += 1
            away_goals = max(1, min(4, int(away_gf_avg * 1.2)))
            home_goals = max(0, min(2, int(home_gf_avg * 0.8)))
        
        team_stats[home_team]['gf'] += home_goals
        team_stats[home_team]['ga'] += away_goals
        team_stats[away_team]['gf'] += away_goals
        team_stats[away_team]['ga'] += home_goals
    
    # Convert to standings format
    standings = []
    for team in teams:
        if team_stats[team]['played'] > 0:  # Only include teams that played
            stats = team_stats[team]
            gd = stats['gf'] - stats['ga']
            standings.append({
                'team': team,
                'pos': 0,  # Will be set after sorting
                'played': stats['played'],
                'wins': stats['wins'],
                'draws': stats['draws'],
                'losses': stats['losses'],
                'gf': stats['gf'],
                'ga': stats['ga'],
                'gd': gd,
                'pts': stats['points']
            })
    
    # Sort by points, then by goal difference
    standings.sort(key=lambda x: (x['pts'], x['gd']), reverse=True)
    
    # Set positions
    for i, team_data in enumerate(standings):
        team_data['pos'] = i + 1
    
    return standings

def train_and_predict(model_name, model_instance, X_train, y_train, X_predict):
    """Train model and generate predictions"""
    print(f"\nTraining {model_name}...")
    
    # Create pipeline with scaling
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', model_instance)
    ])
    
    # Fit the pipeline
    pipeline.fit(X_train, y_train)
    
    # Generate predictions
    predictions = pipeline.predict(X_predict)
    probabilities = pipeline.predict_proba(X_predict)
    
    print(f"✓ {model_name} training completed")
    return predictions, probabilities

# --- Main Execution ---
if __name__ == "__main__":
    print("🏈 La Liga Prediction System")
    print("=" * 50)
    
    # Get historical data
    processed_data, all_teams = get_and_prepare_data([TRAIN_SEASON, PREDICT_SEASON])
    
    # Split training data
    train_data = processed_data[processed_data['season'] == TRAIN_SEASON]
    
    print(f"\n[DEBUG] Training data shape: {train_data.shape}")
    print(f"[DEBUG] Available seasons: {processed_data['season'].unique()}")
    
    if len(train_data) == 0:
        print(f"❌ No training data found for season {TRAIN_SEASON}")
        print("Available seasons:", processed_data['season'].unique())
        exit()
    
    # Calculate season stats for future match creation
    season_stats = {}
    for team in all_teams:
        team_matches = train_data[(train_data['home_team'] == team) | (train_data['away_team'] == team)]
        if len(team_matches) > 0:
            home_matches = team_matches[team_matches['home_team'] == team]
            away_matches = team_matches[team_matches['away_team'] == team]
            
            # Calculate averages
            avg_gf = (home_matches['home_gf_avg'].mean() + away_matches['away_gf_avg'].mean()) / 2
            avg_ga = (home_matches['home_ga_avg'].mean() + away_matches['away_ga_avg'].mean()) / 2
            avg_pts = (home_matches['home_pts_avg'].mean() + away_matches['away_pts_avg'].mean()) / 2
            
            season_stats[team] = {
                'gf_avg': avg_gf if not pd.isna(avg_gf) else 1.2,
                'ga_avg': avg_ga if not pd.isna(avg_ga) else 1.2,
                'pts_avg': avg_pts if not pd.isna(avg_pts) else 1.2
            }
    
    schedule_df = pd.read_csv('24-25_schedule.csv')
    future_matches = create_fixtures_from_schedule(schedule_df, season_stats, season_label='2024/25')

    # future_matches = create_future_matches(all_teams, season_stats)
    
    # Prepare features
    feature_cols = ['home_gf_avg', 'home_ga_avg', 'home_pts_avg', 'away_gf_avg', 'away_ga_avg', 'away_pts_avg']
    
    X_train = train_data[feature_cols]
    y_train = train_data['outcome']
    X_predict = future_matches[feature_cols]
    
    print(f"\n📊 Training on {len(X_train)} matches")
    print(f"🔮 Predicting {len(X_predict)} future matches")
    
    # Define models
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(objective='multi:softmax', n_estimators=100, random_state=42, verbosity=0),
        "LightGBM": LGBMClassifier(objective='multiclass', num_class=3, random_state=42, verbose=-1)
    }
    
    all_dashboard_data = {}
    
    # Train models and generate predictions
    for name, model_instance in models.items():
        try:
            predictions, probabilities = train_and_predict(name, model_instance, X_train, y_train, X_predict)
            
            # Add predictions to future matches
            future_matches_copy = future_matches.copy()
            future_matches_copy['predicted_outcome'] = predictions
            future_matches_copy['predicted_proba'] = [p.tolist() for p in probabilities]
            
            # Generate standings
            standings = simulate_league_standings(future_matches_copy, all_teams)
            
            # Store results
            scenario_key = f"scenario_{name.replace(' ', '_').lower()}"
            all_dashboard_data[scenario_key] = {
                "label": f"{name} Predictions",
                "description": f"La Liga {PREDICT_SEASON} predictions using {name} trained on {TRAIN_SEASON} data",
                "standings": standings,
                "predictions": future_matches_copy[['home_team', 'away_team', 'predicted_outcome']].to_dict('records'),
                "model_info": {
                    "training_season": TRAIN_SEASON,
                    "prediction_season": PREDICT_SEASON,
                    "training_matches": len(X_train),
                    "predicted_matches": len(X_predict)
                }
            }
            
            print(f"✅ {name} completed")
            if standings:
                print(f"   🏆 Top 3: {standings[0]['team']}, {standings[1]['team']}, {standings[2]['team']}")
            
        except Exception as e:
            print(f"❌ Error with {name}: {str(e)}")
            continue
    
    # Export results
    if all_dashboard_data:
        with open(OUTPUT_JSON_FILE, 'w') as f:
            json.dump(all_dashboard_data, f, indent=2)
        
        print(f"\n🎉 SUCCESS!")
        print(f"📁 Results exported to {OUTPUT_JSON_FILE}")
        print(f"📈 Generated {len(all_dashboard_data)} prediction scenarios")
        
        # Print summary
        print(f"\n📋 Summary:")
        print(f"   Training Season: {TRAIN_SEASON}")
        print(f"   Prediction Season: {PREDICT_SEASON}")
        print(f"   Training Matches: {len(X_train)}")
        print(f"   Predicted Matches: {len(X_predict)}")
        print(f"   Teams: {len(all_teams)}")
    else:
        print("❌ No successful predictions generated")