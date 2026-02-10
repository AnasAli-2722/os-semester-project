import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from algorithms.cpu import CPUScheduler, Process
from algorithms.memory import MemoryManager

# --- Page Config ---
st.set_page_config(page_title="OS Simulator", page_icon="💻", layout="wide")

# --- Custom CSS: Professional Design System ---
st.markdown("""
<style>
    /* ===== Google Font ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }

    /* ===== Base Theme ===== */
    .stApp {
        background: #0b0f19;
    }
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(ellipse at 20% 50%, rgba(79, 172, 254, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(0, 242, 96, 0.04) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 80%, rgba(124, 58, 237, 0.04) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(79, 172, 254, 0.25); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(79, 172, 254, 0.4); }

    /* ===== Main Header ===== */
    .main-header {
        font-size: 2.4rem;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #00f260 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        padding: 8px 0 4px 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 0.85rem;
        margin-bottom: 8px;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* ===== Section Headers ===== */
    .sub-header {
        font-size: 1.45rem;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        font-weight: 800;
        letter-spacing: -0.3px;
    }

    /* ===== Cards ===== */
    .card {
        background: rgba(22, 27, 45, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 22px 24px;
        border-radius: 16px;
        border: 1px solid rgba(79, 172, 254, 0.08);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.03);
        margin-bottom: 14px;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: linear-gradient(180deg, #4facfe, #00f2fe);
        border-radius: 3px 0 0 3px;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .card:hover {
        border-color: rgba(79, 172, 254, 0.18);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.05);
        transform: translateY(-1px);
    }
    .card:hover::before { opacity: 1; }
    .card-title {
        color: #8bb8f0;
        font-weight: 700;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 0.2px;
        text-transform: uppercase;
        font-size: 0.78rem;
    }
    .card-body {
        color: #6b7a99;
        font-size: 0.82rem;
        font-weight: 400;
        line-height: 1.4;
    }

    /* ===== Metric Cards ===== */
    .metric-card {
        background: rgba(22, 27, 45, 0.8);
        backdrop-filter: blur(16px);
        padding: 22px 16px;
        border-radius: 16px;
        border: 1px solid rgba(0, 242, 96, 0.1);
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 20%; right: 20%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00f260, transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(0, 242, 96, 0.2);
        box-shadow: 0 8px 32px rgba(0, 242, 96, 0.08);
    }
    .metric-card:hover::after { opacity: 1; }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f260, #0575e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .metric-label {
        color: #5a6a85;
        font-size: 0.72rem;
        margin-top: 6px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ===== Process Chips ===== */
    .process-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(79, 172, 254, 0.08);
        border: 1px solid rgba(79, 172, 254, 0.2);
        color: #7bb8f0;
        padding: 3px 12px;
        border-radius: 20px;
        font-weight: 600;
        margin: 3px;
        font-size: 0.78rem;
        transition: all 0.2s ease;
        letter-spacing: 0.3px;
    }
    .process-chip:hover {
        background: rgba(79, 172, 254, 0.15);
        border-color: rgba(79, 172, 254, 0.35);
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1220 0%, #111827 100%) !important;
        border-right: 1px solid rgba(79, 172, 254, 0.06) !important;
        min-width: 280px !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #94a3b8;
    }
    /* Keep sidebar content visible and properly contained */
    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        height: 100vh;
        overflow-y: auto;
        overflow-x: hidden;
    }
    /* Sidebar collapse button styling */
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="collapsedControl"] {
        color: #4facfe !important;
    }
    [data-testid="collapsedControl"] {
        background: rgba(13, 18, 32, 0.95) !important;
        border: 1px solid rgba(79, 172, 254, 0.15) !important;
        border-radius: 0 12px 12px 0 !important;
        color: #4facfe !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    [data-testid="collapsedControl"]:hover {
        background: rgba(79, 172, 254, 0.1) !important;
        border-color: rgba(79, 172, 254, 0.3) !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #4facfe !important;
        color: #4facfe !important;
    }

    /* Sidebar radio buttons */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 4px !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label {
        background: rgba(79, 172, 254, 0.04) !important;
        border: 1px solid rgba(79, 172, 254, 0.08) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin: 0 !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(79, 172, 254, 0.1) !important;
        border-color: rgba(79, 172, 254, 0.2) !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
    [data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.12), rgba(0, 242, 254, 0.08)) !important;
        border-color: rgba(79, 172, 254, 0.3) !important;
        box-shadow: 0 0 20px rgba(79, 172, 254, 0.08) !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label p {
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }

    /* Sidebar branding */
    .sidebar-logo {
        text-align: center;
        padding: 20px 16px 16px 16px;
    }
    .sidebar-logo-icon { font-size: 2.2rem; margin-bottom: 6px; display: block; }
    .sidebar-logo-text {
        font-size: 1.1rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.3px;
    }
    .sidebar-logo-sub {
        font-size: 0.65rem;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        margin-top: 2px;
        font-weight: 500;
    }
    .sidebar-nav-label {
        font-size: 0.65rem;
        color: #3d4f6b;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
        padding: 0 4px;
        margin-bottom: 6px;
    }
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(79, 172, 254, 0.12), transparent);
        margin: 16px 0;
        border: none;
    }

    /* Sidebar spacer — pushes footer to bottom */
    .sidebar-spacer {
        flex-grow: 1;
        min-height: 40px;
    }

    /* Sidebar footer — in-flow, not fixed */
    .sidebar-footer {
        text-align: center;
        padding: 20px 16px;
        margin-top: auto;
        border-top: 1px solid rgba(79, 172, 254, 0.06);
        background: rgba(11, 15, 25, 0.5);
    }
    .sidebar-footer-text {
        font-size: 0.7rem;
        color: #3d4f6b;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    .sidebar-footer-names {
        font-size: 0.78rem;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin-top: 2px;
        letter-spacing: 0.3px;
    }
    .sidebar-footer-dot {
        display: inline-block;
        width: 4px; height: 4px;
        background: #4facfe;
        border-radius: 50%;
        margin: 0 6px;
        vertical-align: middle;
        opacity: 0.5;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        border-radius: 25px !important;
        padding: 6px 24px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        border: 1px solid rgba(79, 172, 254, 0.2) !important;
        background: rgba(79, 172, 254, 0.06) !important;
        color: #8bb8f0 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        width: auto !important;
        min-height: 38px !important;
        height: 38px !important;
        line-height: 1 !important;
    }
    .stButton > button:hover {
        border-color: rgba(79, 172, 254, 0.4) !important;
        background: rgba(79, 172, 254, 0.12) !important;
        color: #a8d0fa !important;
        box-shadow: 0 4px 20px rgba(79, 172, 254, 0.12) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        border: none !important;
        color: #0b0f19 !important;
        font-weight: 700 !important;
        padding: 8px 32px !important;
        box-shadow: 0 4px 20px rgba(79, 172, 254, 0.25) !important;
        min-height: 42px !important;
        height: 42px !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 30px rgba(79, 172, 254, 0.35) !important;
        transform: translateY(-2px) !important;
        color: #0b0f19 !important;
        filter: brightness(1.1) !important;
    }

    /* Form submit button */
    .stFormSubmitButton > button {
        border-radius: 25px !important;
        padding: 6px 24px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        border: 1px solid rgba(0, 242, 96, 0.25) !important;
        background: rgba(0, 242, 96, 0.08) !important;
        color: #5cd888 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        min-height: 38px !important;
        height: 38px !important;
    }
    .stFormSubmitButton > button:hover {
        background: rgba(0, 242, 96, 0.15) !important;
        border-color: rgba(0, 242, 96, 0.4) !important;
        box-shadow: 0 4px 20px rgba(0, 242, 96, 0.12) !important;
        transform: translateY(-1px) !important;
    }

    /* ===== INPUT FIELDS ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(15, 20, 35, 0.8) !important;
        border: 1px solid rgba(79, 172, 254, 0.1) !important;
        border-radius: 12px !important;
        color: #c8d6e5 !important;
        font-size: 0.88rem !important;
        padding: 8px 14px !important;
        transition: all 0.25s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: rgba(79, 172, 254, 0.35) !important;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.08) !important;
        outline: none !important;
    }
    .stSelectbox > div > div {
        background: rgba(15, 20, 35, 0.8) !important;
        border: 1px solid rgba(79, 172, 254, 0.1) !important;
        border-radius: 12px !important;
        transition: all 0.25s ease !important;
    }
    .stSelectbox > div > div:hover {
        border-color: rgba(79, 172, 254, 0.25) !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(15, 20, 35, 0.5) !important;
        border: 1px dashed rgba(79, 172, 254, 0.15) !important;
        border-radius: 14px !important;
        padding: 12px !important;
        transition: all 0.25s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(79, 172, 254, 0.3) !important;
        background: rgba(79, 172, 254, 0.03) !important;
    }
    [data-testid="stFileUploader"] button {
        border-radius: 20px !important;
    }

    /* Labels */
    .stTextInput > label, .stNumberInput > label, .stSelectbox > label {
        color: #6b7a99 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
    }

    /* ===== FORM CONTAINER ===== */
    [data-testid="stForm"] {
        background: rgba(15, 20, 35, 0.4) !important;
        border: 1px solid rgba(79, 172, 254, 0.06) !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }

    /* ===== DIVIDERS ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(79, 172, 254, 0.1), transparent) !important;
        margin: 16px 0 !important;
    }

    /* ===== DATAFRAME ===== */
    .stDataFrame {
        border-radius: 14px !important;
        overflow: hidden;
        border: 1px solid rgba(79, 172, 254, 0.08) !important;
    }

    /* ===== ALERTS ===== */
    .stAlert {
        border-radius: 14px !important;
        border: none !important;
        backdrop-filter: blur(10px) !important;
    }

    /* ===== EMPTY STATE ===== */
    .empty-state {
        text-align: center;
        padding: 50px 20px;
    }
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 14px;
        opacity: 0.6;
    }
    .empty-state-text {
        color: #4a5568;
        font-size: 0.9rem;
        line-height: 1.6;
        font-weight: 400;
    }

    /* ===== PLOTLY CHART ===== */
    .stPlotlyChart { border-radius: 14px; overflow: hidden; }

    /* ===== SPACING ===== */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] {
        background: transparent !important;
        backdrop-filter: none !important;
    }
    /* Hide only the Streamlit decoration / toolbar, keep sidebar controls */
    header[data-testid="stHeader"] .stAppDeployButton,
    header[data-testid="stHeader"] [data-testid="stStatusWidget"],
    header[data-testid="stHeader"] [data-testid="stToolbar"] {
        visibility: hidden !important;
    }

    /* Ensure sidebar is always rendered */
    [data-testid="stSidebar"] {
        display: flex !important;
        z-index: 999 !important;
    }
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        z-index: 1000 !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Helper ---
def metric_card(label, value):
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    ''', unsafe_allow_html=True)


# --- Header ---
st.markdown('<div class="main-header">💻 Operating System Simulator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Semester Project &nbsp;•&nbsp; BSCS &nbsp;•&nbsp; UET Taxila</div>', unsafe_allow_html=True)
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    # Logo / Branding
    st.markdown('''
    <div class="sidebar-logo">
        <span class="sidebar-logo-icon">💻</span>
        <div class="sidebar-logo-text">OS Simulator</div>
        <div class="sidebar-logo-sub">Interactive Learning Tool</div>
    </div>
    <div class="sidebar-divider"></div>
    ''', unsafe_allow_html=True)

    # Navigation
    st.markdown('<div class="sidebar-nav-label">📌 Modules</div>', unsafe_allow_html=True)
    module = st.radio(
        "Navigation",
        ["⚙️  CPU Scheduling", "🧠  Memory Management"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Context-aware info card
    if "CPU" in module:
        st.markdown('''
        <div class="card" style="padding: 16px 18px;">
            <div class="card-title">💡 Quick Info</div>
            <div class="card-body" style="font-size: 0.78rem; line-height: 1.7;">
                <b style="color:#8bb8f0;">FCFS</b> — First Come, First Served<br>
                <b style="color:#8bb8f0;">SJF</b> — Shortest Job First<br>
                <b style="color:#8bb8f0;">RR</b> — Round Robin with time quantum
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="card" style="padding: 16px 18px;">
            <div class="card-title">💡 Quick Info</div>
            <div class="card-body" style="font-size: 0.78rem; line-height: 1.7;">
                <b style="color:#8bb8f0;">FIFO</b> — First In, First Out<br>
                <b style="color:#8bb8f0;">LRU</b> — Least Recently Used
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # Spacer to push footer down
    st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

    # Footer
    st.markdown('''
    <div class="sidebar-footer">
        <div class="sidebar-footer-text">Made with ❤️ by</div>
        <div class="sidebar-footer-names">
            Mahnoor <span class="sidebar-footer-dot"></span> Anas
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Clean module name
module_clean = module.strip()

# ================= CPU MODULE =================
if "CPU" in module_clean:
    st.markdown('<div class="sub-header">⚙️ CPU Scheduling Simulator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        # Configuration Card
        st.markdown('''<div class="card">
            <div class="card-title">🔧 Configuration</div>
            <div class="card-body">Choose algorithm and set parameters</div>
        </div>''', unsafe_allow_html=True)

        algo = st.selectbox("Algorithm", ["FCFS", "SJF (Non-Preemptive)", "Round Robin"],
                            help="Select a CPU scheduling algorithm to simulate")

        quantum = 2
        if algo == "Round Robin":
            quantum = st.number_input("Time Quantum", min_value=1, value=2,
                                      help="Time slice for Round Robin scheduling")

        st.markdown("---")

        # Process Input Card
        st.markdown('''<div class="card">
            <div class="card-title">➕ Add Processes</div>
            <div class="card-body">Add manually or upload a CSV file</div>
        </div>''', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload CSV (pid, arrival, burst)", type="csv",
                                         help="CSV must have columns: pid, arrival, burst")

        # Session state init
        if 'processes' not in st.session_state:
            st.session_state.processes = []

        # CSV upload handler
        if uploaded_file is not None:
            try:
                df_csv = pd.read_csv(uploaded_file)
                df_csv.columns = [c.strip().lower() for c in df_csv.columns]
                count_before = len(st.session_state.processes)
                for _, row in df_csv.iterrows():
                    st.session_state.processes.append({
                        "pid": int(row['pid']),
                        "arrival": int(row['arrival']),
                        "burst": int(row['burst'])
                    })
                added = len(st.session_state.processes) - count_before
                st.success(f"✅ Loaded {added} processes from CSV!")
            except Exception as e:
                st.error(f"⚠️ CSV Error: {e}. Expected columns: pid, arrival, burst")

        with st.form("add_process"):
            c1, c2, c3 = st.columns(3)
            pid = c1.number_input("PID", min_value=1, value=len(st.session_state.processes) + 1)
            arr = c2.number_input("Arrival", min_value=0, value=0)
            burst = c3.number_input("Burst", min_value=1, value=5)
            submitted = st.form_submit_button("➕  Add Process")

            if submitted:
                st.session_state.processes.append({"pid": pid, "arrival": arr, "burst": burst})
                st.success(f"✅ Added P{pid}")

        if st.button("🗑️  Clear All"):
            st.session_state.processes = []
            st.rerun()

    with col2:
        # Process Queue Card
        st.markdown('''<div class="card">
            <div class="card-title">📋 Process Queue</div>
            <div class="card-body">Processes ready for scheduling</div>
        </div>''', unsafe_allow_html=True)

        if st.session_state.processes:
            df_input = pd.DataFrame(st.session_state.processes)
            df_input.columns = ["PID", "Arrival Time", "Burst Time"]
            st.dataframe(df_input, width='stretch', hide_index=True)

            # Process chips
            chips_html = " ".join([f'<span class="process-chip">P{p["pid"]}</span>' for p in st.session_state.processes])
            st.markdown(f'<div style="margin: 8px 0 16px 0;">{chips_html}</div>', unsafe_allow_html=True)

            # Centered Run button
            btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
            with btn_col2:
                run_clicked = st.button("🚀  Run Simulation", type="primary")

            if run_clicked:
                with st.spinner("Running simulation..."):
                    process_objects = [Process(p['pid'], p['arrival'], p['burst']) for p in st.session_state.processes]
                    scheduler = CPUScheduler()

                    if algo == "FCFS":
                        result_procs, timeline = scheduler.fcfs(process_objects)
                    elif algo == "SJF (Non-Preemptive)":
                        result_procs, timeline = scheduler.sjf_non_preemptive(process_objects)
                    else:
                        result_procs, timeline = scheduler.round_robin(process_objects, quantum)

                # ---- Gantt Chart ----
                st.markdown("---")
                st.markdown('''<div class="card">
                    <div class="card-title">📊 Gantt Chart</div>
                    <div class="card-body">Visual timeline of process execution</div>
                </div>''', unsafe_allow_html=True)

                if timeline:
                    df_timeline = pd.DataFrame(timeline)
                    colors = px.colors.qualitative.Vivid
                    color_map = {}
                    color_idx = 0
                    legend_shown = set()
                    fig = go.Figure()

                    for _, row in df_timeline.iterrows():
                        task = row['Task']
                        if task not in color_map:
                            color_map[task] = colors[color_idx % len(colors)]
                            color_idx += 1

                        show_legend = task not in legend_shown
                        legend_shown.add(task)

                        fig.add_trace(go.Bar(
                            x=[row['Finish'] - row['Start']],
                            y=["Timeline"],
                            base=row['Start'],
                            orientation='h',
                            name=task,
                            marker_color=color_map[task],
                            marker_line=dict(width=1, color='rgba(0,0,0,0.3)'),
                            text=f"{task} ({row['Start']}-{row['Finish']})",
                            textposition='inside',
                            textfont=dict(color='white', size=11, family='Inter'),
                            showlegend=show_legend,
                            hovertemplate=f"<b>{task}</b><br>Start: {row['Start']}ms<br>End: {row['Finish']}ms<extra></extra>"
                        ))

                    fig.update_layout(
                        barmode='stack',
                        xaxis_title="Time (ms)",
                        yaxis_visible=False,
                        height=160,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#8899aa', family='Inter'),
                        margin=dict(l=0, r=0, t=10, b=40),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=11)),
                        xaxis=dict(gridcolor='rgba(79,172,254,0.06)', zerolinecolor='rgba(79,172,254,0.06)')
                    )
                    st.plotly_chart(fig, width='stretch')

                # ---- Performance Metrics ----
                st.markdown('''<div class="card">
                    <div class="card-title">📈 Performance Metrics</div>
                    <div class="card-body">Detailed scheduling results per process</div>
                </div>''', unsafe_allow_html=True)

                res_data = []
                avg_wait = 0
                avg_turn = 0
                for p in result_procs:
                    res_data.append({
                        "PID": f"P{p.pid}",
                        "Arrival": p.arrival_time,
                        "Burst": p.burst_time,
                        "Completion": p.completion_time,
                        "Turnaround": p.turnaround_time,
                        "Waiting": p.waiting_time
                    })
                    avg_wait += p.waiting_time
                    avg_turn += p.turnaround_time

                if result_procs:
                    avg_wait /= len(result_procs)
                    avg_turn /= len(result_procs)

                st.dataframe(pd.DataFrame(res_data), width='stretch', hide_index=True)

                st.markdown("<br>", unsafe_allow_html=True)
                k1, k2, k3 = st.columns(3)
                with k1:
                    metric_card("Avg Waiting Time", f"{avg_wait:.2f} ms")
                with k2:
                    metric_card("Avg Turnaround Time", f"{avg_turn:.2f} ms")
                with k3:
                    max_ct = max(p.completion_time for p in result_procs) if result_procs else 1
                    throughput = len(result_procs) / max_ct
                    metric_card("Throughput", f"{throughput:.2f} p/ms")
        else:
            st.markdown('''
            <div class="card">
                <div class="empty-state">
                    <div class="empty-state-icon">📭</div>
                    <div class="empty-state-text">No processes added yet.<br>Use the panel on the left to add processes manually or upload a CSV file.</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)


# ================= MEMORY MODULE =================
elif "Memory" in module_clean:
    st.markdown('<div class="sub-header">🧠 Memory Management Simulator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        # Configuration Card
        st.markdown('''<div class="card">
            <div class="card-title">🔧 Configuration</div>
            <div class="card-body">Set up the page replacement algorithm</div>
        </div>''', unsafe_allow_html=True)

        algo_mem = st.selectbox("Algorithm", ["FIFO", "LRU"],
                                help="Select a page replacement algorithm")
        frames = st.number_input("Number of Frames", min_value=1, max_value=10, value=3,
                                 help="Number of memory frames available")
        ref_string = st.text_input("Reference String (comma separated)",
                                   "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1",
                                   help="Enter page numbers separated by commas")

        # Page preview chips
        try:
            preview_pages = [int(x.strip()) for x in ref_string.split(',')]
            chips = " ".join([f'<span class="process-chip">{p}</span>' for p in preview_pages])
            st.markdown(f'''<div class="card" style="padding: 16px 20px;">
                <div class="card-title">📄 Page Sequence — {len(preview_pages)} pages</div>
                <div style="margin-top: 8px;">{chips}</div>
            </div>''', unsafe_allow_html=True)
        except Exception:
            pass

    with col2:
        # Centered Simulate button
        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col2:
            sim_clicked = st.button("🚀  Simulate Memory", type="primary")

        if sim_clicked:
            try:
                pages = [int(x.strip()) for x in ref_string.split(',')]
                manager = MemoryManager()

                with st.spinner("Simulating..."):
                    if algo_mem == "FIFO":
                        faults, snapshots = manager.fifo(pages, frames)
                    else:
                        faults, snapshots = manager.lru(pages, frames)

                hits = len(pages) - faults

                # Summary Metrics
                st.markdown(f'''<div class="card">
                    <div class="card-title">📊 Results Summary</div>
                    <div class="card-body">Performance of the {algo_mem} algorithm</div>
                </div>''', unsafe_allow_html=True)

                m1, m2, m3 = st.columns(3)
                with m1:
                    metric_card("Page Faults", f"{faults}")
                with m2:
                    metric_card("Page Hits", f"{hits}")
                with m3:
                    hit_ratio = hits / len(pages) * 100 if pages else 0
                    metric_card("Hit Ratio", f"{hit_ratio:.1f}%")

                st.markdown("<br>", unsafe_allow_html=True)

                # Pie Chart
                st.markdown('''<div class="card">
                    <div class="card-title">📉 Fault vs Hit Analysis</div>
                </div>''', unsafe_allow_html=True)

                fig_pie = px.pie(
                    values=[faults, hits],
                    names=["Faults", "Hits"],
                    color_discrete_sequence=["#ff4b4b", "#00f260"],
                    hole=0.5
                )
                fig_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#8899aa', family='Inter'),
                    height=280,
                    margin=dict(l=20, r=20, t=10, b=10),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=dict(size=12))
                )
                fig_pie.update_traces(textinfo='percent+label', textfont_size=13, textfont_family='Inter')
                st.plotly_chart(fig_pie, width='stretch')

                # Step-by-Step Table
                st.markdown('''<div class="card">
                    <div class="card-title">🔄 Step-by-Step Execution</div>
                    <div class="card-body">Memory frame state at each page request</div>
                </div>''', unsafe_allow_html=True)

                display_data = []
                for i, step in enumerate(snapshots):
                    frames_display = step['Frames'] + ['-'] * (frames - len(step['Frames']))
                    row = {"Step": i + 1, "Page": step['Page'], "Status": step['Status']}
                    for j, f in enumerate(frames_display):
                        row[f"Frame {j + 1}"] = f
                    display_data.append(row)

                df_mem = pd.DataFrame(display_data)

                def color_status(val):
                    if val == 'Miss':
                        return 'color: #ff4b4b; font-weight: bold; background-color: rgba(255,75,75,0.08)'
                    elif val == 'Hit':
                        return 'color: #00f260; font-weight: bold; background-color: rgba(0,242,96,0.08)'
                    return ''

                st.dataframe(
                    df_mem.style.map(color_status, subset=['Status']),
                    width='stretch',
                    hide_index=True
                )

            except ValueError:
                st.error("⚠️ Please enter a valid comma-separated list of integers for the reference string.")
        else:
            st.markdown('''
            <div class="card">
                <div class="empty-state">
                    <div class="empty-state-icon">🧠</div>
                    <div class="empty-state-text">Configure parameters on the left and click<br><b>Simulate Memory</b> to begin.</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
