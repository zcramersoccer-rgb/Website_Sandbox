"""Simplified post + entablature: flat HardieTrim stock widths only, table-saw bevels instead of router profiles.
Units inches. Elevation (left) + section through the front beam (right)."""
import sys, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

D = 11.25; h = D/2
INK, GREY, TRIM, STR = '#2b2b2b', '#8a8a8a', '#ffffff', '#d9c39b'
PITCH = 4/12
GAP = 0.25                                   # HardieTrim 1/4" off the slab
# base: one 5/4 x 5-1/2 band, top edge bevelled
B0, B1 = GAP, GAP + 5.5
# capital: 4/4 x 3-1/2 neck band + abacus of (2) 5/4 x 1-7/8 layers (bevelled top)
N0, N1 = 96 - 5.5, 96 - 2.0
AB0 = N1
# entablature 18-3/4": flat wrap, one 4/4 x 1-1/2 fillet, 5/4 x 3-1/2 band, 5/4 x 2-1/2 cap
TOP = 96 + 18.75
FIL0, FIL1 = 96 + 5.375, 96 + 5.375 + 2.5
BAND0, BAND1 = TOP - 6.0, TOP - 2.5
CAP0 = BAND1

def r(ax, x0, x1, z0, z1, fc=TRIM, lw=0.9, **k):
    ax.add_patch(Rectangle((min(x0, x1), z0), abs(x1-x0), z1-z0, fc=fc, ec=INK, lw=lw, **k))

def elevation(ax):
    ax.add_patch(Rectangle((-48, -3), 96, 3, fc='#d6d1c7', ec=INK, lw=0.8))
    ax.add_patch(Polygon([(-h-1, B0), (h+1, B0), (h+1, B1-0.75), (h+0.25, B1), (-h-0.25, B1), (-h-1, B1-0.75)], closed=True, fc=TRIM, ec=INK, lw=0.9))
    r(ax, -h, h, B1, N0)
    r(ax, -h+2.5, h-2.5, B1+6, N0-6, fc='#f6f5f1', lw=0.6, ls=(0, (4, 2)))
    ax.text(0, (B1+N0)/2, 'plain shaft\n5/4 HardieTrim\n(2) 1x12 + (2) 1x10\n\n- - - panel outline:\noptional 2 1/2 batten\nflat strip frame', ha='center', va='center', fontsize=7.2, color='#555')
    r(ax, -h-0.75, h+0.75, N0, N1)
    ax.add_patch(Polygon([(-h-1.875, AB0), (h+1.875, AB0), (h+1.875, 95.6), (h+1.4, 96), (-h-1.4, 96), (-h-1.875, 95.6)], closed=True, fc=TRIM, ec=INK, lw=0.9))
    r(ax, -48, 48, 95.75, TOP, lw=0.8)
    r(ax, -48, 48, FIL0, FIL1, lw=0.8)
    r(ax, -48, 48, BAND0, BAND1, lw=0.8)
    ax.add_patch(Polygon([(-48, CAP0), (48, CAP0), (48, TOP), (-48, TOP)], closed=True, fc=TRIM, ec=INK, lw=0.8))
    ax.add_patch(Polygon([(-h-1.875, AB0), (h+1.875, AB0), (h+1.875, 95.6), (h+1.4, 96), (-h-1.4, 96), (-h-1.875, 95.6)], closed=True, fc=TRIM, ec=INK, lw=0.9))
    lab = [(B0, B1, 'BASE: (1) 5/4 x 5 1/2 band, bevelled top', 2.5), (N0, N1, 'CAPITAL: 4/4 x 3 1/2 neck band', 89),
           (AB0, 96, '+ abacus, (2) 5/4 layers, bevelled top', 94), (96, FIL0, 'beam wrap: flat 3/4" Hardie, 1/4" drip', 99),
           (FIL0, FIL1, 'fillet 4/4 x 2 1/2 batten  (step 1)', 103), (FIL1, BAND0, 'frieze (flat wrap)', 106.5),
           (BAND0, BAND1, 'band 5/4 x 3 1/2  (step 2)', 110.5), (CAP0, TOP, 'cap 5/4 x 2 1/2, bevelled under (step 3)', 114.5)]
    for z0, z1, t, zt in lab:
        zm = (z0+z1)/2
        ax.plot([h+3, 46, 50], [zm, zt, zt], lw=0.4, color=GREY)
        ax.text(51, zt, t, fontsize=7.4, va='center')
    def vd(x, z0, z1, t):
        ax.annotate('', (x, z0), (x, z1), arrowprops=dict(arrowstyle='<->', lw=0.8, color=INK, shrinkA=0, shrinkB=0))
        ax.text(x-1, (z0+z1)/2, t, rotation=90, ha='right', va='center', fontsize=8.5, bbox=dict(fc='white', ec='none', pad=0.5))
    vd(-40, 0, 96, "8'-0\"  slab to bottom of beam")
    vd(-40, 96, TOP, '18 3/4"')
    ax.text(0, -7, 'ELEVATION - SIMPLIFIED', ha='center', fontsize=10, weight='bold')
    ax.set_xlim(-52, 112); ax.set_ylim(-10, 122); ax.set_aspect('equal'); ax.axis('off')

def section(ax):
    r(ax, -D, 0, 84, N0, fc='#f4f2ec')
    r(ax, -D-0.75, 0.75, N0, N1)
    ax.add_patch(Polygon([(-D-1.875, AB0), (1.875, AB0), (1.875, 95.6), (1.4, 96), (-D-1.4, 96), (-D-1.875, 95.6)], closed=True, fc=TRIM, ec=INK, lw=0.8))
    r(ax, -h-1.75, -h+1.75, TOP-11.875, TOP, fc=STR)
    ax.text(-h, TOP-6, '(2) 1 3/4\nx 11 7/8\nLVL', ha='center', va='center', fontsize=6.3)
    r(ax, -h-1.75, -h+1.75, 96.75, TOP-11.875, fc='#cfe0c4')
    ax.text(-h, (96.75+TOP-11.875)/2, 'PT fur-\ndown', ha='center', va='center', fontsize=6.0)
    for s, x0 in ((1, 0.0), (-1, -D)):
        r(ax, x0, x0 - s*0.75, 95.75, BAND0)
        r(ax, x0, x0 + s*0.75, FIL0, FIL1)
        r(ax, x0 - s*0.75 + s*0.75, x0 + s*1.0, BAND0, BAND1)
        ax.add_patch(Polygon([(x0 - s*0.75, CAP0), (x0 + s*1.0, CAP0), (x0 + s*2.0, CAP0+1.0), (x0 + s*2.0, TOP), (x0 - s*0.75, TOP)], closed=True, fc=TRIM, ec=INK, lw=0.8))
    r(ax, -D+0.75, -0.75, 96, 96.75)
    z_us = lambda x: TOP - PITCH*x
    xe = 24 - h; depth = 7.25/math.cos(math.atan(PITCH))
    ax.add_patch(Polygon([(-30, z_us(-30)), (xe, z_us(xe)), (xe, z_us(xe)+depth), (-30, z_us(-30)+depth)], closed=True, fc=STR, ec=INK, lw=0.7, alpha=0.6))
    ax.plot([-30, xe+0.75], [z_us(-30)+depth+0.6, z_us(xe+0.75)+depth+0.6], lw=2.2, color='#4a4a4a')
    ax.plot([2.0, xe], [z_us(2.0)-0.4, z_us(xe)-0.4], lw=2.4, color='#a8774a')
    ax.plot([-D-2.0, -30], [z_us(-D-2.0)-0.4, z_us(-30)-0.4], lw=2.4, color='#a8774a')
    r(ax, xe, xe+0.75, z_us(xe)-0.9, z_us(xe)+depth+0.2)
    gx, gz = xe+0.75, z_us(xe)+depth-0.6
    th = [math.pi + k*math.pi/12 for k in range(13)]
    ax.add_patch(Polygon([(gx + 2.75 + 2.75*math.cos(t), gz + 2.75*math.sin(t)) for t in th], closed=True, fc='white', ec=INK, lw=0.8))
    ax.text(gx+2.75, gz+1.3, 'half-round\ngutter, white', fontsize=6.5, ha='center', va='bottom')
    ax.add_patch(Rectangle((-D-2.2, TOP), 1.2, 0.7, fc='#ffd76a', ec=INK, lw=0.6))
    for k in range(5):
        ax.plot([-D-1.6, -D-1.6-5-k*3], [TOP+0.7, TOP+4.5+k*2.4], lw=0.5, color='#e8b93c', alpha=0.8)
    ax.text(-D-7, TOP+0.6, 'LED tape\nbehind cap', fontsize=6.3, ha='right', va='bottom', color='#9a7a20')
    for (x, z, t) in ((0.4, 95.9, '1/4" drip reveal'), (0.9, (FIL0+FIL1)/2, 'step 1: flat fillet'), (1.1, (BAND0+BAND1)/2, 'step 2: flat band'),
                      (2.1, (CAP0+TOP)/2, 'step 3: cap, bevelled underside'), (2.0, (N0+N1)/2, 'neck band'), (2.0, (AB0+96)/2, 'abacus, bevelled top')):
        ax.plot([x, 26], [z, z], lw=0.4, color=GREY); ax.text(26.5, z, t, fontsize=6.8, va='center')
    ax.text(-h, 86, 'post', ha='center', fontsize=7, color=GREY)
    ax.text(-30, 86, 'INSIDE', fontsize=9, color=GREY); ax.text(38, 86, 'OUTSIDE', fontsize=9, color=GREY)
    ax.text(-4, 81.5, 'SECTION THROUGH FRONT BEAM (larger scale)', ha='left', fontsize=10, weight='bold')
    ax.set_xlim(-32, 52); ax.set_ylim(80, 130); ax.set_aspect('equal'); ax.axis('off')

fig, axs = plt.subplots(1, 2, figsize=(19, 10.2), gridspec_kw=dict(width_ratios=[1.0, 1.05], wspace=0.03))
elevation(axs[0]); section(axs[1])
fig.suptitle('Post + entablature - SIMPLIFIED: stock-width flat HardieTrim, table-saw bevels, no router profiles. Same 18 3/4" beam face, same proportions.',
             fontsize=12.5, x=0.01, ha='left', y=0.98)
fig.text(0.01, 0.02, 'Concept only. Stock HardieTrim widths (2 1/2 batten, 3 1/2, 5 1/2, 9 1/4, 11 1/4); the only rip is the abacus. Bevels: table saw. '
         'Prime every cut edge. Trim held 1/4" off the slab.', fontsize=8.5, color=GREY)
fig.savefig(sys.argv[1], dpi=105, bbox_inches='tight', facecolor='white'); print('saved')
