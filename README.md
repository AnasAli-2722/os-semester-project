# OS Simulator

Operating System Simulator — an interactive Streamlit application for visualizing and learning core OS concepts: CPU scheduling and page replacement algorithms. Built as a semester project for BSCS at UET Taxila.

## Features

- CPU Scheduling Simulator
  - FCFS, SJF (non-preemptive), Round Robin (configurable quantum)
  - Add processes manually or upload CSV (pid, arrival, burst)
  - Gantt chart visualization and per-process metrics (waiting time, turnaround, throughput)
- Memory Management Simulator
  - Page replacement algorithms: FIFO and LRU
  - Visual step-by-step frame table and summary metrics (faults, hits, hit ratio)
- Modern, responsive UI with themed cards, metric widgets, and Plotly charts

## Tech Stack

- Python 3.14 (tested)
- Streamlit (UI)
- Pandas (data handling)
- Plotly (visualizations)

## Prerequisites

- Windows / macOS / Linux
- Python 3.10+ (project tested with Python 3.14)
- Git (optional)

## Installation

1. Clone the repo

   git clone <repo-url>
   cd "OS project"

2. Create a virtual environment and activate it (Windows PowerShell example)

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

3. Install dependencies

   pip install -r requirements.txt

## Running the app

Start the Streamlit app:

   streamlit run app.py

Open the URL printed by Streamlit in your browser (e.g. `http://localhost:8501` or `http://localhost:8502`).

## Usage

- Use the left sidebar to choose a module (CPU Scheduling or Memory Management).
- For CPU simulation:
  - Add processes manually using the form, or upload a CSV with columns `pid, arrival, burst`.
  - Select algorithm and (for RR) set the time quantum.
  - Click `Run Simulation` to view the Gantt chart and metrics.
- For Memory simulation:
  - Select algorithm, set number of frames, and enter a comma-separated reference string.
  - Click `Simulate Memory` to see faults/hits and the step-by-step table.

## CSV Format (CPU upload)

CSV should have three columns (headers are case-insensitive):

- `pid` — Process identifier (integer)
- `arrival` — Arrival time (integer)
- `burst` — CPU burst time (integer)

Example:

pid,arrival,burst
1,0,5
2,1,3
3,2,8

## Project Structure

- `app.py` — Main Streamlit application and UI (contains CSS and page code)
- `algorithms/` — Algorithm implementations
  - `cpu.py` — CPU scheduling algorithms and `Process` dataclass
  - `memory.py` — Page replacement algorithms (FIFO, LRU)
- `requirements.txt` — Python dependencies

## Development notes & troubleshooting

- The UI includes a custom CSS block inside `app.py`. If the sidebar expand/collapse button is not visible, check the CSS area labeled `HIDE STREAMLIT DEFAULTS` and ensure the toolbar itself is not hidden (the expand button lives inside the toolbar).
- Avoid using broad selectors like `*`, `span`, or `button` with `!important` for font overrides — those can break Streamlit's Material Icons.
- Plotly charts use `width='stretch'` to work with recent Streamlit versions.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with a clear description of changes and rationale.

## Authors

- Mahnoor
- Anas

## License

This project has no license file in the repository. Add a `LICENSE` (for example, MIT) if you wish to make the licensing terms explicit.

---

If you want, I can also add examples, screenshots, or a short demo GIF to the README. Would you like that?