# Local rebuild kit — zero Claude usage

Regenerate or tweak any insert on your own PC. The heavy scan analysis already
happened in the cloud; each part's result is boiled down to a small `*_params.json`
in the `cad/` folder. This kit turns a params file into STEP + STL locally.

## One-time setup (Windows)

1. Install Python 3.11+ from python.org (check "Add python.exe to PATH").
2. Open a terminal in this `run_local` folder and run:

       pip install -r requirements.txt

## Rebuild a part

       python build_from_params.py "..\cad\762_bot_params.json"

Writes `762_bot_local.step` and `.stl` into `cad\`.

## Tweak a part

Open the part's JSON in any text editor, change a number, re-run. Examples:
- slot width: `slots.opening[1]` (30.6 → 31.0 for looser mags)
- pitch: rebuild `centers_y` (evenly spaced center-to-center distances)
- overall height: `H`
- slot floors: `slots.through: false` + `slots.floor_z` (556 style) vs `through: true` (762 style)

New parts get their own JSON as Claude builds them — same command works for all.
