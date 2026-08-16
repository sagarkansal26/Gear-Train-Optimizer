# Gear Train Design & Optimization Tool
## 🔗 Live App
[Open the live app →](https://gear-train-optimizer.streamlit.app/)

A Python/Streamlit application that takes gear design requirements — power, speed, and target ratio — and automatically generates, validates, and ranks candidate spur gear designs using real mechanical engineering calculations (Lewis bending stress equation, safety factor analysis).





---

## What it does

Designing a gear train involves choosing teeth counts, module, and material such that the resulting design safely transmits the required power without failing under bending stress. Doing this by hand means testing dozens of teeth/module combinations manually.

This tool automates that process:
1. Takes your power, RPM, target gear ratio, material, and safety requirements
2. Generates every valid candidate design across a search space of teeth counts and standard modules
3. Filters candidates to those matching your target ratio within tolerance
4. Runs full force, stress, and safety-factor calculations on every surviving candidate
5. Filters out unsafe designs and automatically selects the strongest candidate

---

## Features

- **Full calculation engine** — gear ratio, torque, angular velocity, tangential/radial forces, Lewis bending stress, and safety factor, all computed from first principles
- **Automated candidate search & ranking** — no manual trial-and-error; the tool searches the design space and picks the best safe design
- **Interactive Streamlit UI** — real-time inputs with sensible defaults, an Advanced Options panel for secondary parameters, and a live materials reference table
- **Defensive input handling** — unknown materials raise clear errors instead of silent crashes
- **Fully tested** — 19 automated tests (pytest) covering every calculation, including cross-checks against an independent published Lewis-equation source
- **Documented engineering limitations** — the tool is explicit about using the simplified Lewis equation (not the full AGMA method), and about the reference material data being simplified educational values, not certified datasheet numbers

---




## Tech Stack

- **Python**
- **Streamlit** — interactive web UI
- **Pandas** — candidate generation, filtering, and data handling
- **NumPy** — numerical operations

---

## Installation & Running Locally

```bash
# Clone the repository
git clone https://github.com/sagarkansal26/Gear-Train-Optimizer.git
cd Gear-Train-Optimizer

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## Running the Tests

```bash
python -m pytest tests/ -v
```

All 19 tests should pass, covering:
- Every function in `calculations.py` (gear ratio, torque, forces, bending stress, safety factor)
- Candidate generation and filtering (`candidates.py`)
- Design optimization and selection logic (`optimiser.py`)
- Error handling for invalid material input
- Cross-validation against an independent published source for the Lewis bending equation

---

## Project Structure

```
Gear_Train_Optimiser/
├── app.py                  # Streamlit UI and orchestration
├── src/
│   ├── calculations.py     # Core engineering calculations (11 functions)
│   ├── candidates.py       # Candidate generation and filtering
│   └── optimiser.py        # Safety filtering and best-candidate selection
├── data/
│   └── materials.csv       # Reference material properties
├── tests/                  # Full pytest suite (19 tests)
└── requirements.txt
```

---

## Engineering Methodology & Limitations

This tool uses the **simplified 1892 Lewis bending equation**, not the full modern AGMA standard (which includes dynamic, load-distribution, and reliability factors). This was a deliberate choice to build a correct, well-tested foundation before adding complexity — a limitation explicitly documented in the code itself.

Material property values in `materials.csv` are simplified reference figures suitable for educational/preliminary design use, **not** a substitute for certified material datasheets.

The bending stress implementation was cross-validated against an independent, published Lewis-equation source ([link/description if you want to cite it]), confirming the formula implementation is correct.

---

## What I Learned Building This


- Structuring a Python project with clean separation between calculation logic, data handling, and UI
- Writing a full automated test suite with pytest, including tolerance-based floating-point comparisons and deliberate exception testing
- Building an interactive Streamlit interface driven by real backend logic rather than hardcoded values

---

## Future Improvements

- Full AGMA-standard stress calculations (dynamic factor, load distribution factor, etc.)
- Support for helical and bevel gears
- Export selected design to a PDF/report
- Additional material datasets from certified sources

---

## Author

**Sagar Kansal**
- www.linkedin.com/in/sagar-kansal
