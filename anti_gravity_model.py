import sys
import threading
import webbrowser
import time

try:
    from flask import Flask
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    print("Missing libraries. Please run: pip install flask plotly pandas")
    sys.exit()

app = Flask(__name__)

@app.route('/')
def dashboard():
    print("[SYSTEM] Processing vectors for localhost display...")
    
    # Context Data
    csk_base = 865
    rcb_base = 852
    csk_adjusted = 855  # Reduced by dew
    rcb_adjusted = 907  # Boosted by dew chasing
    
    # 1. Setup Dashboard Framework
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "domain"}, {"type": "bar"}],
               [{"type": "polar", "colspan": 2}, None]],
        subplot_titles=("Win Probability Forecast (%)", "Team Gravity Index Shift", "Core Player Force Matrix")
    )

    # 2. Add Win Probability Donut
    fig.add_trace(
        go.Pie(
            labels=['Chennai Super Kings (Team A)', ' Royal Challengers Bengaluru (Team B)'],
            values=[48.5, 51.5],
            hole=0.6,
            marker_colors=['#fbbc05', '#ea4335'],
            textinfo='label+percent',
            textfont_size=14
        ),
        row=1, col=1
    )

    # 3. Add Gravity Shift Bar Chart
    fig.add_trace(
        go.Bar(
            name="Base Gravity",
            x=['Team A (CSK)', 'Team B (RCB)'],
            y=[csk_base, rcb_base],
            marker_color='rgba(139, 155, 180, 0.4)',
            marker_line_width=1,
            marker_line_color='rgba(139, 155, 180, 1)'
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(
            name="Adjusted Gravity (+Dew)",
            x=['Team A (CSK)', 'Team B (RCB)'],
            y=[csk_adjusted, rcb_adjusted],
            marker_color=['#fbbc05', '#ea4335'],
            text=[csk_adjusted, rcb_adjusted],
            textposition='auto'
        ),
        row=1, col=2
    )

    # 4. Add Matchup Radar Chart
    categories = ['Form (Recent)', 'Strike/Economy', 'Pressure Handling', 'Anti-Gravity Res.', 'Venue Mod']
    fig.add_trace(
        go.Scatterpolar(
            name='R. Gaikwad (CSK)',
            r=[88, 85, 80, 70, 75],
            theta=categories,
            fill='toself',
            fillcolor='rgba(251, 188, 5, 0.2)',
            line=dict(color='#fbbc05')
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatterpolar(
            name='V. Kohli (RCB)',
            r=[95, 80, 95, 90, 100],
            theta=categories,
            fill='toself',
            fillcolor='rgba(234, 67, 53, 0.2)',
            line=dict(color='#ea4335')
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatterpolar(
            name='S. Dube (CSK)',
            r=[92, 98, 85, 88, 80],
            theta=categories,
            fill='toself',
            fillcolor='rgba(0, 210, 255, 0.2)',
            line=dict(color='#00d2ff', dash='dash')
        ),
        row=2, col=1
    )
    
    # Format The Look
    fig.update_layout(
        title_text="🏏 ANTI-GRAVITY ENGINE v2.4 (LOCALHOST INSTANCE)",
        title_font=dict(size=24, color="#00d2ff", family="sans-serif"),
        title_x=0.5,
        template="plotly_dark",
        paper_bgcolor='#0b0f19',
        plot_bgcolor='#0b0f19',
        barmode='group',
        showlegend=True,
        height=850,
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 100], gridcolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")
        )
    )
    fig.update_yaxes(range=[800, 950], row=1, col=2)

    # Return as an HTML string directly served to the browser
    return fig.to_html(include_plotlyjs='cdn', full_html=True)

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    print("[SYSTEM] Starting Local Web Engine...")
    threading.Thread(target=open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
