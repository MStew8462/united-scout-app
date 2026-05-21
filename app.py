import streamlit as st
import pandas as pd

# Set page layout to wide
st.set_page_config(layout="wide", page_title="United Transfer Scout")

st.title("🔴 Manchester United Transfer Scout Dashboard")
st.markdown("---")

# 1. LOAD THE LOCAL CSV DATA
@st.cache_data
def load_local_data():
    try:
        df = pd.read_csv("midfielders.csv")
        return df
    except FileNotFoundError:
        st.error("⚠️ Could not find 'midfielders.csv'. Make sure it's in the same folder as this app.py script!")
        return None

df_players = load_local_data()

if df_players is not None:
    
    # 2. TACTICAL PRESETS CONFIGURATION
    st.sidebar.header("⚙️ Scouting Configuration")
    
    presets = {
        "Custom (Manual Sliders)": [5, 5, 5, 5, 5, 5],
        "Controller (The Press-Breaker)": [9, 10, 5, 5, 2, 4],
        "Destroyer (The Defensive Anchor)": [3, 6, 10, 10, 1, 9],
        "Box-to-Box (The Dynamic Engine)": [5, 6, 7, 7, 7, 7]
    }
    
    selected_preset = st.sidebar.selectbox("Select Tactical Preset:", list(presets.keys()))
    preset_values = presets[selected_preset]

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Tactical Weights")

    w_progression = st.sidebar.slider("Progressive Passing", 1, 10, preset_values[0])
    w_retention = st.sidebar.slider("Ball Retention", 1, 10, preset_values[1])
    w_tackling = st.sidebar.slider("Defensive Intensity", 1, 10, preset_values[2])
    w_recoveries = st.sidebar.slider("Ball Hunting", 1, 10, preset_values[3])
    w_box_threat = st.sidebar.slider("Box-to-Box Threat", 1, 10, preset_values[4])
    w_physicality = st.sidebar.slider("Physical Dominance", 1, 10, preset_values[5])

    total_possible_weight = (w_progression + w_retention + w_tackling + w_recoveries + w_box_threat + w_physicality) * 100

    # HELPER FUNCTION FOR FIT % CALCULATION
    def calculate_fit(row):
        weighted_score = (
            (row["Progression"] * w_progression) +
            (row["Retention"] * w_retention) +
            (row["Tackling"] * w_tackling) +
            (row["Recoveries"] * w_recoveries) +
            (row["BoxThreat"] * w_box_threat) +
            (row["Physicality"] * w_physicality)
        )
        return round((weighted_score / total_possible_weight) * 100, 1)

    # Calculate scores dynamically for all players upfront
    df_players["FitScore"] = df_players.apply(calculate_fit, axis=1)

    # CREATE NAVIGATION TABS
    tab_h2h, tab_leaderboard = st.tabs(["📊 Player Head-to-Head", "🏆 Global Squad Leaderboard"])

    # ==================== TAB 1: HEAD-TO-HEAD LAYOUT ====================
    with tab_h2h:
        player_list = df_players["Player"].tolist()

        col_select1, col_select2 = st.columns(2)
        with col_select1:
            player_a = st.selectbox("Select Player A", player_list, index=0)
        with col_select2:
            player_b = st.selectbox("Select Player B", player_list, index=10)

        row_a = df_players[df_players["Player"] == player_a].iloc[0]
        row_b = df_players[df_players["Player"] == player_b].iloc[0]

        st.markdown("---")

        col_fit1, col_fit2 = st.columns(2)
        with col_fit1:
            st.metric(label=f"📊 {player_a} - Role Match Score", value=f"{row_a['FitScore']}%")
            st.progress(row_a['FitScore'] / 100)
        with col_fit2:
            st.metric(label=f"📊 {player_b} - Role Match Score", value=f"{row_b['FitScore']}%")
            st.progress(row_b['FitScore'] / 100)

        st.markdown("### 📋 Tactical Breakdown & Visual Matrix")
        st.markdown("---")
        
        metrics_mapping = [
            ("Passing Accuracy", "Retention", "PassAccuracyRaw"),
            ("Line-Breaking Passes", "Progression", "ProgPassesRaw"),
            ("Tackles & Interceptions", "Tackling", "TacklesRaw"),
            ("Ball Recoveries", "Recoveries", "RecoveriesRaw"),
            ("Goal/Assist Threat", "BoxThreat", "GARaw"),
            ("Aerial Dominance", "Physicality", "AerialsRaw")
        ]

        # All code loops through a unified full-width system now
        for label, score_col, raw_col in metrics_mapping:
            score_a = row_a[score_col]
            score_b = row_b[score_col]
            raw_a = row_a[raw_col]
            raw_b = row_b[raw_col]
            
            if score_a > score_b:
                winner = f"🟢 {player_a}"
            elif score_b > score_a:
                winner = f"🟢 {player_b}"
            else:
                winner = "🟡 Draw"
                
            # Line 1: Header Text and Matchup Winner Row
            col_text_left, col_text_right = st.columns([3, 1])
            with col_text_left:
                st.markdown(f"#### {label}")
            with col_text_right:
                st.markdown(f"**Winner:** {winner}")
                
            # Line 2: Side-by-Side Values and Progress Bars nested right beneath
            col_bar_a, col_bar_b = st.columns(2)
            with col_bar_a:
                st.write(f"**{player_a}:** {raw_a} *(p{score_a})*")
                st.progress(int(score_a) / 100)
            with col_bar_b:
                st.write(f"**{player_b}:** {raw_b} *(p{score_b})*")
                st.progress(int(score_b) / 100)
                
            st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)
            st.markdown("---")

    # ==================== TAB 2: CLEAN LEADERBOARD LAYOUT ====================
    with tab_leaderboard:
        st.markdown(f"### 🏆 Dynamic Transfer Target Ranking ({selected_preset.split(' (')[0]})")
        st.markdown("The list below sorts automatically from highest to lowest based on your sidebar settings.")
        st.markdown("---")
        
        df_leaderboard = df_players[["Player", "FitScore"]].sort_values(by="FitScore", ascending=False).reset_index(drop=True)
        
        for index, row in df_leaderboard.iterrows():
            col_rank, col_name, col_score = st.columns([1, 4, 2])
            with col_rank:
                st.markdown(f"### **#{index + 1}**")
            with col_name:
                st.markdown(f"### {row['Player']}")
            with col_score:
                st.markdown(f"### 🟢 **{row['FitScore']}%** Match")
            st.markdown("<hr style='margin:0.2rem 0px; opacity:0.3;'>", unsafe_allow_html=True)

    st.info("💡 Pro-Tip: Toggle tabs above to switch between side-by-side numerical scouting matrixes and full squad-fit leaderboards.")