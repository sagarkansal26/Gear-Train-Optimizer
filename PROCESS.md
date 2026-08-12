# Gear Train Design & Optimization Tool — Progress Log

This file tracks project progress so work can resume smoothly in any new chat session, regardless of account/token limits. If starting a new conversation, paste this file's contents (or link the GitHub repo) and say: "Continue mentoring me on this project from here, following the same teaching rules as before."

---

## Project Overview

**Goal:** Build a Gear Train Design & Optimization Tool as a CV/portfolio project — a Streamlit app that takes design requirements (power, speed, ratio) and outputs validated, ranked candidate gear designs with visualizations.

**Learner profile:** Mechanical Engineering student, basic-to-intermediate Python. Learning NumPy, Pandas, SciPy, Streamlit, Git/GitHub, testing, and clean project architecture through this project.

**Teaching style:** Progressive, concept-first, exercise-then-review, escalating hints (conceptual → pseudocode → partial code → full solution), no code dumps. Interview-question checkpoints after major features.

**GitHub repo:** `https://github.com/sagarkansal26/Gear-Train-Optimizer` (public, pushed and working)

---

## Project Structure (current, matches plan)

```
Gear_Train_Optimiser/
├── app.py                      # orchestrator — imports & calls src/ functions, no logic itself
├── src/
│   ├── __init__.py             # empty, makes src/ a package
│   ├── calculations.py         # DONE — 5 pure functions, fully documented
│   ├── candidates.py           # DONE — generate_candidates(), needs filtering added
│   ├── optimiser.py            # NOT STARTED (note: spelled "optimiser", not "optimizer")
│   └── validation.py           # NOT STARTED
├── data/
│   └── materials.csv           # NOT STARTED (empty placeholder)
├── tests/
│   ├── test_calculations.py    # NOT STARTED
│   ├── test_candidates.py      # NOT STARTED
│   └── test_optimiser.py       # NOT STARTED
├── .gitignore                  # DONE (.venv/, __pycache__/, *.pyc, .idea/)
├── README.md                   # NOT STARTED (still empty)
└── requirements.txt            # DONE (numpy, pandas via pip freeze)
```

---

## What's Been Built So Far

### `src/calculations.py` — COMPLETE (5 functions, all with Google-style docstrings)

1. `calc_gear_ratio(teeth_driver, teeth_driven)` → `teeth_driven / teeth_driver`
2. `rpm_to_omega(rpm)` → `(2 * 3.14 * rpm) / 60`
3. `calc_driver_torque(power, omega_driver)` → `power / omega_driver`
4. `calc_driven_side(gear_ratio, omega_driver, torque_driver)` → returns `(omega_driven, torque_driven)` tuple
   - `omega_driven = omega_driver / gear_ratio`
   - `torque_driven = torque_driver * gear_ratio`
5. `calc_pitch_diameter(module, teeth)` → `module * teeth`

**Verified test case** (teeth_driver=20, teeth_driven=60, rpm=1500, power=5000):
- gear_ratio = 3.0
- omega_driver ≈ 157.0 rad/s
- torque_driver ≈ 31.85 N·m
- omega_driven ≈ 52.33 rad/s, torque_driven ≈ 95.54 N·m
- pitch_diameter (module=2): driver=40mm, driven=120mm, center_distance=80mm

**Key engineering assumption documented:** all calculations assume 100% efficiency (ideal, lossless gear pair) — real efficiency factor not yet added.

### `src/candidates.py` — MOSTLY COMPLETE

`generate_candidates(target_ratio, standard_modules, teeth_range)`:
- Nested loop over `standard_modules` × `teeth_range`
- For each combo: rounds `teeth_driven`, computes `actual_ratio`, calls `calc_pitch_diameter` (imported from `src.calculations`) for both gears, computes `center_distance`
- Builds list of dicts → returns as Pandas DataFrame with 7 columns: `module, teeth_driver, teeth_driven, actual_ratio, pitch_diameter_driver, pitch_diameter_driven, center_distance`
- **Verified working:** test case (target_ratio=2.7, modules=[1,2,3], teeth_range=[15,20,25]) produces 9 rows × 7 columns correctly, confirmed against hand calculations.

**NOT yet done:** tolerance-based filtering (keep only candidates within X% of target ratio) — this is Lesson 11, next up.

### `app.py` — orchestrator, imports and calls everything above with test values, prints results. Working end-to-end.

---

## Engineering Concepts Covered
- Gear ratio, angular velocity (rad/s), torque, power relationship (`Power = Torque × omega`)
- Why torque ↑ when speed ↓ (power conservation, ideal case)
- Gear module, pitch diameter, center distance
- Why teeth counts must be integers → achieved ratio is only ever an approximation of target ratio (this is why filtering/tolerance is needed, not a simplification we invented)

## Python/Tooling Concepts Covered
- Functions with docstrings (Args/Returns, Google style), no `input()`/`print()` inside logic functions (separation of concerns)
- NumPy: `np.array`, `np.arange` (stop is exclusive), vectorization vs loops
- Pandas: building DataFrames two ways (column-dict style, and list-of-dicts style), boolean mask filtering with `&`/`|` (not `and`/`or`)
- Nested loops for combinatorial candidate generation
- f-strings
- Python packages: `__init__.py`, `from src.module import function` pattern — and why imports must be written the same way (`src.xxx`) from *any* file in the project, including files inside `src/` itself
- Git: init, add, commit, push, `.gitignore`, remote/origin, GitHub repo setup
- PyCharm: venv per project, terminal, Rename Refactor tool
- Naming consistency (avoiding e.g. "diametre"/"diameter"/"dia" mixed spellings), lowercase variables vs capitalized classes

---

## Immediate Next Steps (in order)

1. **Lesson 11:** Add tolerance-based filtering to `generate_candidates()` (or as a separate function) — keep only rows where `actual_ratio` is within some % of `target_ratio`. Reuse the boolean-mask pattern from Lesson 4.
2. Git commit checkpoint after filtering is added.
3. Build out real engineering calculations still missing: tangential force, radial force, bending stress (Lewis equation), contact stress, safety factor — these go in `calculations.py`.
4. Write `src/optimiser.py` — use `scipy.optimize` (not yet taught) to rank/select best candidates by an objective (e.g., minimize size, maximize safety factor). Need a "learn SciPy basics" mini-lesson first, per the teaching rules.
5. Write `tests/test_calculations.py` using `pytest` (not yet taught — needs its own lesson).
6. Fill in `data/materials.csv` with real material properties (yield strength etc.) for stress/safety-factor calculations.
7. Build the Streamlit interface (`app.py` becomes the real UI — currently just a test/orchestration script).
8. Validate results against a textbook example (e.g. Shigley's Mechanical Engineering Design) — per original brief rule #17.
9. Write README.md properly, add screenshots once UI exists.
10. Interview-question review across all phases before considering Project 1 "done."

## Rough Progress Estimate
~25–30% through Project 1 as of this log (architecture + calculation engine + candidate generation core are done; optimization, Streamlit UI, testing, validation, and documentation are the majority of what's left).

## Decisions/Preferences to Remember
- UI framework: **Streamlit** (confirmed, staying with it — a mix-up about "Replit" was clarified as not a real alternative for this purpose)
- Spelling convention: American spelling throughout code (e.g., "diameter" not "diametre", "optimizer" was recommended over "optimiser" but the student's files currently use "optimiser" — worth reconfirming/renaming for consistency before this file grows further)
- Quiz format: prefers multiple-choice tap-to-answer format over typing long answers
- Project 2 (Stock Backtesting) and Project 3 (Resume Matcher) have NOT been started — Project 1 must be completed first per original instructions