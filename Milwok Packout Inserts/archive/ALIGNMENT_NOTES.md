# Aligned scans — ready for reverse engineering

All five `_READY` scans, aligned and cleaned. Files: `<part>_ALIGNED.stl`.

## Conventions (identical for every file)

- **X** = length (longest), **Y** = width, **Z** = height. Axes squared to the part itself:
  leveled on the dominant flat faces and rotated so walls sit exactly on X/Y. Residual
  tilt < 0.01° on every part.
- **Z+ = up = the side the cavities/holes open toward** (mag slots up, 9mm cartridge grid up).
  For the 762/556 bottoms that is the big-cavity side (the lip layer sits at the bottom).
- **Origin**: XY at the footprint center, Z=0 at the bottom face. Front/Top/Right planes in
  SolidWorks line up with the part directly.

## Parts

| File | Size (mm) | Faces | Notes |
|---|---|---|---|
| 556mag_top_ALIGNED | 210.9 × 163.6 × 41.2 | 40k | fair scan; walls partly missing |
| 556mag_bot_ALIGNED | 213.4 × 165.1 × 41.7 | 200k | roughest scan; **57 debris fragments removed** |
| 762mag_top_ALIGNED | 202.4 × 156.1 × 41.0 | 40k | good |
| 762mag_bot_ALIGNED | 209.3 × 163.0 × 41.2 | 40k | best scan |
| 9mm_ALIGNED | 309.7 × 216.6 × 33.0 | 50k | cartridge-grid side up; frame leveled to the pan's flats |

## Measured numbers you may want (from the CAD work, all in `_CAD_Project/PROJECT.md`)

762 bottom: deck/ledge plane 32.3 up from the bottom, total 40.6; mag openings ≈153.2–153.6 × 30.5–30.9
with a ~0.55 mm taper along the length (alternating flipped slots); all-around lip +0.85 mm/side,
end reach 8.1/7.6; outer skirt drafted ~1° (209.3 at the cutout side → 207.4 at the other);
slot walls vertical within 0.1 mm. Scan noise floor ≈ 0.2 mm — treat dimensions beyond one decimal with suspicion.

Scans are open shells (not watertight) — import as mesh/graphics bodies for reference sketching.
