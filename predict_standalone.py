import pandas as pd
import numpy as np

# 1. Load the dataset
df = pd.read_csv('ipl_all_teams_antigravity.csv')
df.fillna(0, inplace=True)

def calc_raw(row):
    sr = min(row['strike_rate'], 200)
    batting = (0.6 * sr) + (0.4 * row['average'])
    
    if row['wickets'] == 0 and row['economy'] == 0.0:
        bowling = 0
    else:
        bowling = (row['wickets'] * 5) + (10 - row['economy'])
    
    exp = row['recent_form'] * 0.8
    
    # Role adjustments
    role = row['role'].lower()
    if 'batsman' in role or 'finisher' in role:
        batting *= 1.2
    elif 'bowler' in role:
        bowling *= 1.2
    elif 'allrounder' in role:
        batting *= 1.1
        bowling *= 1.1

    grav = (0.35 * batting) + (0.30 * bowling) + (0.25 * row['recent_form']) + (0.10 * exp)
    
    # Pressure penalty
    if row['recent_form'] < 60:
        grav -= 10
        
    return grav

df['gravity'] = df.apply(calc_raw, axis=1)

team1 = df[df['team'] == 'RCB'].nlargest(11, 'gravity')
team2 = df[df['team'] == 'CSK'].nlargest(11, 'gravity')

t1_score = team1['gravity'].sum()
t2_score = team2['gravity'].sum()

# Toss advantage 3% to Team 1
t1_score *= 1.03

total = t1_score + t2_score
p1 = (t1_score / total) * 100
p2 = (t2_score / total) * 100

combined = pd.concat([team1, team2])
top_3 = combined.nlargest(3, 'gravity')[['player_name', 'team', 'gravity']]
xf = combined[combined['recent_form'] > 85].nlargest(1, 'gravity')[['player_name', 'team', 'gravity']]
risk = combined.nsmallest(1, 'recent_form')[['player_name', 'team', 'recent_form']]

print(f"RCB_PROB:{p1:.2f}%")
print(f"CSK_PROB:{p2:.2f}%")
print(f"RCB_SCORE:{t1_score:.2f}")
print(f"CSK_SCORE:{t2_score:.2f}")

print("TOP_3:")
for _, r in top_3.iterrows():
    print(f"- {r['player_name']} ({r['team']}): {r['gravity']:.1f}")
    
print("XFACTOR:")
if not xf.empty:
    print(f"- {xf.iloc[0]['player_name']} ({xf.iloc[0]['team']}): {xf.iloc[0]['gravity']:.1f}")

print("RISK:")
if not risk.empty:
    print(f"- {risk.iloc[0]['player_name']} ({risk.iloc[0]['team']}) Form: {risk.iloc[0]['recent_form']}")
