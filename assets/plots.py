import plotly.graph_objects as go
import numpy as np

BG_COLOR = '#0b0f19'
TEAM_A_COLOR = '#00d2ff'
TEAM_B_COLOR = '#ff3366'

def generate_player_contribution_chart(df_a, df_b):
    team_a_name = df_a['team'].iloc[0] if not df_a.empty else 'Team 1'
    team_b_name = df_b['team'].iloc[0] if not df_b.empty else 'Team 2'
    
    top_a = df_a.nlargest(5, 'gravity_score')
    top_b = df_b.nlargest(5, 'gravity_score')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=top_a['player_name'], y=top_a['gravity_score'], name=team_a_name, marker_color=TEAM_A_COLOR))
    fig.add_trace(go.Bar(x=top_b['player_name'], y=top_b['gravity_score'], name=team_b_name, marker_color=TEAM_B_COLOR))
    
    fig.update_layout(title="Top Gravity Contributors (Base Matrix)", barmode='group', template='plotly_dark', paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR, hovermode="x unified")
    return fig

def generate_radar_chart(metrics_a, metrics_b, t_a, t_b):
    categories = ['Batting Score', 'Bowling Score', 'Form Score', 'Overall Index']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[metrics_a['batting_score'], metrics_a['bowling_score'], metrics_a['form_score'], metrics_a['team_index']], theta=categories, fill='toself', name=t_a, line=dict(color=TEAM_A_COLOR)))
    fig.add_trace(go.Scatterpolar(r=[metrics_b['batting_score'], metrics_b['bowling_score'], metrics_b['form_score'], metrics_b['team_index']], theta=categories, fill='toself', name=t_b, line=dict(color=TEAM_B_COLOR)))
    fig.update_layout(title="Team Force Comparison", polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)"), angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")), showlegend=True, template='plotly_dark', paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR)
    return fig
    
def generate_momentum_curve(prob_a, prob_b, t_a, t_b):
    x = np.linspace(0, 20, 20)
    noise_a = np.random.normal(0, 5, 10).tolist() + np.random.normal(0, 1, 10).tolist()
    y_a = np.linspace(50, prob_a, 20) + noise_a
    y_a = np.clip(y_a, 0, 100)
    y_b = 100 - y_a
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_a, mode='lines+markers', name=t_a + ' Prob (%)', line=dict(color=TEAM_A_COLOR, width=3)))
    fig.add_trace(go.Scatter(x=x, y=y_b, mode='lines+markers', name=t_b + ' Prob (%)', line=dict(color=TEAM_B_COLOR, width=3)))
    fig.update_layout(title="Simulated Live Match Momentum (20 Overs)", xaxis_title="Overs", yaxis_title="Win Probability (%)", template='plotly_dark', paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR, yaxis=dict(range=[0,100]))
    return fig
