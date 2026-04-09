import streamlit as st
import pandas as pd
import os
from engine.utils import validate_and_preprocess
from engine.calculator import process_match
from assets.plots import generate_player_contribution_chart, generate_radar_chart, generate_momentum_curve

# --- Web UI Config ---
st.set_page_config(page_title="Anti-Gravity IPL 2026", layout="wide", page_icon="🔋")

# Fictional Sci-Fi CSS Injection
st.markdown("""
<style>
    .stApp {
        background-color: #030509;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Pulsing headers */
    h1, h2, h3 {
        color: #00d2ff !important;
        text-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(4, 7, 13, 0.95) !important;
        border-right: 1px solid #00d2ff33;
        box-shadow: 5px 0 15px rgba(0, 210, 255, 0.05);
    }
    [data-testid="stMetricValue"] {
        color: #ff3366 !important;
        text-shadow: 0 0 12px rgba(255, 51, 102, 0.6);
        font-family: 'Courier New', Courier, monospace;
    }
    [data-testid="stMetricLabel"] {
        color: #8b9bb4 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    /* Neon Terminal Buttons */
    .stButton>button {
        border: 1px solid #00d2ff !important;
        background: rgba(0, 210, 255, 0.05) !important;
        color: #00d2ff !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.1) inset;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: bold;
        border-radius: 2px;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.6) inset, 0 0 20px rgba(0,210,255,0.4);
        color: #ffffff !important;
        text-shadow: 0 0 10px #fff;
    }
    /* Glassmorphism Alerts */
    .stAlert {
        background: rgba(5, 8, 15, 0.8) !important;
        border: 1px solid rgba(0, 210, 255, 0.2);
        color: #00d2ff;
        border-left: 4px solid #00d2ff;
    }
    .stSelectbox label, .stRadio label {
        color: #8b9bb4 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    hr {
        border-color: rgba(0, 210, 255, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔋 IPL '26 NEON ANTI-GRAVITY ENGINE")
st.markdown("Select two real IPL teams. The system automatically loads their 2026 active rosters and runs an Advanced Predictive Gravity Simulation.")

TEAM_MAP = {
    "Royal Challengers Bengaluru (RCB)": "data/rcb_2026.csv",
    "Chennai Super Kings (CSK)": "data/csk_2026.csv",
    "Mumbai Indians (MI)": "data/mi_2026.csv",
    "Gujarat Titans (GT)": "data/gt_2026.csv",
    "Rajasthan Royals (RR)": "data/rr_2026.csv",
    "Kolkata Knight Riders (KKR)": "data/kkr_2026.csv",
    "Sunrisers Hyderabad (SRH)": "data/srh_2026.csv",
    "Delhi Capitals (DC)": "data/dc_2026.csv",
    "Lucknow Super Giants (LSG)": "data/lsg_2026.csv",
    "Punjab Kings (PBKS)": "data/pbks_2026.csv"
}

st.sidebar.header("🌍 Match Context")
venue = st.sidebar.selectbox("Select Venue", ["Wankhede Stadium (Mumbai)", "M. Chinnaswamy (Bengaluru)", "Eden Gardens (Kolkata)", "Chepauk (Chennai)", "Narendra Modi Stadium (Ahmedabad)"])
pitch = st.sidebar.selectbox("Pitch Condition", ["Batting-Friendly", "Spin-Friendly", "Green Top", "Dustbowl"])

st.sidebar.markdown("---")
st.sidebar.info("🧠 **Advanced Logic Activated**:\n1. Dynamic Role Weighting\n2. Clutch Score Boosts\n3. Extreme Pressure Penalties")

# Dropdown Selection
col1, col2 = st.columns(2)
with col1:
    team1_name = st.selectbox("Select Team 1", list(TEAM_MAP.keys()), index=0)
with col2:
    team2_name = st.selectbox("Select Team 2", list(TEAM_MAP.keys()), index=1)

if team1_name == team2_name:
    st.warning("Please select two different teams to simulate the matchup.")
else:
    if st.button("🚀 Run Anti-Gravity Simulation", type="primary", use_container_width=True):
        if not os.path.exists(TEAM_MAP[team1_name]):
            st.error("Data arrays not found! Please run the dataset generator script first.")
        else:
            with st.spinner(f"Loading {team1_name} and {team2_name} matrices..."):
                try:
                    df_a = pd.read_csv(TEAM_MAP[team1_name])
                    df_b = pd.read_csv(TEAM_MAP[team2_name])
                    
                    df_a = validate_and_preprocess(df_a)
                    df_b = validate_and_preprocess(df_b)
                    
                    prob_a, prob_b, metrics_a, metrics_b, df_a_scored, df_b_scored = process_match(df_a, df_b, venue, pitch)
                    
                    # Store display names into dataframes for plots
                    t_a_code = team1_name.split(' ')[-1].replace('(','').replace(')','')
                    t_b_code = team2_name.split(' ')[-1].replace('(','').replace(')','')
                    df_a_scored['team'] = t_a_code
                    df_b_scored['team'] = t_b_code
                    
                    st.divider()
                    
                    st.header("⚡ Predictive Outcome Matrix")
                    
                    res1, res2 = st.columns(2)
                    res1.metric(label=f"{team1_name}", value=f"{prob_a:.1f}% Win Prob", delta="Advantage" if prob_a > prob_b else "-")
                    res2.metric(label=f"{team2_name}", value=f"{prob_b:.1f}% Win Prob", delta="Advantage" if prob_b > prob_a else "-")
                    
                    st.divider()
                    st.subheader("📊 Advanced Telemetry Visualizations")
                    
                    plot1, plot2 = st.columns(2)
                    with plot1:
                        st.plotly_chart(generate_radar_chart(metrics_a, metrics_b, t_a_code, t_b_code), use_container_width=True)
                    with plot2:
                        st.plotly_chart(generate_player_contribution_chart(df_a_scored, df_b_scored), use_container_width=True)
                        
                    st.plotly_chart(generate_momentum_curve(prob_a, prob_b, t_a_code, t_b_code), use_container_width=True)
                    
                    # AI Highlight Matrix
                    st.divider()
                    st.header("🧠 Engine Data Highlights")
                    col_high1, col_high2, col_high3 = st.columns(3)
                    
                    with col_high1:
                        st.subheader("⭐ Top Core Gravity")
                        st.caption("Maximum structural benefit to team.")
                        top_combined = pd.concat([df_a_scored, df_b_scored]).nlargest(4, 'gravity_score')
                        for _, row in top_combined.iterrows():
                            st.success(f"**{row['player_name']}** ({row['team']}) — Score: {row['gravity_score']:.1f}")
                            
                    with col_high2:
                        st.subheader("🔥 Target X-Factors")
                        st.caption("Clutch trigger overrides activated.")
                        clutch = pd.concat([df_a_scored, df_b_scored])
                        clutch = clutch[clutch['status'] == 'CLUTCH']
                        if not clutch.empty:
                            for _, row in clutch.nlargest(4, 'gravity_score').iterrows():
                                st.warning(f"**{row['player_name']}** ({row['team']})")
                        else:
                            st.write("No clutch players found.")
                            
                    with col_high3:
                        st.subheader("⚠️ Pressure Risks")
                        st.caption("Anti-Gravity drags due to missing form.")
                        risk = pd.concat([df_a_scored, df_b_scored])
                        risk = risk[risk['status'] == 'RISK']
                        if not risk.empty:
                            for _, row in risk.nsmallest(4, 'gravity_score').iterrows():
                                st.error(f"**{row['player_name']}** ({row['team']})")
                        else:
                            st.write("No clear risk players identified.")

                    # Full Rosters
                    st.divider()
                    st.header("📋 Playing XI Rosters")
                    roster_col1, roster_col2 = st.columns(2)
                    
                    def display_roster(df, team_title):
                        st.subheader(team_title)
                        batsmen = df[df['role'] == 'batsman']['player_name'].tolist()
                        allrounders = df[df['role'] == 'allrounder']['player_name'].tolist()
                        bowlers = df[df['role'] == 'bowler']['player_name'].tolist()
                        if batsmen: st.markdown(f"🏏 **Batsmen:** {', '.join(batsmen)}")
                        if allrounders: st.markdown(f"⚔️ **Allrounders:** {', '.join(allrounders)}")
                        if bowlers: st.markdown(f"🎯 **Bowlers:** {', '.join(bowlers)}")

                    with roster_col1:
                        display_roster(df_a_scored, team1_name)
                    with roster_col2:
                        display_roster(df_b_scored, team2_name)

                except Exception as e:
                    st.error(f"Error Processing Data: {str(e)}")
