# Milwok Packout Inserts — Scan-to-CAD Project

Goal: rebuild 5 scanned Packout inserts (+1 new 45 ACP variant) as clean re-printable CAD.
Per part: **STEP** (SolidWorks/Fusion/FreeCAD) + **STL** + params JSON (rebuildable locally via `run_local/`).
Scanner scale trusted (physical inserts gone). Fidelity-first: reproduce the scan; invent nothing; ask Sam with images when unsure.

## Status

| Part | Aligned bbox (mm) | Status |
|---|---|---|
| 762 bottom | 209.3 × 162.9 × 40.6 | ✅ **v6 delivered — only open item: end-wall draft verify** |
| 762 top | 202.4 × 155.7 × 41.2 | next — must mate with bottom |
| 5.56 bottom | 213.2 × 165.0 × 41.9 | queued (slots WITH floors) |
| 5.56 top | 210.8 × 163.6 × 42.8 | queued |
| 9mm tray | 305.1 × 213.8 × 32.1 | queued |
| 45 ACP tray | new design | queued — re-pitch 9mm layout for .45 ACP |

## Design rules from Sam

1. 762 slots NO floor (through); 5.56 slots WITH floors.
2. All slots in a tray identical, uniform pitch.
3. Fidelity first — no invented fillets; corners as measured (762 outer corners are near-sharp, r≈0.4–0.7). The 45° Packout corner chamfers stay chamfers.
4. Top+bottom pairs must mate properly (engineer when building tops).
5. Ask Sam with images when a feature is ambiguous.

## 762 bottom — v13 (`cad/762_bot_v13.step/.stl`, `762_bot_params.json`)

v13 = v12 + Sam's 7/22 night feedback (fewer/straighter lines, lip reach):
- **Line regularizer**: profiles are now fitted straight lines intersected at corners — slots are 8–12 lines each (were 25–31 wobbly segments). Outer kept on wall-snapping (regularizer over-merged its notches — reverted after a test).
- **Lip profile rebuilt without smearing**: the deep cavity is the slot profile STRETCHED lengthwise (features stay at their ends) then offset +0.85 all around — kills the stepped ghost lines Sam saw in SolidWorks. End reach stays at the measured 8.11/7.59.
- Verification: **median 0.22, p90 0.63, p99 1.24** (slots 0.21/0.54, outer 0.25/0.75) — best build; slightly localized ~1 mm zones remain at deep slot-end walls (sparse scan there).
- Same as v12: drafted skirt, per-slot PMAG shapes, alternating orientation, vertical slot walls, exports cutout-side-up, top-edge fillet NOT applied (OCCT + lofted skirt = OOM; one click in CAD).

## (superseded) v12 notes

Minimal-deviation build per Sam (7/22 late): **median 0.20 mm, p90 0.64, p99 1.43, 100% of scan surfaces** — at the scan's own noise floor.
- Each slot cut with its OWN measured PMAG profile (simplify 0.15, no snapping/canonicalizing) — taper, stepped end, everything as scanned. Orientation pattern alternates as designed.
- **All-around lip confirmed and measured**: deep cavity = the slot profile extended at the ends (+8.11/+7.59, flip-aware) and offset **+0.85 mm/side** (measured: 5159 deep points, mode −0.80 vs flush model). Sam was right; the earlier "flush" reading was a face-clustering artifact.
- Outer skirt: faithful DRAFT (lofted 209.26 → 207.08 in x over the height; y ~vertical) — the drop-in lead-in, reproduced instead of verticalized.
- Slot walls vertical (measured ±0.1). Exports in Sam's orientation (cutout side up).
- Top-edge 0.8 fillet NOT applied (OCCT chokes tessellating fillets on the lofted skirt — OOM). One-click in SolidWorks/Fusion if wanted.
- params schema v10+ (`mode: per_slot`, lofted outer); local kit updated + verified (433 cm³ match).

## (superseded) v9 notes

v9 supersedes v6 per Sam's 7/22 evening feedback:
- **Straight edges**: canonical long edges are least-squares line fits — real taper −0.55 mm over the span kept (identical in all 4 slots, mirrored on flipped ones = the mag-profile wedge; extraction wobble rms 0.1 removed).
- **Scan-true slot centers** (23.08/57.26/92.82/126.89, pitches 34.18/35.56/34.07) — uniform-pitch idealization removed per "deviation low" rule.
- **All-around lip question, current state**: ends extend +8.05/−7.67 (solid data). Side walls measured FLUSH at mid-depth (stem faces align with opening edges, n=8 faces, 3 cross-cuts) and both widened-side variants scored worse against the scan (v5: p90 2.69, v8: 2.82 vs v9: 1.22). Sam's screenshot ridge may be a shallow mouth ring or a ledge relief — OPEN question to Sam.
- Verification: median 0.34 mm, p90 1.22 (97%). Residual fin hotspots ≈ slot-to-slot shape variation vs the identical-canonical rule.
- Orientation locked: Sam's TOP = big-cavity openings; Sam's BOTTOM = single mag profile visible. Exports flipped accordingly; 0.8 fillet on Sam's-top edges.

## (superseded) v6 notes

Per Sam's design answers (7/22): each slot = TWO simple profiles — the mag through-profile (cuts 0→top) + the little END-LIP profile (floor→ledge z32.3, extends x only: L+8.05/R+7.67). ONE canonical profile, alternating 180° flips, staggered — scan-detected pattern **[flipped, canonical, flipped, canonical]**. All walls perfectly vertical.

- Outer: faithful 44-vertex snapped outline (mid-height, z=20), no invented rounding; corners near-sharp as measured; top-edge fillet r0.8 applied.
- Slots: canonical 20-vertex measured mag profile, uniform pitch 34.77, cx 104.8, centers y 22.8/57.6/92.4/127.1.
- Webs between slots: FULL thickness (~4.3 mm) all the way down — settled EMPIRICALLY: all-around lip (v5) pushed scan disagreement to p90 2.69 mm; ends-only (v6) drops it to 1.09. The sideways widening in the one deep loop was scanner bloom.
- Verification: median |d| 0.38 mm, p90 1.09 mm (97% of surfaces). Residual warm stripes = uniform-pitch idealization (real pitches 34.1/35.7/33.9).
- OPEN — wall verticality (Sam to verify): scan's outer END walls lean inward with height: footprint x 208.95 @z6 → 207.36 @z36 (~0.8 mm/side, ≈1.5°). Y-walls vertical (±0.2). Built vertical at mid-height (208.15). If the original truly had drafted end walls, or if vertical-at-base (209.0) is wanted for fit, say so. Slot walls measured dead vertical (±0.1) — no action.

## Local-run kit (`run_local/`)

`pip install -r requirements.txt` once → `python build_from_params.py "..\cad\762_bot_params.json"`.
v6 schema (canonical polygon + orientations + lip). Verified: local == cloud build (413 cm³) incl. fillet.

## Notes for remaining parts

- 762 top: extract underside interface; mate vs bottom rim/lip, ~0.2–0.3 mm print clearance.
- 5.56 pair: bottom scan is walls-missing — slot layout from 5.56-top sibling + floored slots.
- 9mm: analyze interior before rebuild (holes/dividers unknown); bed ≥305 mm or split.
- 45 ACP: same envelope as 9mm; resize features (.45: rim Ø12.2, OAL 32.4 vs 9mm Ø9.96/29.7).
- HQ reminder about manual CAD fillets: moot — automated fillet now works on faithful profiles.
