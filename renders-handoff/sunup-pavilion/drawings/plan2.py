"""Pavilion concept plan v2: 16x20 roof, posts 13x16 c/c, 2' overhang front/sides, 1' at the back wall.
Units feet. x along the long side (left -> right as seen from inside facing the back wall), y from the back post line
toward the open front."""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Polygon

P = 11.25/12; h = P/2                       # post 11-1/4" square
W, L = 12.0, 16.0                           # post centres
RX0, RX1, RY0, RY1 = -2.0, L+2.0, -2.0, W+2.0   # roof / slab edge
INK, GREY, LIGHT = '#2b2b2b', '#8f8f8f', '#cfc9be'
WOOD, FAB, TVC = '#e9e6df', '#e4ddd0', '#1d1d1d'

def ftin(v):
    s = '-' if v < 0 else ''; v = abs(v); f = int(v + 1e-9); i = (v - f)*12
    q = round(i*8)/8
    if q >= 12: f, q = f+1, 0
    w = int(q); fr = q - w
    frs = {0: '', .125: ' 1/8', .25: ' 1/4', .375: ' 3/8', .5: ' 1/2', .625: ' 5/8', .75: ' 3/4', .875: ' 7/8'}[round(fr, 3)]
    return f"{s}{f}'-{w}{frs}\""

def dim(ax, a, b, at, text, horiz=True, fs=8.5, c=INK):
    if horiz:
        ax.annotate('', (a, at), (b, at), arrowprops=dict(arrowstyle='<->', lw=0.7, color=c, shrinkA=0, shrinkB=0))
        ax.text((a+b)/2, at-0.12, text, ha='center', va='bottom', fontsize=fs, color=c, bbox=dict(fc='white', ec='none', pad=0.4))
    else:
        ax.annotate('', (at, a), (at, b), arrowprops=dict(arrowstyle='<->', lw=0.7, color=c, shrinkA=0, shrinkB=0))
        ax.text(at-0.12, (a+b)/2, text, ha='right', va='center', fontsize=fs, color=c, rotation=90, bbox=dict(fc='white', ec='none', pad=0.4))

fig, ax = plt.subplots(figsize=(16, 11.6))
# slab: salt field + broom border band
ax.add_patch(Rectangle((RX0, RY0), RX1-RX0, RY1-RY0, fc='#e2ded6', ec=INK, lw=1.2, zorder=0))
ax.add_patch(Rectangle((-h, -h), L+P, W+P, fc='#efece6', ec='none', zorder=0))
for yy in [RY0 + k*0.12 for k in range(int((RY1-RY0)/0.12)+1)]:      # broom texture on the border band only
    for xa, xb in ((RX0, -h), (L+h, RX1)):
        ax.plot([xa, xb], [yy, yy], lw=0.25, color='#cdc7bb', zorder=0)
for xx in [RX0 + k*0.12 for k in range(int((RX1-RX0)/0.12)+1)]:
    pass
for yy in [RY0 + k*0.12 for k in range(int((RY1-RY0)/0.12)+1)]:
    if yy < -h or yy > W+h: ax.plot([-h, L+h], [yy, yy], lw=0.25, color='#cdc7bb', zorder=0)
# saw cuts: border at outside face of posts, carried to the slab edge; centre cross joints
cut = dict(lw=1.0, color='#6d6458', ls=(0, (5, 2)), zorder=1)
for xx in (-h, L+h): ax.plot([xx, xx], [RY0, RY1], **cut)
for yy in (-h, W+h): ax.plot([RX0, RX1], [yy, yy], **cut)
ax.plot([L/2, L/2], [RY0, RY1], **cut); ax.plot([RX0, RX1], [W/2, W/2], **cut)
# roof: hips from post corners at 45 deg, 3' ridge, clipped back corners (1' overhang at the back)
ry = W/2; rx0, rx1 = -h + (W+P)/2, L+h - (W+P)/2
rl = dict(lw=0.9, color='#b5aa98', zorder=1)
ax.plot([rx0, rx1], [ry, ry], lw=2.2, color='#b5aa98', zorder=1)
for (cx, cy, sx, sy) in ((-h, W+h, -1, 1), (L+h, W+h, 1, 1), (-h, -h, -1, -1), (L+h, -h, 1, -1)):
    ex = rx0 if sx < 0 else rx1
    ax.plot([cx, ex], [cy, ry], **rl)
    d = (RY1 - cy) if sy > 0 else (cy - RY0)
    ax.plot([cx, cx + sx*d], [cy, cy + sy*d], **rl)
# gutters + downspouts
ax.add_patch(Rectangle((RX0, RY0), RX1-RX0, RY1-RY0, fill=False, ec='#7d8a96', lw=2.6, zorder=2, alpha=0.55))
for (dx, dy) in ((RX0+0.35, RY0-0.25), (RX1-0.35, RY0-0.25), (RX1+0.25, RY1-0.35)):
    ax.add_patch(Rectangle((dx-0.17, dy-0.17), 0.34, 0.34, fc='#7d8a96', ec=INK, lw=0.6, zorder=6))
ax.text(RX0+0.7, RY0-0.32, 'DS', fontsize=7.5, va='center'); ax.text(RX1-0.75, RY0-0.32, 'DS', fontsize=7.5, va='center', ha='right')
ax.text(RX1+0.5, RY1-0.35, 'DS (if needed)', fontsize=7.5, va='center')
# posts
for px in (0, L):
    for py in (0, W):
        ax.add_patch(Rectangle((px-h, py-h), P, P, fc='white', ec=INK, lw=1.3, zorder=7))
# back wall: 2x6, centred on posts, inset ~1 7/8" from both post faces
wt = 7.5/12
ax.add_patch(Rectangle((h, -wt/2), L-P, wt, fc='#bdb6aa', ec=INK, lw=0.9, zorder=5))
# TV + sconces + bench + shelves (TV centred on the wall)
tvw = 61.0/12; cx = L/2
ax.add_patch(Rectangle((cx-tvw/2, wt/2), tvw, 0.22, fc=TVC, ec=INK, zorder=6))
ax.text(cx, wt/2+0.42, '70" TV + soundbar', ha='center', va='top', fontsize=8.5)
sl = (h + cx - tvw/2)/2; sr = (cx + tvw/2 + L - h)/2
for s in (sl, sr):
    ax.add_patch(Circle((s, wt/2+0.12), 0.2, fc='#c8a24a', ec=INK, lw=0.8, zorder=6))
for s_ in (sl, sr):
    ax.add_patch(Rectangle((s_-1.6, wt/2), 3.2, 0.85, fc='none', ec=INK, lw=0.8, ls=(0, (3, 2)), zorder=5))
    ax.text(s_, wt/2+1.05, 'floating shelves\n(sconce above)', ha='center', va='top', fontsize=7.5)
# kitchen at the right end: front flush with inside face of posts, 30" deep, back at the drip edge
kx0, kd = L - h, 2.5
ax.add_patch(Rectangle((kx0, h), kd, W-P, fc='#3a3a3a', ec=INK, lw=1.0, zorder=4))
run = [('', 12), ('ICE / DRINKS 24"', 24), ('CABINETS 24"', 24), ('', 18), ('GRILL 36" / LP below', 36), ('', 18.75)]
yk = h
for name, w in run:
    hh = w/12
    if name:
        fc = {'G': '#9a9a9a', 'I': '#a9c6d6'}.get(name[0], '#c9c9c9')
        ax.add_patch(Rectangle((kx0+0.22, yk+0.06), kd-0.44, hh-0.12, fc=fc, ec=INK, lw=0.6, zorder=5))
        ax.text(kx0+kd/2, yk+hh/2, name, rotation=90, ha='center', va='center', fontsize=7, zorder=6)
    yk += hh
ax.text(RX1+0.3, W/2+3.6, 'black\ncountertop,\nstainless\ncabinets', fontsize=7.5, va='center')
ax.add_patch(Rectangle((kx0-3.5, h), 3.5, W-P, fc='#f3e7c9', ec='none', alpha=0.85, zorder=2))
ax.text(kx0-1.75, W/2+2.2, "COOK AISLE 3'-6\"", rotation=90, ha='center', va='center', fontsize=8, color='#8a6d2e', zorder=3)
# lounge: sofa centred on the TV, back on the front post line (slab runs 2' past it)
sb = W; sf = sb - 3.0; sw = 8.0; m0 = cx - sw/2
fab = dict(boxstyle='round,pad=0,rounding_size=0.35', fc=FAB, ec=INK, lw=0.9, zorder=4)
ax.add_patch(FancyBboxPatch((m0, sf), sw, 3.0, **fab))
ax.add_patch(FancyBboxPatch((m0, sb-7.0), 3.0, 7.0, **fab))
ax.add_patch(FancyBboxPatch((m0+3.6, sf-2.6), 3.6, 2.0, boxstyle='round,pad=0,rounding_size=0.25', fc='#d8c3a5', ec=INK, lw=0.8, zorder=4))
ax.text(cx+1.2, sf+1.5, 'SECTIONAL', ha='center', va='center', fontsize=8.5, zorder=5)
ax.annotate('', (cx+2.9, wt/2+0.25), (cx+2.9, sf), arrowprops=dict(arrowstyle='<->', lw=0.8, color='#7a5c3a'), zorder=6)
ax.text(cx+3.05, 2.2, f"viewing\n{ftin(sf-wt/2-0.25)}", fontsize=8, color='#7a5c3a', va='top')
# fan on ridge + soffit lights
ax.add_patch(Circle((L/2, W/2), 26/12, fill=False, ec='#2f6f8f', lw=1.2, ls=(0, (4, 2)), zorder=6))
ax.text(L/2, W/2-2.35, '52" fan + light on ridge', ha='center', fontsize=8, color='#2f6f8f', zorder=6)
for (lx, ly) in ((L*0.25, W+1.15), (L*0.75, W+1.15), (-1.15, W*0.3), (-1.15, W*0.7)):
    ax.add_patch(Circle((lx, ly), 0.17, fc='#ffd76a', ec=INK, lw=0.7, zorder=6))
ax.text(L*0.25+0.3, W+1.15, 'soffit light', fontsize=7, va='center', zorder=6)
ax.text(-0.95, W*0.3-0.35, 'soffit light', fontsize=7, va='center', rotation=90, zorder=6)
ax.text(L/2, -0.05, 'LED tape on top of the interior cornice, all 4 beams', fontsize=7, ha='center', va='center', color='#9a7a20', zorder=7)
# labels
ax.text(-1.0, W/2 + 0.6, 'OPEN SIDE', rotation=90, fontsize=9, color=GREY, ha='center', va='center')
ax.text(L/2, RY1 + 0.55, 'OPEN FRONT', fontsize=9, color=GREY, ha='center')
ax.text(RX0+0.15, RY1-0.25, 'BROOM-FINISH BORDER', fontsize=7, color='#6d6458')
ax.text(1.0, W/2+0.35, 'SALT FINISH', fontsize=7.5, color='#6d6458')
ax.text(L/2+0.15, RY1-0.15, 'saw cut', fontsize=7, color='#6d6458', rotation=90, va='bottom')
for xx in (3.0, 8.0, 13.0):
    ax.annotate('', (xx, RY1-0.2), (xx, RY1-1.5), arrowprops=dict(arrowstyle='->', lw=1.0, color='#4c8db5'), zorder=8)
ax.text(13.3, RY1-0.85, 'slab slopes away from back wall', fontsize=7.5, color='#4c8db5', va='center', zorder=8)
ax.text(RX1-2.0, RY1-0.12, "counter back = drip edge (+3/8\")", fontsize=7, color=GREY, ha='right', va='bottom')
# dimensions
dim(ax, RX0, RX1, RY1+1.6, "ROOF / SLAB 20'-0\"")
dim(ax, 0, L, RY1+2.5, "16'-0\" post c/c")
dim(ax, h, L-h, RY1+3.4, f"{ftin(L-P)} clear between posts", fs=8)
dim(ax, RY0, RY1, RX0-1.1, "ROOF / SLAB 16'-0\"", horiz=False)
dim(ax, 0, W, RX0-2.1, "12'-0\" post c/c", horiz=False)
dim(ax, h, W-h, RX0-3.0, f"{ftin(W-P)} clear", horiz=False, fs=8)
dim(ax, W, RY1, RX1+1.6, "2'", horiz=False, fs=8); dim(ax, RY0, 0, RX1+1.6, "2'", horiz=False, fs=8)
dim(ax, h, W-h, RX1+2.6, f"kitchen run {ftin(W-P)}", horiz=False, fs=8)
dim(ax, -h, L/2, RY0-1.3, f"panel {ftin(L/2+h)}", fs=7.5, c='#6d6458')
dim(ax, -h, W/2, -3.7, '', horiz=False, fs=7.5, c='#6d6458')
ax.text(-3.85, W/4-0.2, f"panel\n{ftin(W/2+h)}", fontsize=7.5, color='#6d6458', ha='right', va='center')
ax.set_title('Pavilion plan v3  -  16 x 20 roof, posts 12 x 16 c/c, 2\' overhang all around, 11-1/4" posts', fontsize=14, loc='left', pad=12)
ax.set_aspect('equal'); ax.set_xlim(-7.5, 22.5); ax.set_ylim(RY1+4.2, RY0-1.9); ax.axis('off')
fig.text(0.04, 0.035, "Concept only. Saw cuts dashed (about 1\" deep), carried through the border band to the slab edge. "
         "Slab = drip edge. Gutters all 4 sides; downspouts at the back corners. Furniture to scale.", fontsize=9, color=GREY)
fig.savefig(sys.argv[1], dpi=105, bbox_inches='tight', facecolor='white'); print('saved')
