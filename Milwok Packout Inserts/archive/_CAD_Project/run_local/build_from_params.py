"""Rebuild a Packout insert from its params JSON — no scans or Claude needed.

Usage:  python build_from_params.py ..\\cad\\762_bot_params.json
Output: <part>_local.step / .stl next to the JSON.

Supports two schemas:
- per_slot (v10+): outer_pts (+ optional outer_pts_bottom/outer_pts_top for a drafted
  skirt loft), slots_pts = [{pts, lip_pts}], each cut vertically; H, z_step.
- canonical (v6-v9): slot {canonical_pts, cx, centers_y, orientations, lip{w,h,dx,dy,r},
  through / floor_z}.
Tweak by editing the JSON and re-running.
"""
import json, os, sys
import numpy as np
from build123d import *

p = json.load(open(sys.argv[1]))
out_base = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), p['part'] + '_local')

def ensure_ccw(pts):
    pts = np.asarray(pts, dtype=float)
    a = 0.0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return pts if a > 0 else pts[::-1]

def face_from(pts, z=0.0):
    return Face(Wire.make_polygon([Vector(q[0], q[1], z) for q in pts], close=True))

H = p['H']
z_step = p.get('z_step', 0)

if p.get('outer_pts_bottom') and p.get('outer_pts_top'):
    part = loft([face_from(ensure_ccw(p['outer_pts_bottom']), 0.0),
                 face_from(ensure_ccw(p['outer_pts_top']), H)])
else:
    part = extrude(face_from(ensure_ccw(p['outer_pts'])), amount=H)
assert part.bounding_box().max.Z > 1, 'extrude/loft direction wrong'

if p.get('mode') == 'per_slot':
    for s in p['slots_pts']:
        part = part - extrude(face_from(ensure_ccw(s['pts'])), amount=H + 1)
        if s.get('lip_pts'):
            part = part - extrude(face_from(ensure_ccw(s['lip_pts']), z=-1), amount=z_step + 2)
else:
    s = p['slot']
    can = np.asarray(s['canonical_pts'], dtype=float)
    orients = s.get('orientations', [1] * len(s['centers_y']))
    for cy, sgn in zip(s['centers_y'], orients):
        pts_slot = ensure_ccw(can * sgn + np.array([s['cx'], cy]))
        if s.get('through', False):
            part = part - extrude(face_from(pts_slot), amount=H + 1)
            lip = s.get('lip')
            if lip:
                part = part - extrude(Pos(s['cx'] + sgn * lip.get('dx', 0),
                                          cy + sgn * lip.get('dy', 0), -1) *
                                      RectangleRounded(lip['w'], lip['h'], lip.get('r', 1.5)),
                                      amount=z_step + 1)
        else:
            fz = s.get('floor_z', 2.5)
            part = part - extrude(face_from(pts_slot, z=fz), amount=H - fz + 1)

r_top = p.get('top_edge_fillet')
if r_top:
    try:
        part = fillet(part.edges().group_by(Axis.Z)[0], radius=r_top)
        print(f'top-edge fillet {r_top} OK')
    except Exception:
        print('top-edge fillet skipped (engine refused) — add in CAD if wanted')

print(f'volume {part.volume/1000:.0f} cm3')
if p.get('export_flip_x180'):
    part = Rotation(180, 0, 0) * part
    fb = part.bounding_box()
    part = Pos(-fb.min.X, -fb.min.Y, -fb.min.Z) * part
export_step(part, out_base + '.step')
export_stl(part, out_base + '.stl', tolerance=0.1)
print('wrote', out_base + '.step / .stl')
