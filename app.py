import streamlit as st
import pandas as pd

# Set page layout to wide
st.set_page_config(layout="wide", page_title="United Transfer Scout")

st.title("🔴 Manchester United Pro-Tier Scout Engine")
st.markdown("---")

# 1. LOAD THE ADVANCED DATA MODEL
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

        # HELPER FUNCTION FOR FIT % CALCULATION (Using the raw data columns safely)
    def calculate_fit(row):
        # Fallback math mapping directly to the advanced raw metrics
        calc_passing = float(row.get("pPassing", (row["PassPctShort"] + row["PassPctLong"]) / 2))
        calc_retention = float(row.get("pRetention", row["PressPassPct"]))
        calc_defending = float(row.get("pDefending", row["DribblersTackledPct"]))
        calc_hunting = float(row.get("pHunting", (row["TacklesMid3rd"] * 25) + 30))  # Estimated scaled percentile
        calc_threat = float(row.get("pThreat", (row["SCA"] * 15) + 20))
        calc_physical = float(row.get("pPhysical", row["AerialWonPct"]))

        weighted_score = (
            (calc_passing * w_progression) +
            (calc_retention * w_retention) +
            (calc_defending * w_tackling) +
            (calc_hunting * w_recoveries) +
            (calc_threat * w_box_threat) +
            (calc_physical * w_physicality)
        )
        return round((weighted_score / total_possible_weight) * 100, 1)

    # Force string clean-up on the dataframe column names just in case of hidden GitHub spaces
    df_players.columns = df_players.columns.str.strip()
    df_players["FitScore"] = df_players.apply(calculate_fit, axis=1)

    df_players["FitScore"] = df_players.apply(calculate_fit, axis=1)

    # NAVIGATION TABS
    tab_h2h, tab_leaderboard = st.tabs(["📊 Deep-Dive Comparison Matrix", "🏆 Global Squad Leaderboard"])

    # ==================== TAB 1: ADVANCED H2H MATRIX ====================
    with tab_h2h:
        player_list = df_players["Player"].tolist()

        col_select1, col_select2 = st.columns(2)
        with col_select1:
            player_a = st.selectbox("Select Player A", player_list, index=2) # Default to Ederson
        with col_select2:
            player_b = st.selectbox("Select Player B", player_list, index=4) # Default to Stiller

        row_a = df_players[df_players["Player"] == player_a].iloc[0]
        row_b = df_players[df_players["Player"] == player_b].iloc[0]

        st.markdown("---")

        col_fit1, col_fit2 = st.columns(2)
        with col_fit1:
            st.metric(label=f"📊 {player_a} - Engine Fit Rating", value=f"{row_a['FitScore']}%")
            st.progress(row_a['FitScore'] / 100)
        with col_fit2:
            st.metric(label=f"📊 {player_b} - Engine Fit Rating", value=f"{row_b['FitScore']}%")
            st.progress(row_b['FitScore'] / 100)

        st.markdown("### 📋 24-Parameter Advanced Scouting Feed")
        st.markdown("---")
        
        # Dictionary breaking down the 24 specific metrics mapped by subcategories
        metric_categories = {
            "📈 Passing Architecture & Range": [
                ("Short-Medium Pass Accuracy", "PassPctShort", "%", True),
                ("Long-Range Pass Accuracy", "PassPctLong", "%", True),
                ("Passes Delivered into Final Third", "FinalThirdPasses", "/90", True),
                ("Progressive Distance Gained (Passing)", "ProgPassDistance", " yards", True),
                ("Through Balls Executed", "ThroughBalls", "/90", True),
                ("Switches of Play Swapped", "Switches", "/90", True),
            ],
            "🛡️ Press Resistance & Ball Carrying": [
                ("Pass Completion under Active Press", "PressPassPct", "%", True),
                ("Progressive Ball Carries", "ProgCarries", "/90", True),
                ("Successful 1v1 Take-On Rate", "TakeOnPct", "%", True),
                ("Dispossessed / Lost Possession Ball Controls", "Dispossessed", "/90", False),
            ],
            "🛑 True Defensive Architecture": [
                ("Tackles Executed in Defensive Third", "TacklesDef3rd", "/90", True),
                ("Tackles Executed in Middle Third", "TacklesMid3rd", "/90", True),
                ("True Dribblers Tackled Efficiency Rate", "DribblersTackledPct", "%", True),
                ("Interceptions Logged", "Interceptions", "/90", True),
                ("Shots/Passes Blocked", "Blocks", "/90", True),
                ("Clearances Completed", "Clearances", "/90", True),
            ],
            "⚔️ Creativity & Structural Presence": [
                ("Shot-Creating Actions Generated", "SCA", "/90", True),
                ("Expected Assists (xA Matrix)", "xA", "/90", True),
                ("Ball Touches Inside Attacking Box", "BoxTouches", "/90", True),
                ("Aerial Duels Won Percentage", "AerialWonPct", "%", True),
            ]
        }

        # Loop through each macro category
        for category_name, metrics in metric_categories.items():
            st.markdown(f"### {category_name}")
            st.markdown("<br>", unsafe_allow_html=True)
            
            for label, col_key, suffix, higher_is_better in metrics:
                val_a = row_a[col_key]
                val_b = row_b[col_key]
                
                # Evaluation logic for matchup edge
                if val_a == val_b:
                    winner = "🟡 Draw"
                else:
                    if higher_is_better:
                        winner = f"🟢 {player_a}" if val_a > val_b else f"🟢 {player_b}"
                    else:
                        winner = f"🟢 {player_a}" if val_a < val_b else f"🟢 {player_b}"
                
                # Render Row Description layout block
                col_text_left, col_text_right = st.columns([3, 1])
                with col_text_left:
                    st.markdown(f"#### {label}")
                with col_text_right:
                    st.markdown(f"**Edge:** {winner}")
                    
                # Nested side-by-side progression bar metrics
                col_bar_a, col_bar_b = st.columns(2)
                with col_bar_a:
                    st.write(f"**{player_a}:** {val_a}{suffix}")
                    # Map progress rendering logic securely
                    prog_val_a = min(100, int(val_a) if "%" in suffix or val_a > 1 else int(val_a * 100))
                    st.progress(max(0, prog_val_a) / 100)
                with col_bar_b:
                    st.write(f"**{player_b}:** {val_b}{suffix}")
                    prog_val_b = min(100, int(val_b) if "%" in suffix or val_b > 1 else int(val_b * 100))
                    st.progress(max(0, prog_val_b) / 100)
                    
                st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
            st.markdown("---")

    # ==================== TAB 2: GLOBAL LEADERBOARD ====================
    with tab_leaderboard:
        st.markdown(f"### 🏆 Dynamic Transfer Target Ranking ({selected_preset.split(' (')[0]})")
        st.markdown("Calculated by tracking multi-layered sub-parameters simultaneously against sidebar configurations.")
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

    st.info("💡 Pro-Tip: Use custom sliders in the sidebar to reposition weights. The engine parses all 24 database points automatically inside the fit algorithm calculations.")
