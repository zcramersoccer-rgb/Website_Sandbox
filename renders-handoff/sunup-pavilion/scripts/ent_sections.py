import sys, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
B, T = 96.0, 114.75
ENTS = {
 'A': ([(0, B-0.25), (0, B+5.375), (1.0, B+5.375), (1.0, B+7.875), (0, B+7.875)],
       [(0, T-8.0), (1.75, T-8.0), (1.75, T-4.5), (3.0, T-3.25), (3.0, T-2.0), (0, T-2.0)]),
 'B': ([(0, B-0.25), (0, B+2.75), (0.75, B+2.75), (0.75, B+5.375), (0, B+5.375)],
       [(0, B+10.75), (0.5, B+10.75), (1.5, B+11.75), (1.5, B+12.75), (3.0, B+12.75), (3.0, B+15.75), (3.5, B+15.75), (3.5, B+16.75), (0, B+16.75)]),
 'C': ([(0, B-0.25), (0.75, B-0.25), (0.75, B+5.375), (0, B+5.375)],
       [(0, B+11.0), (0.75, B+11.0), (2.0, B+12.25), (2.0, B+16.75), (0, B+16.75)]),
}
T_ = {'A': 'A  current\nfillet + band + cap', 'B': 'B  classical\n2-step architrave / plain frieze / cornice', 'C': 'C  simple\nthick architrave band / plain frieze / crown band'}
fig, axs = plt.subplots(1, 3, figsize=(15, 7.2))
for ax, k in zip(axs, 'ABC'):
    arch, corn = ENTS[k]
    pts = [(-4, B-0.25)] + arch + corn + [(0, T), (-4, T)]
    ax.add_patch(Polygon(pts, closed=True, fc='white', ec='#222', lw=1.4))
    ax.add_patch(Rectangle((-4, 84), 4, B - 84 - 0.25 - 0.0, fc='#f1efe9', ec='#222', lw=1.0))          # post below
    ax.add_patch(Polygon([(-4, 94), (1.875, 94), (1.875, 95.6), (1.4, 96), (-4, 96)], closed=True, fc='white', ec='#222', lw=1.0))
    ax.add_patch(Rectangle((-4, 90.5), 4.75, 3.5, fc='white', ec='#222', lw=1.0))
    xs = [0, 20]; ax.plot(xs, [T - 0.75 - x/3 for x in xs], color='#a8774a', lw=3)                     # soffit underside
    ax.text(8, T - 0.75 - 8/3 + 0.6, 'T&G soffit (4:12)', color='#7a5232', fontsize=9, rotation=-18.4)
    for a_, b_ in zip(pts, pts[1:]):
        pass
    ax.set_title(T_[k], fontsize=12, loc='left')
    ax.set_xlim(-5, 14); ax.set_ylim(84, 118); ax.set_aspect('equal'); ax.axis('off')
    ax.text(-4.6, 97, 'post / beam face', rotation=90, fontsize=8, color='#777')
fig.suptitle('Entablature profiles in section (outside face), true scale. Beam face 18 3/4" over an 11 1/4" post.', fontsize=12, x=0.01, ha='left')
fig.savefig(sys.argv[1], dpi=110, bbox_inches='tight', facecolor='white')
