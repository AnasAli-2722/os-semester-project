import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from algorithms.cpu import CPUScheduler, Process
from algorithms.memory import MemoryManager

# --- Page Config ---
st.set_page_config(page_title="OS Simulator | Anas", page_icon="💻", layout="wide")

# --- Custom CSS for Beautiful Look ---
st.markdown("""
<style>
    /* === Base Theme === */
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1a2e 50%, #16213e 100%);
    }

    /* === Headers === */
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        padding: 10px 0;
        letter-spacing: 1px;
    }
    .sub-header {
        font-size: 1.6rem;
        background: linear-gradient(90deg, #00f260, #0575e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        font-weight: 700;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 20px;
    }

    /* === Cards === */
    .card {
        background: linear-gradient(145deg, #1e1e2f, #262740);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(79, 172, 254, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(79, 172, 254, 0.15);
    }
    .card-title {
        font-size: 1.1rem;
        color: #4facfe;
        font-weight: 600;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card-body {
        color: #ccc;
        font-size: 0.95rem;
    }

    /* === Metric Cards === */
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e, #222240);
        padding: 20px;
        border-radius: 14px;
        border: 1px solid rgba(0, 242, 96, 0.2);
        text-align: center;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f260, #0575e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        color: #aaa;
        font-size: 0.85rem;
        margin-top: 4px;
    }

    /* === Process Chips === */
    .process-chip {
        display: inline-block;
        background: linear-gradient(135deg, #4facfe22, #00f2fe22);
        border: 1px solid #4facfe44;
        color: #4facfe;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 600;
        margin: 3px;
        font-size: 0.85rem;
    }

    /* === Sidebar === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0e1117, #1a1a2e) !important;
        border-right: 1px solid rgba(79, 172, 254, 0.1);
    }

    /* === Empty State === */
    .empty-state {
        text-align: center;
        padding: 50px 20px;
        color: #666;
    }
    .empty-state-icon {
        font-size: 3.5rem;
        margin-bottom: 12px;
    }
    .empty-state-text {
        color: #888;
        font-size: 1rem;
    }

    /* === Dividers === */
    hr {
        border-color: rgba(79, 172, 254, 0.12) !important;
    }

    /* === Dataframe === */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* === Alert boxes === */
    .stAlert {
        border-radius: 12px !important;
    }

    /* === Status badges === */
    .badge-miss {
        color: #ff4b4b;
        font-weight: bold;
        background: rgba(255, 75, 75, 0.1);
        padding: 2px 10px;
        border-radius: 10px;
    }
    .badge-hit {
        color: #00f260;
        font-weight: bold;
        background: rgba(0, 242, 96, 0.1);
        padding: 2px 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# --- Helper Functions ---
def metric_card(label, value):
    """Renders a styled metric card."""
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

# --- Sidebar Navigation ---
st.sidebar.title("🧭 Navigation")
module = st.sidebar.radio("Select Module", ["CPU Scheduling", "Memory Management"])

# ================= CPU MODULE =================
if module == "CPU Scheduling":
    st.markdown('<div class="sub-header">⚙️ CPU Scheduling Simulator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        # --- Algorithm Configuration Card ---
        st.markdown('''<div class="card">
            <div class="card-title">🔧 Configuration</div>
            <div class="card-body">Choose an algorithm and set parameters.</div>
        </div>''', unsafe_allow_html=True)

        algo = st.selectbox("Algorithm", ["FCFS", "SJF (Non-Preemptive)", "Round Robin"])

        quantum = 2
        if algo == "Round Robin":
            quantum = st.number_input("⏱️ Time Quantum", min_value=1, value=2)

        st.markdown("---")

        # --- Process Input Card ---
        st.markdown('''<div class="card">
            <div class="card-title">➕ Add Processes</div>
            <div class="card-body">Add manually or upload a CSV file.</div>
        </div>''', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload CSV (pid, arrival, burst)", type="csv")

        # Initialize session state
        if 'processes' not in st.session_state:
            st.session_state.processes = []

        # Handle CSV upload
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
            submitted = st.form_submit_button("➕ Add Process", use_container_width=True)

            if submitted:
                st.session_state.processes.append({"pid": pid, "arrival": arr, "burst": burst})
                st.success(f"✅ Added P{pid}")

        if st.button("🗑️ Clear All Processes", use_container_width=True):
            st.session_state.processes = []
            st.rerun()

    with col2:
        # --- Process Queue Card ---
        st.markdown('''<div class="card">
            <div class="card-title">📋 Process Queue</div>
            <div class="card-body">Processes ready for scheduling.</div>
        </div>''', unsafe_allow_html=True)

        if st.session_state.processes:
            df_input = pd.DataFrame(st.session_state.processes)
            df_input.columns = ["PID", "Arrival Time", "Burst Time"]
            st.dataframe(df_input, use_container_width=True, hide_index=True)

            # Process chips visual
            chips_html = " ".join([f'<span class="process-chip">P{p["pid"]}</span>' for p in st.session_state.processes])
            st.markdown(f'<div style="margin: 8px 0 16px 0;">{chips_html}</div>', unsafe_allow_html=True)

            if st.button("🚀 Run Simulation", type="primary", use_container_width=True):
                # Convert dict to Process objects
                process_objects = [Process(p['pid'], p['arrival'], p['burst']) for p in st.session_state.processes]
                scheduler = CPUScheduler()

                if algo == "FCFS":
                    result_procs, timeline = scheduler.fcfs(process_objects)
                elif algo == "SJF (Non-Preemptive)":
                    result_procs, timeline = scheduler.sjf_non_preemptive(process_objects)
                else:
                    result_procs, timeline = scheduler.round_robin(process_objects, quantum)

                # ======== GANTT CHART ========
                st.markdown("---")
                st.markdown('''<div class="card">
                    <div class="card-title">📊 Gantt Chart</div>
                    <div class="card-body">Visual timeline of process execution.</div>
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
                            text=f"{task} ({row['Start']}-{row['Finish']})",
                            textposition='inside',
                            textfont=dict(color='white', size=11),
                            showlegend=show_legend,
                            hovertemplate=f"<b>{task}</b><br>Start: {row['Start']}ms<br>End: {row['Finish']}ms<extra></extra>"
                        ))

                    fig.update_layout(
                        barmode='stack',
                        xaxis_title="Time (ms)",
                        yaxis_visible=False,
                        height=180,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        margin=dict(l=0, r=0, t=10, b=40),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # ======== PERFORMANCE METRICS ========
                st.markdown('''<div class="card">
                    <div class="card-title">📈 Performance Metrics</div>
                    <div class="card-body">Detailed scheduling results per process.</div>
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

                st.dataframe(pd.DataFrame(res_data), use_container_width=True, hide_index=True)

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
                    <div class="empty-state-text">No processes added yet.<br>Use the panel on the left to add processes manually or via CSV.</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)


elif module == "Memory Management":
    st.markdown('<div class="sub-header">🧠 Memory Management Simulator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('''<div class="card">
            <div class="card-title">🔧 Configuration</div>
            <div class="card-body">Set up the page replacement algorithm.</div>
        </div>''', unsafe_allow_html=True)

        algo_mem = st.selectbox("Algorithm", ["FIFO", "LRU"])
        frames = st.number_input("Number of Frames", min_value=1, max_value=10, value=3)
        ref_string = st.text_input("Reference String (comma separated)", "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1")

        try:
            preview_pages = [int(x.strip()) for x in ref_string.split(',')]
            chips = " ".join([f'<span class="process-chip">{p}</span>' for p in preview_pages])
            st.markdown(f'''<div class="card">
                <div class="card-title">📄 Page Sequence ({len(preview_pages)} pages)</div>
                <div style="margin-top: 8px;">{chips}</div>
            </div>''', unsafe_allow_html=True)
        except Exception:
            pass

    with col2:
        if st.button("🚀 Simulate Memory", type="primary", use_container_width=True):
            try:
                pages = [int(x.strip()) for x in ref_string.split(',')]
                manager = MemoryManager()

                if algo_mem == "FIFO":
                    faults, snapshots = manager.fifo(pages, frames)
                else:
                    faults, snapshots = manager.lru(pages, frames)

                hits = len(pages) - faults

                st.markdown('''<div class="card">
                    <div class="card-title">📊 Results Summary</div>
                    <div class="card-body">Overall performance of {algo} algorithm.</div>
                </div>'''.replace("{algo}", algo_mem), unsafe_allow_html=True)

                m1, m2, m3 = st.columns(3)
                with m1:
                    metric_card("Page Faults", f"{faults}")
                with m2:
                    metric_card("Page Hits", f"{hits}")
                with m3:
                    hit_ratio = hits / len(pages) * 100 if pages else 0
                    metric_card("Hit Ratio", f"{hit_ratio:.1f}%")

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown('''<div class="card">
                    <div class="card-title">📉 Fault vs Hit Analysis</div>
                </div>''', unsafe_allow_html=True)

                fig_pie = px.pie(
                    values=[faults, hits],
                    names=["Faults", "Hits"],
                    color_discrete_sequence=["#ff4b4b", "#00f260"],
                    hole=0.45
                )
                fig_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=280,
                    margin=dict(l=20, r=20, t=10, b=10),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                )
                fig_pie.update_traces(
                    textinfo='percent+label',
                    textfont_size=14
                )
                st.plotly_chart(fig_pie, use_container_width=True)

                st.markdown('''<div class="card">
                    <div class="card-title">🔄 Step-by-Step Execution</div>
                    <div class="card-body">Memory frame state at each page request.</div>
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
                        return 'color: #ff4b4b; font-weight: bold; background-color: rgba(255,75,75,0.1)'
                    elif val == 'Hit':
                        return 'color: #00f260; font-weight: bold; background-color: rgba(0,242,96,0.1)'
                    return ''

                st.dataframe(
                    df_mem.style.map(color_status, subset=['Status']),
                    use_container_width=True,
                    hide_index=True
                )

            except ValueError:
                st.error("⚠️ Please enter a valid comma-separated list of integers for the reference string.")
        else:
            st.markdown('''
            <div class="card">
                <div class="empty-state">
                    <div class="empty-state-icon">🧠</div>
                    <div class="empty-state-text">Configure parameters on the left and click <b>Simulate Memory</b> to begin.</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)