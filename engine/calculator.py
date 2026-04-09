import numpy as np
import pandas as pd

def compute_player_gravity(df):
    """Calculates Anti-Gravity score using advanced role-based weighting & clutch indexing."""
    scores = []
    modifiers = []
    
    for _, row in df.iterrows():
        role = row['role'].lower()
        form = row['recent_form']
        
        # 1. Base Role Logic
        if role == 'batsman':
            norm_sr = min(row['strike_rate'] / 250.0, 1)
            norm_avg = min(row['average'] / 60.0, 1)
            base_score = (norm_sr * 0.6 + norm_avg * 0.4) * 100
        elif role == 'bowler':
            norm_w = min(row['wickets'] / 25.0, 1)
            safe_econ = row['economy'] if row['economy'] > 5 else 5
            norm_econ = max(0, (12 - safe_econ) / 7.0) # Lower is better
            base_score = (norm_w * 0.5 + norm_econ * 0.5) * 100
        else: # allrounder
            norm_sr = min(row['strike_rate'] / 200.0, 1)
            norm_w = min(row['wickets'] / 20.0, 1)
            safe_econ = row['economy'] if row['economy'] > 5 else 10
            norm_econ = max(0, (12 - safe_econ) / 7.0)
            base_score = (norm_sr * 0.4 + norm_w * 0.3 + norm_econ * 0.3) * 100
            
        # Natively blend base with recent form
        gravity = (base_score * 0.6) + (form * 0.4)
        
        # 2. Advanced Modifiers (Pressure and Clutch)
        pressure_mod = 0
        if form < 60:
            pressure_mod -= 15 # Penalize form < 60
        if form > 85:
            pressure_mod += 15 # Boost form > 85
            
        gravity += pressure_mod
        gravity = max(0, min(gravity, 120)) # Cap extreme ends
        
        scores.append(gravity)
        modifiers.append("CLUTCH" if form > 85 else ("RISK" if form < 60 else "NEUTRAL"))
        
    df['gravity_score'] = scores
    df['status'] = modifiers
    return df

def calculate_team_gravity(df):
    """Computes aggregate Team Gravity Index and returns sub-metrics"""
    batsman = df[df['role'] == 'batsman']
    bowlers = df[df['role'] == 'bowler']
    
    batting_score = np.mean(batsman['gravity_score']) if not batsman.empty else 50
    bowling_score = np.mean(bowlers['gravity_score']) if not bowlers.empty else 50
    form_score = np.mean(df['recent_form'])
    
    team_index = (0.4 * batting_score) + (0.4 * bowling_score) + (0.2 * form_score)
    
    return {
        'team_index': team_index,
        'batting_score': batting_score,
        'bowling_score': bowling_score,
        'form_score': form_score
    }

def process_match(df_a, df_b, venue, pitch):
    """Calculates final win probability relying strictly on core player dynamics."""
    df_a = compute_player_gravity(df_a)
    df_b = compute_player_gravity(df_b)
    
    score_a = calculate_team_gravity(df_a)
    score_b = calculate_team_gravity(df_b)
    
    idx_a = score_a['team_index']
    idx_b = score_b['team_index']
    
    mod_a, mod_b = 0, 0
    
    # Venue Boost (Chennai rewards good spin/economy)
    if "Chennai" in venue:
        econ_a = np.mean(df_a[df_a['role'] == 'bowler']['economy'])
        econ_b = np.mean(df_b[df_b['role'] == 'bowler']['economy'])
        if econ_a < econ_b: mod_a += 4.0
        else: mod_b += 4.0
        
    final_a = max(0, idx_a + mod_a)
    final_b = max(0, idx_b + mod_b)
    
    total = final_a + final_b
    prob_a = (final_a / total) * 100 if total > 0 else 50
    prob_b = (final_b / total) * 100 if total > 0 else 50
    
    return prob_a, prob_b, score_a, score_b, df_a, df_b
