import streamlit as st
import pandas as pd

# Set page layout to wide
st.set_page_config(layout="wide", page_title="United Transfer Scout")

st.title("🔴 Manchester United Pro-Tier Scout Engine")
st.markdown("---")

# HARDCODED BACKUP DATASET (Prevents any CSV syncing/pasting errors)
BACKUP_DATA = [
    {"Player": "Sandro Tonali", "PassPctShort": 89.4, "PassPctLong": 68.2, "FinalThirdPasses": 5.2, "ProgPassDistance": 240.5, "ThroughBalls": 0.18, "Switches": 1.4, "PressPassPct": 82.4, "ProgCarries": 2.1, "TakeOnPct": 55.0, "Dispossessed": 1.1, "TacklesDef3rd": 1.1, "TacklesMid3rd": 1.4, "DribblersTackledPct": 48.5, "Interceptions": 1.2, "Blocks": 1.2, "Clearances": 0.8, "SCA": 3.2, "xA": 0.14, "BoxTouches": 1.1, "AerialWonPct": 52.0, "pPassing": 73, "pRetention": 84, "pDefending": 45, "pHunting": 62, "pThreat": 22, "pPhysical": 50},
    {"Player": "Adam Wharton (Crystal Palace)", "PassPctShort": 87.5, "PassPctLong": 58.2, "FinalThirdPasses": 6.4, "ProgPassDistance": 295.1, "ThroughBalls": 0.22, "Switches": 1.8, "PressPassPct": 84.1, "ProgCarries": 1.9, "TakeOnPct": 52.3, "Dispossessed": 0.9, "TacklesDef3rd": 1.9, "TacklesMid3rd": 1.8, "DribblersTackledPct": 51.4, "Interceptions": 1.4, "Blocks": 1.6, "Clearances": 1.2, "SCA": 3.4, "xA": 0.18, "BoxTouches": 1.2, "AerialWonPct": 46.5, "pPassing": 85, "pRetention": 84, "pDefending": 83, "pHunting": 93, "pThreat": 20, "pPhysical": 40},
    {"Player": "Éderson (Atalanta)", "PassPctShort": 89.2, "PassPctLong": 72.1, "FinalThirdPasses": 4.2, "ProgPassDistance": 210.5, "ThroughBalls": 0.08, "Switches": 1.1, "PressPassPct": 74.5, "ProgCarries": 2.3, "TakeOnPct": 55.2, "Dispossessed": 0.9, "TacklesDef3rd": 1.8, "TacklesMid3rd": 2.1, "DribblersTackledPct": 53.6, "Interceptions": 1.1, "Blocks": 1.5, "Clearances": 1.6, "SCA": 2.1, "xA": 0.07, "BoxTouches": 1.4, "AerialWonPct": 41.5, "pPassing": 62, "pRetention": 83, "pDefending": 86, "pHunting": 81, "pThreat": 48, "pPhysical": 68},
    {"Player": "Mateus Fernandes (West Ham)", "PassPctShort": 85.4, "PassPctLong": 52.1, "FinalThirdPasses": 4.8, "ProgPassDistance": 215.2, "ThroughBalls": 0.14, "Switches": 0.8, "PressPassPct": 80.5, "ProgCarries": 2.8, "TakeOnPct": 54.5, "Dispossessed": 1.4, "TacklesDef3rd": 1.2, "TacklesMid3rd": 1.5, "DribblersTackledPct": 45.2, "Interceptions": 0.9, "Blocks": 1.1, "Clearances": 1.3, "SCA": 2.9, "xA": 0.12, "BoxTouches": 1.6, "AerialWonPct": 36.5, "pPassing": 74, "pRetention": 80, "pDefending": 68, "pHunting": 66, "pThreat": 50, "pPhysical": 38},
    {"Player": "Angelo Stiller", "PassPctShort": 92.4, "PassPctLong": 78.9, "FinalThirdPasses": 6.8, "ProgPassDistance": 315.2, "ThroughBalls": 0.24, "Switches": 2.3, "PressPassPct": 88.1, "ProgCarries": 1.4, "TakeOnPct": 58.3, "Dispossessed": 0.5, "TacklesDef3rd": 0.8, "TacklesMid3rd": 1.4, "DribblersTackledPct": 58.1, "Interceptions": 1.8, "Blocks": 1.1, "Clearances": 1.4, "SCA": 3.8, "xA": 0.21, "BoxTouches": 1.7, "AerialWonPct": 46.5, "pPassing": 88, "pRetention": 93, "pDefending": 60, "pHunting": 78, "pThreat": 42, "pPhysical": 55},
    {"Player": "Kobbie Mainoo (Man Utd)", "PassPctShort": 91.2, "PassPctLong": 70.5, "FinalThirdPasses": 4.1, "ProgPassDistance": 195.4, "ThroughBalls": 0.11, "Switches": 0.6, "PressPassPct": 86.5, "ProgCarries": 2.9, "TakeOnPct": 62.1, "Dispossessed": 1.5, "TacklesDef3rd": 1.2, "TacklesMid3rd": 1.1, "DribblersTackledPct": 46.1, "Interceptions": 0.8, "Blocks": 1.3, "Clearances": 0.6, "SCA": 2.8, "xA": 0.10, "BoxTouches": 1.8, "AerialWonPct": 45.0, "pPassing": 65, "pRetention": 86, "pDefending": 55, "pHunting": 60, "pThreat": 40, "pPhysical": 48},
    {"Player": "Casemiro (Man Utd)", "PassPctShort": 82.1, "PassPctLong": 56.4, "FinalThirdPasses": 4.9, "ProgPassDistance": 235.1, "ThroughBalls": 0.15, "Switches": 2.1, "PressPassPct": 72.4, "ProgCarries": 0.8, "TakeOnPct": 40.0, "Dispossessed": 1.1, "TacklesDef3rd": 2.1, "TacklesMid3rd": 1.6, "DribblersTackledPct": 54.2, "Interceptions": 2.1, "Blocks": 1.9, "Clearances": 2.4, "SCA": 2.2, "xA": 0.11, "BoxTouches": 1.3, "AerialWonPct": 72.1, "pPassing": 40, "pRetention": 79, "pDefending": 85, "pHunting": 78, "pThreat": 35, "pPhysical": 78},
    {"Player": "Bruno Fernandes (Man Utd)", "PassPctShort": 76.4, "PassPctLong": 44.2, "FinalThirdPasses": 7.4, "ProgPassDistance": 345.8, "ThroughBalls": 0.42, "Switches": 3.1, "PressPassPct": 71.2, "ProgCarries": 2.6, "TakeOnPct": 50.0, "Dispossessed": 1.8, "TacklesDef3rd": 0.7, "TacklesMid3rd": 1.2, "DribblersTackledPct": 38.5, "Interceptions": 1.1, "Blocks": 0.9, "Clearances": 0.5, "SCA": 5.4, "xA": 0.32, "BoxTouches": 3.4, "AerialWonPct": 38.0, "pPassing": 96, "pRetention": 74, "pDefending": 40, "pHunting": 58, "pThreat": 88, "pPhysical": 35},
    {"Player": "Manuel Ugarte (Man Utd)", "PassPctShort": 92.1, "PassPctLong": 64.2, "FinalThirdPasses": 2.8, "ProgPassDistance": 142.1, "ThroughBalls": 0.02, "Switches": 0.4, "PressPassPct": 85.2, "ProgCarries": 0.9, "TakeOnPct": 45.0, "Dispossessed": 0.6, "TacklesDef3rd": 2.4, "TacklesMid3rd": 2.8, "DribblersTackledPct": 56.5, "Interceptions": 2.2, "Blocks": 1.8, "Clearances": 1.5, "SCA": 1.1, "xA": 0.03, "BoxTouches": 0.4, "AerialWonPct": 52.5, "pPassing": 32, "pRetention": 88, "pDefending": 94, "pHunting": 89, "pThreat": 10, "pPhysical": 55},
    {"Player": "Declan Rice (Arsenal)", "PassPctShort": 91.5, "PassPctLong": 74.2, "FinalThirdPasses": 5.8, "ProgPassDistance": 285.4, "ThroughBalls": 0.16, "Switches": 1.9, "PressPassPct": 86.2, "ProgCarries": 2.4, "TakeOnPct": 56.0, "Dispossessed": 0.7, "TacklesDef3rd": 1.4, "TacklesMid3rd": 1.8, "DribblersTackledPct": 53.1, "Interceptions": 1.7, "Blocks": 1.4, "Clearances": 1.6, "SCA": 3.5, "xA": 0.20, "BoxTouches": 2.1, "AerialWonPct": 61.2, "pPassing": 78, "pRetention": 87, "pDefending": 79, "pHunting": 82, "pThreat": 60, "pPhysical": 70},
    {"Player": "Elliot Anderson (Nottingham)", "PassPctShort": 84.2, "PassPctLong": 58.5, "FinalThirdPasses": 4.6, "ProgPassDistance": 220.2, "ThroughBalls": 0.12, "Switches": 1.1, "PressPassPct": 81.4, "ProgCarries": 3.1, "TakeOnPct": 59.2, "Dispossessed": 1.3, "TacklesDef3rd": 1.4, "TacklesMid3rd": 1.6, "DribblersTackledPct": 48.2, "Interceptions": 1.1, "Blocks": 1.3, "Clearances": 1.1, "SCA": 3.1, "xA": 0.15, "BoxTouches": 2.2, "AerialWonPct": 58.9, "pPassing": 71, "pRetention": 85, "pDefending": 72, "pHunting": 68, "pThreat": 55, "pPhysical": 82},
    {"Player": "Carlos Baleba (Brighton)", "PassPctShort": 88.5, "PassPctLong": 65.4, "FinalThirdPasses": 4.3, "ProgPassDistance": 212.4, "ThroughBalls": 0.06, "Switches": 0.9, "PressPassPct": 84.1, "ProgCarries": 2.7, "TakeOnPct": 61.4, "Dispossessed": 1.2, "TacklesDef3rd": 1.9, "TacklesMid3rd": 2.2, "DribblersTackledPct": 54.0, "Interceptions": 1.5, "Blocks": 1.6, "Clearances": 1.2, "SCA": 1.9, "xA": 0.06, "BoxTouches": 0.9, "AerialWonPct": 62.0, "pPassing": 58, "pRetention": 86, "pDefending": 88, "pHunting": 76, "pThreat": 25, "pPhysical": 72},
    {"Player": "Alex Scott (Bournemouth)", "PassPctShort": 83.1, "PassPctLong": 54.0, "FinalThirdPasses": 4.2, "ProgPassDistance": 198.5, "ThroughBalls": 0.15, "Switches": 0.7, "PressPassPct": 79.2, "ProgCarries": 2.3, "TakeOnPct": 53.1, "Dispossessed": 1.6, "TacklesDef3rd": 1.1, "TacklesMid3rd": 1.3, "DribblersTackledPct": 44.5, "Interceptions": 1.0, "Blocks": 1.2, "Clearances": 0.8, "SCA": 2.7, "xA": 0.14, "BoxTouches": 1.5, "AerialWonPct": 44.2, "pPassing": 68, "pRetention": 81, "pDefending": 64, "pHunting": 59, "pThreat": 42, "pPhysical": 46},
    {"Player": "Hayden Hackney (Middlesbrough)", "PassPctShort": 86.4, "PassPctLong": 69.1, "FinalThirdPasses": 5.9, "ProgPassDistance": 278.4, "ThroughBalls": 0.21, "Switches": 1.6, "PressPassPct": 83.0, "ProgCarries": 2.2, "TakeOnPct": 50.0, "Dispossessed": 1.1, "TacklesDef3rd": 1.0, "TacklesMid3rd": 1.2, "DribblersTackledPct": 46.2, "Interceptions": 1.3, "Blocks": 1.0, "Clearances": 0.7, "SCA": 3.0, "xA": 0.13, "BoxTouches": 1.0, "AerialWonPct": 42.0, "pPassing": 81, "pRetention": 85, "pDefending": 58, "pHunting": 70, "pThreat": 38, "pPhysical": 44},
    {"Player": "Aurélien Tchouaméni (Real Madrid)", "PassPctShort": 93.1, "PassPctLong": 82.4, "FinalThirdPasses": 6.2, "ProgPassDistance": 310.2, "ThroughBalls": 0.14, "Switches": 2.5, "PressPassPct": 89.5, "ProgCarries": 1.2, "TakeOnPct": 52.0, "Dispossessed": 0.4, "TacklesDef3rd": 1.6, "TacklesMid3rd": 2.1, "DribblersTackledPct": 62.4, "Interceptions": 2.3, "Blocks": 1.4, "Clearances": 2.1, "SCA": 2.0, "xA": 0.08, "BoxTouches": 0.8, "AerialWonPct": 76.5, "pPassing": 88, "pRetention": 92, "pDefending": 82, "pHunting": 85, "pThreat": 30, "pPhysical": 91}
]

# 1. LOAD DATA METHOD WITH FAILSAFE AUTOMATION
def load_data():
    try:
        df = pd.read_csv("midfielders.csv")
        df.columns = df.columns.str.strip()
        # Verify a key column exists, otherwise trigger backup fallback
        if "PassPctShort" in df.columns:
            return df
    except Exception:
        pass
    return pd.DataFrame(BACKUP_DATA)

df_players = load_data()

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
            (float(row["pPassing"]) * w_progression) +
            (float(row["pRetention"]) * w_retention) +
            (float(row["pDefending"]) * w_tackling) +
            (float(row["pHunting"]) * w_recoveries) +
            (float(row["pThreat"]) * w_box_threat) +
            (float(row["pPhysical"]) * w_physicality)
        )
        return round((weighted_score / total_possible_weight) * 100, 1)

    df_players["FitScore"] = df_players.apply(calculate_fit, axis=1)

    # CREATE NAVIGATION TABS
    tab_h2h, tab_leaderboard = st.tabs(["📊 Deep-Dive Comparison Matrix", "🏆 Global Squad Leaderboard"])

    # ==================== TAB 1: ADVANCED H2H MATRIX ====================
    with tab_h2h:
        player_list = df_players["Player"].tolist()

        col_select1, col_select2 = st.columns(2)
        with col_select1:
            player_a = st.selectbox("Select Player A", player_list, index=2) # Default Éderson
        with col_select2:
            player_b = st.selectbox("Select Player B", player_list, index=4) # Default Stiller

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
        
        metric_categories = {
            "📈 Passing Architecture & Range": [
                ("Short-Medium Pass Accuracy", "PassPctShort", "%", True),
                ("Long-Range Pass Accuracy", "PassPctLong", "%", True),
                ("Passes Delivered into Final Third", "FinalThirdPasses", "/90", True),
                ("Progressive Distance Gained (Passing)", "ProgPassDistance", " yards", True),
                ("Through Balls Executed", "ThroughBalls", "/90", True),
                ("Switches of Play", "Switches", "/90", True),
            ],
            "🛡️ Press Resistance & Ball Carrying": [
                ("Pass Completion under Active Press", "PressPassPct", "%", True),
                ("Progressive Ball Carries", "ProgCarries", "/90", True),
                ("Successful 1v1 Take-On Rate", "TakeOnPct", "%", True),
                ("Dispossessed / Lost Possession", "Dispossessed", "/90", False),
            ],
            "🛑 True Defensive Architecture": [
                ("Tackles in Defensive Third", "TacklesDef3rd", "/90", True),
                ("Tackles in Middle Third", "TacklesMid3rd", "/90", True),
                ("True Dribblers Tackled Efficiency Rate", "DribblersTackledPct", "%", True),
                ("Interceptions Logged", "Interceptions", "/90", True),
                ("Shots/Passes Blocked", "Blocks", "/90", True),
                ("Clearances Completed", "Clearances", "/90", True),
            ],
            "⚔️ Creativity & Structural Presence": [
                ("Shot-Creating Actions Generated", "SCA", "/90", True),
                ("Expected Assists (xA)", "xA", "/90", True),
                ("Ball Touches Inside Attacking Box", "BoxTouches", "/90", True),
                ("Aerial Duels Won Percentage", "AerialWonPct", "%", True),
            ]
        }

        for category_name, metrics in metric_categories.items():
            st.markdown(f"### {category_name}")
            st.markdown("<br>", unsafe_allow_html=True)
            
            for label, col_key, suffix, higher_is_better in metrics:
                val_a = row_a[col_key]
                val_b = row_b[col_key]
                
                if val_a == val_b:
                    winner = "🟡 Draw"
                else:
                    if higher_is_better:
                        winner = f"🟢 {player_a}" if val_a > val_b else f"🟢 {player_b}"
                    else:
                        winner = f"🟢 {player_a}" if val_a < val_b else f"🟢 {player_b}"
                
                col_text_left, col_text_right = st.columns([3, 1])
                with col_text_left:
                    st.markdown(f"#### {label}")
                with col_text_right:
                    st.markdown(f"**Edge:** {winner}")
                    
                col_bar_a, col_bar_b = st.columns(2)
                with col_bar_a:
                    st.write(f"**{player_a}:** {val_a}{suffix}")
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
