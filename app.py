import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="IoT Network Command", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- AUTHENTICATION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# --- ADVANCED CUSTOM CSS (Animated Background, Massive Title & Protected Icons) ---
st.markdown("""
    <style>
    /* 1. Import Custom Tech Font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&display=swap');

    /* 2. Force Rajdhani globally but protect icons */
    html, body, [class*="css"], [class*="st-"], span, div, p, h1, h2, h3, h4, h5, h6, a, button, input {
        font-family: 'Rajdhani', sans-serif !important;
    }

    /* CRITICAL FIX: Protect Streamlit's built-in icons from being overwritten */
    .material-icons, 
    .material-symbols-rounded, 
    [data-testid="stIconMaterial"], 
    [data-testid="stIconMaterial"] * {
        font-family: 'Material Symbols Rounded', sans-serif !important;
    }

    /* 3. Custom App Background (Animated Neural Breathing Effect) */
    .stApp {
        background: linear-gradient(-45deg, #070A14, #0B162C, #0F1D35, #050814);
        background-size: 400% 400%;
        animation: breathingNetwork 25s ease infinite;
        background-attachment: fixed;
    }

    @keyframes breathingNetwork {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .block-container { padding-top: 3.5rem; padding-bottom: 2rem; max-width: 95%; }
    
    /* 4. Glowing Massive Gradient Title */
    .main-title {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 5.5rem !important; 
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00D2FF, #00FFAA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        margin-bottom: 0rem;
        text-shadow: 0px 0px 20px rgba(0, 255, 170, 0.2);
        line-height: 1.2 !important;
        padding-top: 10px;
    }
    
    /* Interactive Metric Cards */
    div[data-testid="metric-container"] {
        background: rgba(15, 20, 30, 0.5);
        border: 1px solid rgba(0, 255, 170, 0.2);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 255, 170, 0.8);
        box-shadow: 0 12px 40px 0 rgba(0, 255, 170, 0.3);
    }
    
    /* Sleek Progress Bars */
    .stProgress > div > div > div > div { 
        background-image: linear-gradient(90deg, #00D2FF 0%, #00FFAA 100%);
        border-radius: 10px;
    }
    
    /* Customize Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.3rem;
        font-weight: 600;
        height: 50px;
        background-color: transparent;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    /* Login Box Styling */
    .login-box {
        background: rgba(15, 20, 30, 0.8);
        padding: 40px;
        border-radius: 15px;
        border: 1px solid rgba(0, 255, 170, 0.4);
        max-width: 500px;
        margin: auto;
        margin-top: 10vh;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- AI PREDICTION ENGINE ---
@st.cache_resource
def train_network_ai():
    np.random.seed(42)
    hours = np.random.randint(0, 24, 1000)
    demand = np.where((hours >= 18) & (hours <= 23), 
                      np.random.normal(350, 50, 1000),  
                      np.random.normal(120, 30, 1000))  
    historical_data = pd.DataFrame({'hour': hours, 'demand': demand})
    model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
    model.fit(historical_data[['hour']], historical_data['demand'])
    return model

ai_model = train_network_ai()

# ==========================================
# LOGIN SCREEN
# ==========================================
if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<p class="main-title" style="font-size: 2.5rem; text-align: center;">SYSTEM LOGIN</p>', unsafe_allow_html=True)
    st.write("---")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login as Admin", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.rerun()
            else:
                st.error("Invalid Admin Credentials")
    with col2:
        if st.button("Continue as Guest", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.role = "Guest"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MAIN APPLICATION
# ==========================================
else:
    is_guest = st.session_state.role == "Guest"

    # --- HEADER AREA ---
    st.markdown('<p class="main-title">NEURAL IOT CONTROLLER</p>', unsafe_allow_html=True)
    st.markdown("Enterprise-grade network optimization utilizing Weighted Fair Queuing (WFQ) and Machine Learning.")
    st.write("") 

    # --- SIDEBAR: GLOBAL CONTROLS ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2885/2885412.png", width=60)
        st.header("Control Panel")
        
        if is_guest:
            st.warning("👤 Logged in as: **GUEST**")
        else:
            st.success("🛡️ Logged in as: **ADMIN**")
        
        with st.expander("📡 Network Parameters", expanded=True):
            total_bw = st.slider("Total ISP Bandwidth (Mbps)", 10, 500, 150, 10, disabled=is_guest)
        
        with st.expander("🔌 Active Endpoints", expanded=True):
            laptop_on = st.toggle("💻 Work Laptop", value=True, disabled=is_guest)
            gaming_on = st.toggle("🎮 Gaming Node", value=False, disabled=is_guest)
            tv_on = st.toggle("📺 Media Stream", value=True, disabled=is_guest)
            iot_on = st.toggle("🌡️ IoT Sub-network", value=True, disabled=is_guest)

        with st.expander("🧠 AI Auto-Scaling", expanded=False):
            ai_mode = st.toggle("Enable Neural Forecast", value=False, disabled=is_guest)
            if ai_mode:
                simulated_hour = st.slider("Simulate Network Time", 0, 23, 19, format="%d:00", disabled=is_guest)
                
        st.write("---")
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # --- CORE LOGIC ---
    devices = [
        {"name": "Work Laptop", "category": "Critical", "weight": 10, "active": laptop_on},
        {"name": "Gaming Node", "category": "High", "weight": 8, "active": gaming_on},
        {"name": "Media Stream", "category": "High", "weight": 5, "active": tv_on},
        {"name": "IoT Sub-network", "category": "Low", "weight": 1, "active": iot_on},
    ]

    if ai_mode:
        predicted_demand = int(ai_model.predict([[simulated_hour]])[0])
        if predicted_demand > total_bw:
            for d in devices:
                if d['category'] == 'Low': d['active'] = False

    active_devices = [d for d in devices if d['active']]
    total_weight = sum(d['weight'] for d in active_devices)

    for d in devices:
        if d['active'] and total_weight > 0:
            d['allocated'] = round((d['weight'] / total_weight) * total_bw, 2)
            d['progress_ratio'] = min(d['allocated'] / total_bw, 1.0)
        else:
            d['allocated'] = 0.0; d['progress_ratio'] = 0.0

    df = pd.DataFrame(devices)
    active_df = df[df['active']] 

    # --- APP NAVIGATION (TABS) ---
    tab1, tab2, tab3 = st.tabs(["📊 Live Dashboard", "🧠 AI Analytics", "⚙️ System Logs"])

    # === TAB 1: LIVE DASHBOARD ===
    with tab1:
        st.markdown("### Real-Time Network Telemetry")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Total Uplink Capacity", value=f"{total_bw} Mbps")
        col2.metric(label="Active Endpoints", value=len(active_df))
        
        if not active_df.empty and 'Work Laptop' in active_df['name'].values:
            laptop_speed = active_df.loc[active_df['name'] == 'Work Laptop', 'allocated'].iloc[0]
            status = "Secure" if laptop_speed > 20 else "Compromised"
            col3.metric(label="Critical Node Health", value=status, delta="Optimal" if status == "Secure" else "-Warning")
        else:
            col3.metric(label="Critical Node Health", value="Standby")

        st.write("---")
        
        left_col, right_col = st.columns([2, 1.2])
        with left_col:
            st.markdown("#### Topology Distribution")
            if not active_df.empty:
                # NEW SLEEK AREA CHART
                fig = px.area(
                    active_df, 
                    x='name', 
                    y='allocated', 
                    color='category',
                    line_shape='spline',
                    color_discrete_map={'Critical': '#FF3366', 'High': '#00D2FF', 'Low': '#00FFAA'}
                )
                
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", 
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis_title="", 
                    yaxis_title="Bandwidth (Mbps)",
                    font=dict(color="#FAFAFA", family="Rajdhani"), 
                    showlegend=True, 
                    margin=dict(l=0, r=0, t=30, b=0),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                fig.update_traces(fill='tonexty', marker=dict(size=8))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("System Idle. Enable endpoints in the control panel.")

        with right_col:
            st.markdown("#### Port Utilization")
            if not active_df.empty:
                for index, row in active_df.iterrows():
                    st.write(f"**{row['name']}**")
                    st.progress(float(row['progress_ratio']), text=f"Allocated: {row['allocated']} Mbps")

    # === TAB 2: AI ANALYTICS ===
    with tab2:
        st.markdown("### Predictive Machine Learning Engine")
        if not ai_mode:
            st.warning("⚠️ Neural Forecast is currently disabled.")
        else:
            if predicted_demand > total_bw:
                st.error(f"🔴 **CRITICAL ALERT:** Projected demand at {simulated_hour}:00 is **{predicted_demand} Mbps**.")
            else:
                st.success(f"🟢 **SYSTEM STABLE:** Projected demand at {simulated_hour}:00 is **{predicted_demand} Mbps**.")
            
            curve_hours = np.arange(0, 24)
            curve_predictions = ai_model.predict(curve_hours.reshape(-1, 1))
            curve_df = pd.DataFrame({'Hour': curve_hours, 'Predicted Mbps': curve_predictions})
            
            fig2 = px.line(curve_df, x='Hour', y='Predicted Mbps')
            fig2.add_hline(y=total_bw, line_dash="dash", line_color="red", annotation_text="Limit")
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                font=dict(color="#FAFAFA", family="Rajdhani")
            )
            st.plotly_chart(fig2, use_container_width=True)

    # === TAB 3: SYSTEM LOGS ===
    with tab3:
        st.markdown("### Raw Router Telemetry")
        st.dataframe(df[['name', 'category', 'weight', 'active', 'allocated']], use_container_width=True, hide_index=True)
