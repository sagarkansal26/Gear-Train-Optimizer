# Gear Train Design & Optimization Tool — Progress Log

This file tracks project progress so work can resume smoothly in any new chat session, regardless of account/token limits. If starting a new conversation, paste this file's contents (or link the GitHub repo) and say: "Continue mentoring me on this project from here, following the same teaching rules as before — progressive lessons, no code dumps, exercise-then-review, escalating hints."

---

## Project Overview

**Goal:** Build a Gear Train Design & Optimization Tool as a CV/portfolio project — a Streamlit app that takes design requirements (power, speed, ratio) and outputs validated, ranked candidate gear designs with visualizations.

**Learner profile:** Mechanical Engineering student, basic-to-intermediate Python. Learning NumPy, Pandas, SciPy, Streamlit, Git/GitHub, testing, and clean project architecture through this project.

**Teaching style:** Progressive, concept-first, exercise-then-review, escalating hints (conceptual → pseudocode → partial code → full solution), no code dumps. Interview-question checkpoints after major features. Quiz format preferred as multiple-choice/tap-to-answer over typed answers, when the tool is available.

**GitHub repo:** `https://github.com/sagarkansal26/Gear-Train-Optimizer` (public, actively pushed)

---

## Project Structure (current)

```
Gear_Train_Optimiser/
├── app.py                      # orchestrator — imports & calls src/ functions with test values, prints results
├── src/
│   ├── __init__.py             # empty, makes src/ a package
│   ├── calculations.py         # 9 functions, all documented — see below
│   ├── candidates.py           # generate_candidates() + filter_by_ratio(), both done and tested
│   ├── optimiser.py            # NOT STARTED (still spelled "optimiser" — naming decision not yet finalized, see Open Items)
│   └── validation.py           # NOT STARTED
├── data/
│   └── materials.csv           # STILL EMPTY — needed next lesson (yield strength for safety factor)
├── tests/
│   ├── test_calculations.py    # NOT STARTED
│   ├── test_candidates.py      # NOT STARTED
│   └── test_optimiser.py       # NOT STARTED
├── .gitignore                  # DONE
├── PROCESS.md                  # this file
├── README.md                   # NOT STARTED (still empty)
└── requirements.txt            # DONE (numpy, pandas)
```

---

## `src/calculations.py` — 11 functions, all complete with docstrings (updated through Lesson 14)

1. `calc_gear_ratio(teeth_driver, teeth_driven)` → `teeth_driven / teeth_driver`
2. `rpm_to_omega(rpm)` → `(2 * 3.14 * rpm) / 60`
3. `calc_driver_torque(power, omega_driver)` → `power / omega_driver`
4. `calc_driven_side(gear_ratio, omega_driver, torque_driver)` → returns `(omega_driven, torque_driven)` tuple
5. `calc_pitch_diameter(module, teeth)` → `module * teeth` (returns mm)
6. `calc_tangential_force(torque, pitch_diameter_mm)` → converts mm→m internally, returns `2*torque/pitch_diameter_m` in Newtons
7. `calc_radial_force(tangential_force, pressure_angle_deg)` → uses `math.radians()` + `math.tan()`, returns Newtons
8. `get_lewis_form_factor(teeth)` → dictionary lookup table (standard 20° pressure-angle Y values for teeth 12–300), finds nearest match via `min(..., key=lambda t: abs(t-teeth))`
9. `calc_bending_stress(tangential_force, module, face_width, y_factor)` → `tangential_force / (module * face_width * y_factor)`, returns N/mm² (approx MPa) — docstring explicitly flags this as the simplified Lewis equation (no AGMA dynamic/reliability factors), recommends validation against textbook
10. `get_allowable_stress(material_name)` → reads `data/materials.csv` via `pd.read_csv()`, filters by exact material name match, returns `allowable_bending_stress_mpa` value. **KNOWN LIMITATION (not yet fixed):** if `material_name` doesn't exist in the CSV, this crashes with `IndexError: index 0 is out of bounds for axis 0 with size 0` — no error handling yet. This is intentionally deferred to a future lesson on input validation/error handling (ties into `src/validation.py`, still empty).
11. `calc_safety_factor(allowable_stress, bending_stress)` → `allowable_stress / bending_stress`, dimensionless. Rule of thumb: >1 = predicted to survive, but real engineering wants meaningful margin (1.5–3+), not a value near 1.0.

**Note:** `import math` and `import pandas as pd` are both at top of `calculations.py` (math for functions 7/8, pandas for function 10).

### `data/materials.csv` — populated (Lesson 14)
```
material,allowable_bending_stress_mpa
Cast Iron,55
Steel (Low Carbon),138
"Steel (Medium Carbon, Heat Treated)",275
Alloy Steel,414
Bronze,55
```
**Important CSV lesson learned:** any material name containing a comma (e.g. "Steel (Medium Carbon, Heat Treated)") MUST be wrapped in double quotes, or the comma gets misread as a column separator and silently corrupts the row (data shifts into wrong columns, no error thrown). Values are simplified/approximate references for the Lewis equation from introductory machine design sources — documented as NOT a substitute for a real materials datasheet, per Rule #16.

**Verified test case** (teeth_driver=20, teeth_driven=60, rpm=1500, power=5000, module=2, pressure_angle=20°, face_width=10×module=20):
- gear_ratio = 3.0, omega_driver ≈ 157.0, torque_driver ≈ 31.85 N·m
- omega_driven ≈ 52.33, torque_driven ≈ 95.54 N·m
- pitch_diameter_driver=40mm, pitch_diameter_driven=120mm, center_distance=80mm
- tangential_force = 1592.5 N, radial_force ≈ 579.62 N
- Y_factor (teeth=20, exact table match) = 0.29
- bending_stress ≈ 137.28 N/mm² — hand-verified: 1592.5/(2×20×0.29) = 137.28 ✓
- allowable_stress ("Steel (Low Carbon)") = 138
- **safety_factor ≈ 1.005** — technically >1 but a poor/risky design in real practice (essentially no margin; real designs typically target 1.5–3+). This result is a good illustration of *why* the optimizer step matters — a candidate can look "valid" but still be a bad choice.

**FULL CALCULATION CHAIN NOW COMPLETE:** power/speed → torque → forces → bending stress → safety factor, for a single candidate. Next major step is applying this across every row of the filtered candidates DataFrame at once (Lesson 15, needs Pandas `.apply()` — not yet taught).

## `src/candidates.py` — 2 functions, complete and tested

- `generate_candidates(target_ratio, standard_modules, teeth_range)`: nested loop, imports `calc_pitch_diameter` from `src.calculations`, builds list-of-dicts → Pandas DataFrame. Returns 7 columns: module, teeth_driver, teeth_driven, actual_ratio, pitch_diameter_driver, pitch_diameter_driven, center_distance.
- `filter_by_ratio(df, target_ratio, tolerance)`: boolean mask filter (`&` not `and`), keeps rows where `actual_ratio` within `target_ratio ± tolerance`. Kept as a SEPARATE function from `generate_candidates` deliberately (single responsibility principle) — do not merge these.

**Verified:** target_ratio=2.7, modules=[1,2,3], teeth_range=[15,20,25] → 9 candidates generated; tolerance=0.01 correctly filters down to 3 rows (only exact actual_ratio=2.7 matches, teeth_driver=20 across all 3 modules). Original DataFrame indices preserved after filtering (not renumbered) — expected Pandas behavior.

## `app.py` — orchestrator only, no logic
Currently defines test variables explicitly at top (`teeth_driver=20`, `teeth_driven=60`, `module=2`, etc. — IMPORTANT lesson learned: must define these as real named variables, NOT just pass literals into functions, since function parameter names don't leak out as caller-side variables), then calls the full chain from both modules in sequence, printing every result. Also sets `pd.set_option('display.max_columns', None)` and `pd.set_option('display.width', None)` near the top so full DataFrames print without truncation in the console.

---

## Engineering Concepts Covered
- Gear ratio, angular velocity (rad/s), torque, power relationship (`Power = Torque × omega`), why torque↑ when speed↓ (power conservation, ideal/lossless assumption — documented as a limitation)
- Gear module, pitch diameter, center distance
- Why teeth counts must be integers → achieved ratio only approximates target → justifies tolerance-based filtering
- Tangential force (from torque and pitch radius — unit consistency mm→m is critical)
- Pressure angle (standard 20°) and radial force (`tangential_force × tan(pressure_angle)`)
- Lewis bending stress: simplified 1892 formula, Y form factor from a standard published lookup table (NOT invented/computed) — explicit documentation that this is the simplified educational version, not full AGMA-standard stress analysis, per project Rule #16 (never invent formulas, always distinguish simplified vs. industry-standard, document assumptions/limitations)

## Python/Tooling Concepts Covered
- Functions with Google-style docstrings (Args/Returns with units specified), no `input()`/`print()` inside logic functions (separation of concerns)
- NumPy: `np.array`, `np.arange` (stop exclusive), vectorization vs loops
- Pandas: DataFrames built two ways (column-dict, and list-of-dicts from a loop), boolean mask filtering with `&`/`|`, `pd.set_option` for display width/columns
- Nested loops for combinatorial candidate generation, f-strings
- Python dictionaries as lookup tables; `min(iterable, key=lambda...)` pattern for finding closest match
- `math.radians()`/`math.tan()` — trig functions expect radians, not degrees
- Explicit unit-labeled parameter names as a defensive coding habit (e.g. `pitch_diameter_mm`, `pressure_angle_deg`)
- Critical distinction: function parameter names ≠ caller-side variables; passing a literal doesn't create a named variable in the calling file
- Python packages: `__init__.py`, `from src.module import function` — must use `src.xxx` form from ANY file including files inside `src/` itself
- Git: init, add, commit, push, `.gitignore`, remote/origin — full workflow practiced multiple times, now a solid habit
- PyCharm: venv per project, terminal, Rename Refactor tool
- Naming consistency (avoiding mixed spellings like "diametre"/"diameter"), lowercase variables vs capitalized classes, avoiding hardcoded "magic numbers" scattered through a file

---

## Immediate Next Steps (in order)

1. **Lesson 15 (next up):** Apply the full calculation chain (tangential force → radial force → bending stress → safety factor) across EVERY row of the filtered candidates DataFrame at once, not just one hardcoded example. Needs a new Pandas concept: `.apply()` (running a function across DataFrame rows) — not yet taught, teach as part of this lesson. End result: filtered candidates DataFrame gains new columns (tangential_force, radial_force, bending_stress, safety_factor) for every single candidate.
2. Git commit checkpoint after this is working.
3. Mini-lesson on SciPy basics (not yet taught) before building `src/optimiser.py` — use `scipy.optimize` (or simpler: sort/rank by safety_factor using Pandas) to select best candidates by an objective (e.g., maximize safety factor while minimizing size/center distance — likely a multi-objective trade-off worth discussing).
4. Mini-lesson on `pytest` (not yet taught) before writing `tests/test_calculations.py`, `tests/test_candidates.py`, `tests/test_optimiser.py`.
5. (Optional, lower priority) Add basic error handling to `get_allowable_stress()` for unrecognized material names — ties into `src/validation.py`, still empty.
6. Build the Streamlit interface — `app.py` currently is just a test/orchestration script; this becomes the real UI (input form → results table → charts).
7. Validate results against a textbook example (e.g. Shigley's Mechanical Engineering Design) — per Rule #17.
8. Write README.md properly, add screenshots once UI exists.
9. Interview-question review across all phases before considering Project 1 "done."

## Rough Progress Estimate
~45% through Project 1 as of this log. Architecture, and the FULL calculation engine (ratio/torque/forces/bending stress/safety factor) are done, plus candidate generation+filtering. Remaining: applying calculations across all candidates at once, SciPy optimization, Streamlit UI, testing, and validation/documentation — the UI build is likely to be the single largest remaining time investment.

## Open Items / Decisions to Revisit
- **Naming: `optimiser.py` vs `optimizer.py`** — was raised early, recommended standardizing to American spelling ("optimizer") for consistency with rest of codebase and with `scipy.optimize`, but file is still named `optimiser.py` and not yet renamed. Worth deciding before writing real code into it (cheaper to rename now while empty).
- UI framework: **Streamlit confirmed** — a friend's suggestion of "Replit" was clarified as not a real alternative (Replit is a hosting/IDE platform, not a UI framework; Streamlit is staying).
- Spelling convention generally: American spelling throughout (e.g., "diameter" not "diametre") — enforce this consistently in any new code (including future `optimizer.py`/`optimiser.py` decision above).
- Projects 2 (Stock Backtesting) and 3 (Resume Matcher) have NOT been started — Project 1 must be completed first per original instructions.
- Exact safety factor formula (yield_strength / bending_stress, or with an additional factor) should be confirmed/taught properly in Lesson 14, not assumed.