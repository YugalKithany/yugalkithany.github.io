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


# Match and team data sourced from FBref.com, courtesy of Sports Reference LLC, accessed via the soccerdata Python package.
# Custom schedule and standings data compiled by the author.
# Modeling powered by scikit-learn, XGBoost, and LightGBM.

# --- Configuration ---
LEAGUE = 'ESP-La Liga'
TRAIN_SEASONS = ["20/21", "21/22", "22/23", "23/24"]  # Multiple seasons for training
PREDICT_SEASONS = ["24/25", "25/26"]  # Both seasons for prediction
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
    "RCD Espanyol de Barcelona": "Espanyol",
    "Villarreal CF": "Villarreal",
    "Atlético de Madrid": "Atletico"  # Match the CSV format
}

# Mapping for promoted teams to use relegated teams' data
PROMOTED_TO_RELEGATED_MAPPING = {
    "Levante UD": "Valladolid",
    "Elche CF": "Las Palmas", 
    "Real Oviedo": "Leganés"
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
    print(f"[DEBUG] Looking for training seasons: {TRAIN_SEASONS}")
    
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
    
    # Get unique teams across all seasons
    teams = pd.concat([matches['home_team'], matches['away_team']]).unique()
    print(f"[DEBUG] Found {len(teams)} unique teams")
    
    # Enhanced feature engineering with xG data
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
            
            # Estimate xG based on performance (simplified approach)
            # In real implementation, you'd get actual xG data from FBref
            attack_strength = total_gf / max(total_matches, 1)
            defense_strength = total_ga / max(total_matches, 1)
            
            # Simulate xG based on goals and performance
            xg_for = attack_strength * 0.95 + np.random.normal(0, 0.1)  # Slight variation
            xg_against = defense_strength * 0.95 + np.random.normal(0, 0.1)
            
            team_stats[team] = {
                'gf_avg': total_gf / max(total_matches, 1),
                'ga_avg': total_ga / max(total_matches, 1),
                'pts_avg': total_points / max(total_matches, 1),
                'xg_avg': max(0.1, xg_for),  # Ensure positive
                'xga_avg': max(0.1, xg_against)
            }
        
        # Create features for each match in this season
        for _, match in season_matches.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            
            # Use team stats
            home_stats = team_stats.get(home_team, {'gf_avg': 1.0, 'ga_avg': 1.0, 'pts_avg': 1.0, 'xg_avg': 1.0, 'xga_avg': 1.0})
            away_stats = team_stats.get(away_team, {'gf_avg': 1.0, 'ga_avg': 1.0, 'pts_avg': 1.0, 'xg_avg': 1.0, 'xga_avg': 1.0})
            
            features.append({
                'home_team': home_team,
                'away_team': away_team,
                'home_gf_avg': home_stats['gf_avg'],
                'home_ga_avg': home_stats['ga_avg'],
                'home_pts_avg': home_stats['pts_avg'],
                'home_xg_avg': home_stats['xg_avg'],
                'home_xga_avg': home_stats['xga_avg'],
                'away_gf_avg': away_stats['gf_avg'],
                'away_ga_avg': away_stats['ga_avg'],
                'away_pts_avg': away_stats['pts_avg'],
                'away_xg_avg': away_stats['xg_avg'],
                'away_xga_avg': away_stats['xga_avg'],
                'outcome': match['outcome'],
                'season': season,
                'date': match['date']
            })
    
    processed_data = pd.DataFrame(features)
    
    print(f"[DEBUG] Processed DataFrame size: {len(processed_data)} rows.")
    print(f"[DEBUG] Seasons in processed data: {processed_data['season'].unique()}")
    
    return processed_data, teams

def load_real_standings_data():
    """Load real standings data from CSV for 24/25 season"""
    try:
        standings_df = pd.read_csv('24-25_standings.csv')
        print(f"[DEBUG] Loaded real standings data: {len(standings_df)} teams")
        
        # Normalize team names
        standings_df['team'] = standings_df['team'].apply(lambda x: TEAM_NAME_FIXES.get(x, x))
        
        # Calculate stats per game
        real_stats = {}
        for _, row in standings_df.iterrows():
            team = row['team']
            # Assume 38 games played (full season)
            games_played = 38
            
            real_stats[team] = {
                'gf_avg': row['goals for'] / games_played,
                'ga_avg': row['against'] / games_played,
                'pts_avg': row['pts'] / games_played,
                'xg_avg': row['xGA'],  # xG per game
                'xga_avg': row['xGA against']  # xGA per game
            }
        
        print(f"[DEBUG] Real stats calculated for {len(real_stats)} teams")
        return real_stats
    except Exception as e:
        print(f"[WARNING] Could not load real standings data: {e}")
        return {}

def create_fixtures_from_schedule(schedule_df, season_stats, season_label):
    """Create fixture list using actual season schedule"""
    print(f"Creating fixtures using real schedule for {season_label}...")

    def normalize_team_name(name):
        return TEAM_NAME_FIXES.get(name, name)

    schedule_df['home_team'] = schedule_df['home_team'].apply(normalize_team_name)
    schedule_df['away_team'] = schedule_df['away_team'].apply(normalize_team_name)

    all_teams_in_schedule = set(schedule_df['home_team']) | set(schedule_df['away_team'])
    
    # Handle promoted teams by mapping them to relegated teams' data
    updated_season_stats = season_stats.copy()
    
    for promoted_team, relegated_team in PROMOTED_TO_RELEGATED_MAPPING.items():
        if promoted_team in all_teams_in_schedule and promoted_team not in updated_season_stats:
            if relegated_team in updated_season_stats:
                print(f"Mapping {promoted_team} to use {relegated_team}'s historical data")
                updated_season_stats[promoted_team] = updated_season_stats[relegated_team].copy()
            else:
                print(f"Warning: {relegated_team} data not found for mapping to {promoted_team}")
    
    missing_stats = [team for team in all_teams_in_schedule if team not in updated_season_stats]
    if missing_stats:
        print(f"Teams still missing from season_stats: {missing_stats}")

    fixtures = []

    for _, row in schedule_df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        # if home_team not in team_stats or away_team not in team_stats:
        #     continue  # or log warning

        # Get season stats or use fallback
        home_stats = updated_season_stats.get(home_team, {
            'gf_avg': 1.5, 'ga_avg': 1.0, 'pts_avg': 1.5, 'xg_avg': 1.3, 'xga_avg': 1.1
        })
        away_stats = updated_season_stats.get(away_team, {
            'gf_avg': 1.2, 'ga_avg': 1.2, 'pts_avg': 1.2, 'xg_avg': 1.1, 'xga_avg': 1.2
        })

        fixture = {
            'home_team': home_team,
            'away_team': away_team,
            'home_gf_avg': home_stats['gf_avg'],
            'home_ga_avg': home_stats['ga_avg'],
            'home_pts_avg': home_stats['pts_avg'],
            'home_xg_avg': home_stats['xg_avg'],
            'home_xga_avg': home_stats['xga_avg'],
            'away_gf_avg': away_stats['gf_avg'],
            'away_ga_avg': away_stats['ga_avg'],
            'away_pts_avg': away_stats['pts_avg'],
            'away_xg_avg': away_stats['xg_avg'],
            'away_xga_avg': away_stats['xga_avg'],
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
    """Simulate league standings based on predictions with xG stats"""
    # team_stats = {team: {
    #     'points': 0, 'wins': 0, 'draws': 0, 'losses': 0, 
    #     'gf': 0, 'ga': 0, 'played': 0, 'xg': 0, 'xga': 0
    # } for team in teams}

    from collections import defaultdict

    default_team_data = lambda: {
        'points': 0, 'wins': 0, 'draws': 0, 'losses': 0,
        'gf': 0, 'ga': 0, 'played': 0, 'xg': 0, 'xga': 0
    }
    team_stats = defaultdict(default_team_data)

    for _, row in predictions_df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        predicted_outcome = row['predicted_outcome']
        
        # Update matches played
        team_stats[home_team]['played'] += 1
        team_stats[away_team]['played'] += 1
        
        # Get xG values
        home_xg = row.get('home_xg_avg', 1.3)
        away_xg = row.get('away_xg_avg', 1.1)
        home_xga = row.get('home_xga_avg', 1.1)
        away_xga = row.get('away_xga_avg', 1.2)
        
        # Update xG stats
        team_stats[home_team]['xg'] += home_xg
        team_stats[home_team]['xga'] += home_xga
        team_stats[away_team]['xg'] += away_xg
        team_stats[away_team]['xga'] += away_xga
        
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
                'pts': stats['points'],
                'xg': round(stats['xg'], 2),
                'xga': round(stats['xga'], 2)
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
    print("🏈 Enhanced La Liga Prediction System")
    print("=" * 50)
    
    # Get historical data with expanded training seasons
    all_seasons = TRAIN_SEASONS + ["24/25"]  # Include 24/25 for feature calculation
    processed_data, all_teams = get_and_prepare_data(all_seasons)
    
    # Split training data (use multiple seasons)
    train_data = processed_data[processed_data['season'].isin(TRAIN_SEASONS)]
    
    print(f"\n[DEBUG] Training data shape: {train_data.shape}")
    print(f"[DEBUG] Training seasons: {TRAIN_SEASONS}")
    print(f"[DEBUG] Available seasons: {processed_data['season'].unique()}")
    
    if len(train_data) == 0:
        print(f"❌ No training data found for seasons {TRAIN_SEASONS}")
        print("Available seasons:", processed_data['season'].unique())
        exit()
    
    # Calculate season stats for 24/25 predictions (from historical data)
    season_stats_2425 = {}
    for team in all_teams:
        team_matches = train_data[(train_data['home_team'] == team) | (train_data['away_team'] == team)]
        if len(team_matches) > 0:
            # Calculate weighted averages across all training seasons
            avg_gf = team_matches['home_gf_avg'].mean() if team in team_matches['home_team'].values else 0
            avg_gf += team_matches['away_gf_avg'].mean() if team in team_matches['away_team'].values else 0
            avg_gf /= 2
            
            avg_ga = team_matches['home_ga_avg'].mean() if team in team_matches['home_team'].values else 0
            avg_ga += team_matches['away_ga_avg'].mean() if team in team_matches['away_team'].values else 0
            avg_ga /= 2
            
            avg_pts = team_matches['home_pts_avg'].mean() if team in team_matches['home_team'].values else 0
            avg_pts += team_matches['away_pts_avg'].mean() if team in team_matches['away_team'].values else 0
            avg_pts /= 2
            
            avg_xg = team_matches['home_xg_avg'].mean() if team in team_matches['home_team'].values else 0
            avg_xg += team_matches['away_xg_avg'].mean() if team in team_matches['away_team'].values else 0
            avg_xg /= 2
            
            avg_xga = team_matches['home_xga_avg'].mean() if team in team_matches['home_team'].values else 0
            avg_xga += team_matches['away_xga_avg'].mean() if team in team_matches['away_team'].values else 0
            avg_xga /= 2
            
            season_stats_2425[team] = {
                'gf_avg': avg_gf if not pd.isna(avg_gf) else 1.2,
                'ga_avg': avg_ga if not pd.isna(avg_ga) else 1.2,
                'pts_avg': avg_pts if not pd.isna(avg_pts) else 1.2,
                'xg_avg': avg_xg if not pd.isna(avg_xg) else 1.2,
                'xga_avg': avg_xga if not pd.isna(avg_xga) else 1.2
            }
    
    # Load real 24/25 standings for 25/26 predictions
    real_stats_2425 = load_real_standings_data()
    
    # Prepare feature columns (now including xG)
    feature_cols = ['home_gf_avg', 'home_ga_avg', 'home_pts_avg', 'home_xg_avg', 'home_xga_avg',
                    'away_gf_avg', 'away_ga_avg', 'away_pts_avg', 'away_xg_avg', 'away_xga_avg']
    
    X_train = train_data[feature_cols]
    y_train = train_data['outcome']
    
    # Define models
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(objective='multi:softmax', n_estimators=100, random_state=42, verbosity=0),
        "LightGBM": LGBMClassifier(objective='multiclass', num_class=3, random_state=42, verbose=-1)
    }
    
    all_dashboard_data = {}
    
    print(f"\n📊 Training on {len(X_train)} matches from {len(TRAIN_SEASONS)} seasons")
    
    # Generate predictions for both seasons
    for predict_season in PREDICT_SEASONS:
        print(f"\n🔮 Generating predictions for {predict_season}...")
        
        # Load appropriate schedule and stats
        if predict_season == "24/25":
            schedule_df = pd.read_csv('24-25_schedule.csv')
            season_stats = season_stats_2425
        else:  # 25/26
            schedule_df = pd.read_csv('25-26_schedule.csv')
            season_stats = real_stats_2425 if real_stats_2425 else season_stats_2425
        
        future_matches = create_fixtures_from_schedule(schedule_df, season_stats, predict_season)
        X_predict = future_matches[feature_cols]
        
        print(f"🔮 Predicting {len(X_predict)} matches for {predict_season}")
        
        # Dictionary to store predictions for this season
        season_predictions = {}
        
        # Train models and generate predictions
        for name, model_instance in models.items():
            try:
                predictions, probabilities = train_and_predict(name, model_instance, X_train, y_train, X_predict)
                
                # Add predictions to future matches
                future_matches_copy = future_matches.copy()
                future_matches_copy['predicted_outcome'] = predictions
                future_matches_copy['predicted_proba'] = [p.tolist() for p in probabilities]
                
                # Generate standings
                # standings = simulate_league_standings(future_matches_copy, all_teams)
                # season_teams = set(future_matches_copy['home_team']).union(future_matches_copy['away_team'])
                # standings = simulate_league_standings(future_matches_copy, season_teams)
                season_teams = set(future_matches_copy['home_team']) | set(future_matches_copy['away_team'])
                standings = simulate_league_standings(future_matches_copy, season_teams)

                # Store results
                scenario_key = f"scenario_{name.replace(' ', '_').lower()}_{predict_season.replace('/', '_')}"
                prediction_data = {
                    "label": f"{name} Predictions {predict_season}",
                    "description": f"La Liga {predict_season} predictions using {name} trained on {'-'.join(TRAIN_SEASONS)} data",
                    "standings": standings,
                    "predictions": future_matches_copy[['home_team', 'away_team', 'predicted_outcome']].to_dict('records'),
                    "model_info": {
                        "training_seasons": TRAIN_SEASONS,
                        "prediction_season": predict_season,
                        "training_matches": len(X_train),
                        "predicted_matches": len(X_predict),
                        "uses_real_data": predict_season == "25/26" and bool(real_stats_2425)
                    }
                }
                
                all_dashboard_data[scenario_key] = prediction_data
                season_predictions[scenario_key] = prediction_data
                
                print(f"✅ {name} completed for {predict_season}")
                if standings:
                    print(f"   🏆 Top 3: {standings[0]['team']}, {standings[1]['team']}, {standings[2]['team']}")
                
            except Exception as e:
                print(f"❌ Error with {name} for {predict_season}: {str(e)}")
                continue
        
        # Save predictions for this season separately for debugging
        if season_predictions:
            season_file = f"predictions_{predict_season.replace('/', '_')}.json"
            with open(season_file, 'w') as f:
                json.dump(season_predictions, f, indent=2)
            print(f"📁 {predict_season} predictions saved to {season_file}")
        
        print(f"✅ Completed predictions for {predict_season}")
        print(f"   Generated {len(season_predictions)} scenarios for {predict_season}")
    
    # Export results
    if all_dashboard_data:
        with open(OUTPUT_JSON_FILE, 'w') as f:
            json.dump(all_dashboard_data, f, indent=2)
        
        print(f"\n🎉 SUCCESS!")
        print(f"📁 Results exported to {OUTPUT_JSON_FILE}")
        print(f"📈 Generated {len(all_dashboard_data)} prediction scenarios")
        
        # Print summary
        print(f"\n📋 Summary:")
        print(f"   Training Seasons: {'-'.join(TRAIN_SEASONS)}")
        print(f"   Prediction Seasons: {', '.join(PREDICT_SEASONS)}")
        print(f"   Training Matches: {len(X_train)}")
        print(f"   Teams: {len(all_teams)}")
        print(f"   Features: {len(feature_cols)} (including xG metrics)")
        print(f"   Real 24/25 data used: {'Yes' if real_stats_2425 else 'No'}")
    else:
        print("❌ No successful predictions generated")