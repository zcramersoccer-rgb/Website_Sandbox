"""Post + entablature concept detail. Doric proportions from Ware, The American Vignola, with D = 11-1/4" post.
Units inches. Elevation (left) and section through the front beam and eave (right)."""
import sys, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch

D = 11.25; h = D/2
INK, GREY, TRIM, TRIM2, STR = '#2b2b2b', '#8a8a8a', '#ffffff', '#f1efe9', '#d9c39b'
PITCH = 4/12

def frac(v):
    w = int(v + 1e-9); f = round((v - w)*16)
    if f == 16: w, f = w+1, 0
    if f == 0: return f'{w}"'
    n, d = f, 16
    while n % 2 == 0: n //= 2; d //= 2
    return f'{w} {n}/{d}"' if w else f'{n}/{d}"'

# vertical stack (inches above slab)
GAP = 0.25                               # HardieTrim min 1/4" off hardscape (HZ10)
PL0, PL1 = GAP, GAP + D/4                # plinth 1/4 D
TO1 = PL1 + 1.9375                       # torus
BA1 = TO1 + 0.75                         # fillet / cincture -> top of base
CAP_TOP = 96.0                           # 8'-0" slab to bottom of beam
AB0 = CAP_TOP - D/6                      # abacus 1/6 D
EC0 = AB0 - D/6                          # echinus 1/6 D
NE0 = EC0 - D/6                          # necking 1/6 D
AS0 = NE0 - 0.75                         # astragal ~1/16 D
ENT = 0.75 + 18.0                        # bottom board + (2) 1-3/4 x 18 LVL: rafters bear on the LVL
A1, A2, TAE = 96 + 2.25, 96 + 2.25 + 2.125, 96 + ENT*2/7          # architrave: 2 fascias + taenia (Tuscan 2:2:3 split)
FR = TAE + ENT*2/7                       # frieze
BED, COR, TOP = FR + 2.0, FR + 6.0, 96 + ENT                        # cornice: bed / corona / cap

def elevation(ax):
    def blk(x0, x1, z0, z1, fc=TRIM, lw=0.9, ec=INK, **k):
        ax.add_patch(Rectangle((x0, z0), x1-x0, z1-z0, fc=fc, ec=ec, lw=lw, **k))
    ax.add_patch(Rectangle((-48, -3), 96, 3, fc='#d6d1c7', ec=INK, lw=0.8))                  # slab
    ax.text(-46, -1.6, 'SLAB (salt / broom border)', fontsize=7, va='center', color='#5f584e')
    blk(-h-D/6, h+D/6, PL0, PL1)                                                           # plinth
    ax.add_patch(FancyBboxPatch((-h-1.25, PL1), D+2.5, TO1-PL1, boxstyle='round,pad=0,rounding_size=0.9', fc=TRIM, ec=INK, lw=0.9))
    blk(-h-0.75, h+0.75, TO1, BA1)
    blk(-h, h, BA1, AS0)                                                                    # shaft
    blk(-h+2.5, h-2.5, BA1+6, AS0-6, fc=TRIM2, lw=0.8)                                      # recessed panel
    blk(-h+2.9, h-2.9, BA1+6.4, AS0-6.4, fc='none', lw=0.4, ec=GREY)
    ax.text(-h-3, (BA1+AS0)/2+10, 'PANELED SHAFT\n(Mt Vernon piers\nare paneled)\n\n3/4" Hardie box\nwrapped to 9 3/4",\n3/4" stiles + rails\napplied -> 11 1/4"\nface, panel 3/4"\nrecessed', ha='right', va='center', fontsize=7.0, color='#555')
    ax.add_patch(FancyBboxPatch((-h-0.75, AS0), D+1.5, 0.75, boxstyle='round,pad=0,rounding_size=0.36', fc=TRIM, ec=INK, lw=0.9))
    blk(-h, h, NE0, EC0)                                                                    # necking
    ec = [(-h, EC0), (h, EC0)] + [(h + 1.4*math.sin(t*math.pi/2), EC0 + (AB0-EC0)*(1-math.cos(t*math.pi/2))) for t in [i/10 for i in range(11)]]
    ec += [(-x, z) for (x, z) in reversed(ec[2:])]
    ax.add_patch(Polygon(ec, closed=True, fc=TRIM, ec=INK, lw=0.9))                         # echinus (routed ovolo)
    blk(-h-D/6, h+D/6, AB0, CAP_TOP)                                                       # abacus
    # entablature (beam runs left-right)
    for (z0, z1, inset) in ((95.75, A1, 0), (A1, A2, -0.6), (A2, TAE, -1.2), (TAE, FR, 0), (FR, BED, -1.4), (BED, COR, -2.6), (COR, TOP, -3.3)):
        blk(-48, 48, z0, z1, fc=TRIM if inset == 0 else '#f7f6f2', lw=0.8)
    blk(-h-D/6, h+D/6, AB0, CAP_TOP)
    # labels right
    lab = [(PL0, PL1, 'plinth 1/4 D'), (PL1, BA1, 'torus + fillet'), (AS0, NE0, 'astragal'), (NE0, EC0, 'necking 1/6 D'),
           (EC0, AB0, 'echinus 1/6 D (routed ovolo)'), (AB0, CAP_TOP, 'abacus 1/6 D, projects 1/6 D'),
           (96, TAE, 'ARCHITRAVE: 2 fascias + taenia'), (TAE, FR, 'FRIEZE (plain)'), (FR, TOP, 'CORNICE: cove bed / corona / ovolo cap')]
    ty = {'astragal': 80.5, 'necking 1/6 D': 84.5, 'echinus 1/6 D (routed ovolo)': 88.5, 'abacus 1/6 D, projects 1/6 D': 92.5,
          'plinth 1/4 D': 2.0, 'torus + fillet': 7.5}
    for z0, z1, t in lab:
        zm = (z0+z1)/2; zt = ty.get(t, zm)
        ax.plot([h+D/6+1, 46, 50], [zm, zt, zt], lw=0.4, color=GREY)
        ax.text(51, zt, f'{t}   {frac(z1-z0)}', fontsize=7.4, va='center')
    # big dims
    def vd(x, z0, z1, t):
        ax.annotate('', (x, z0), (x, z1), arrowprops=dict(arrowstyle='<->', lw=0.8, color=INK, shrinkA=0, shrinkB=0))
        ax.text(x-1, (z0+z1)/2, t, rotation=90, ha='right', va='center', fontsize=8.5, bbox=dict(fc='white', ec='none', pad=0.5))
    vd(-40, 0, 96, "8'-0\"  slab to bottom of beam  (8.5 D)")
    vd(-40, 96, TOP, '18 3/4"')
    vd(-30, 0, BA1, 'base 1/2 D')
    vd(-30, AS0, 96, 'capital 1/2 D')
    ax.text(0, -7, 'ELEVATION', ha='center', fontsize=10, weight='bold')
    ax.set_xlim(-52, 112); ax.set_ylim(-10, 126); ax.set_aspect('equal'); ax.axis('off')

def section(ax):
    def blk(x0, x1, z0, z1, fc=TRIM, lw=0.8, **k):
        ax.add_patch(Rectangle((min(x0, x1), z0), abs(x1-x0), z1-z0, fc=fc, ec=INK, lw=lw, **k))
    # post below (cut), capital outline
    blk(-D, 0, 82, NE0, fc='#f4f2ec')
    ax.add_patch(Rectangle((-D-0.75, AS0), D+1.5, 0.75, fc=TRIM, ec=INK, lw=0.8))
    blk(-D, 0, NE0, EC0)
    ec = [(-D, EC0), (0, EC0)] + [(1.4*math.sin(t*math.pi/2), EC0 + (AB0-EC0)*(1-math.cos(t*math.pi/2))) for t in [i/10 for i in range(11)]]
    ec += [(-D - x, z) for (x, z) in reversed(ec[2:])]
    ax.add_patch(Polygon(ec, closed=True, fc=TRIM, ec=INK, lw=0.8))
    ax.add_patch(Rectangle((-D-D/6, AB0), D+D/3, CAP_TOP-AB0, fc=TRIM, ec=INK, lw=0.8))
    # structure: (2) 1-3/4 x 11-7/8 LVL, rafters bear directly on it; beam furred down to the 18 3/4" face
    blk(-h-1.75, -h+1.75, TOP-11.875, TOP, fc=STR)
    ax.text(-h, TOP-6, '(2) 1 3/4\nx 11 7/8\nLVL', ha='center', va='center', fontsize=6.3)
    blk(-h-1.75, -h+1.75, 96.75, TOP-11.875, fc='#cfe0c4')
    ax.text(-h, (96.75+TOP-11.875)/2, 'PT fur-\ndown', ha='center', va='center', fontsize=6.0)
    for xx in (-D+0.75, -h+1.75): blk(xx, xx + (-h-1.75 - (-D+0.75)), 96.75, TOP, fc='#efe6d4', lw=0.5)
    # trim both faces (mirror)
    for s, x0 in ((1, 0.0), (-1, -D)):
        blk(x0, x0 - s*0.75, 95.75, FR)                                                    # side board w/ 1/4" drip
        blk(x0, x0 + s*0.75, A1, A2); blk(x0, x0 + s*1.5, A2, TAE)
        cove = [(x0, FR), (x0 + s*1.625, FR)] + [(x0 + s*(1.625 - 1.1*math.sin(t*math.pi/2)), FR + 0.2 + 1.1*(1-math.cos(t*math.pi/2))*0) for t in (0,)]
        ax.add_patch(Polygon([(x0, FR), (x0 + s*0.6, FR), (x0 + s*1.625, BED-0.35), (x0 + s*1.625, BED), (x0, BED)], closed=True, fc=TRIM, ec=INK, lw=0.8))
        blk(x0, x0 + s*3.5, BED, COR)
        ax.add_patch(Polygon([(x0, COR), (x0 + s*3.5, COR), (x0 + s*4.25, COR+0.9), (x0 + s*4.25, TOP), (x0, TOP)], closed=True, fc=TRIM, ec=INK, lw=0.8))
    blk(-D+0.75, -0.75, 96, 96.75)                                                         # bottom board
    # rafters: underside passes through (outer face, TOP) at 4:12
    z_us = lambda x: TOP - PITCH*x
    xe = 24 - h                                                                            # eave: 2' from post centre
    depth = 7.25/math.cos(math.atan(PITCH))
    ax.add_patch(Polygon([(-34, z_us(-34)), (xe, z_us(xe)), (xe, z_us(xe)+depth), (-34, z_us(-34)+depth)], closed=True, fc=STR, ec=INK, lw=0.7, alpha=0.6))
    ax.text(-30, z_us(-30)+3.5, '2x8 rafter @ 4:12', fontsize=6.5, rotation=math.degrees(math.atan(PITCH)), va='center')
    # roof deck + shingles
    ax.plot([-34, xe+0.75], [z_us(-34)+depth+0.6, z_us(xe+0.75)+depth+0.6], lw=2.2, color='#4a4a4a')
    # T&G soffit (outside) and ceiling (inside)
    ax.plot([4.25, xe], [z_us(4.25)-0.4, z_us(xe)-0.4], lw=2.4, color='#a8774a')
    ax.plot([-D-4.25, -34], [z_us(-D-4.25)-0.4, z_us(-34)-0.4], lw=2.4, color='#a8774a')
    ax.text(10, z_us(10)-2.2, 'beaded T&G soffit', fontsize=6.5, rotation=-math.degrees(math.atan(PITCH)), color='#7a5232')
    ax.text(-33, z_us(-24)-3.0, 'beaded T&G ceiling', fontsize=6.5, rotation=math.degrees(math.atan(PITCH))*0, color='#7a5232')
    # fascia + gutter
    blk(xe, xe+0.75, z_us(xe)-0.9, z_us(xe)+depth+0.2)
    gx = xe+0.75
    ax.add_patch(Polygon([(gx, z_us(xe)+depth-0.5), (gx+5, z_us(xe)+depth-0.5), (gx+4.5, z_us(xe)+depth-4.5), (gx+0.8, z_us(xe)+depth-4.7)], closed=True, fc='#c9cfd4', ec=INK, lw=0.7))
    ax.text(gx+2.5, z_us(xe)+depth+1.6, 'gutter', fontsize=6.5, ha='center')
    # LED cove on the inside
    ax.add_patch(Rectangle((-D-2.6, TOP), 1.2, 0.7, fc='#ffd76a', ec=INK, lw=0.6))
    for k in range(5):
        ax.plot([-D-2.0, -D-2.0-6-k*3], [TOP+0.7, TOP+5+k*2.5], lw=0.5, color='#e8b93c', alpha=0.8)
    ax.text(-D-8, TOP+1.2, 'LED tape\nbehind cap', fontsize=6.3, ha='right', va='bottom', color='#9a7a20')
    # sightline from a person 15 ft out
    fb = (xe, z_us(xe) - 0.9); ex, ez = 180.0, 66.0
    sl = (fb[1] - ez)/(ex - fb[0]); z0 = fb[1] + sl*fb[0]
    ax.plot([0, 60], [z0, z0 - sl*60], lw=0.8, ls=(0, (5, 3)), color='#4c8db5')
    ax.add_patch(Rectangle((-0.2, z0), 4.6, TOP - z0, fc='#4c8db5', alpha=0.18, ec='none'))
    ax.text(16, 91.5, f"sightline from eye 5'-6\" high, 15' away:\neave hides only the top {frac(TOP - z0)} (the cap);\nfrom inside, the whole entablature shows", fontsize=6.6, color='#2f6f8f', va='top')
    ax.text(-h, 85, 'post', ha='center', fontsize=7, color=GREY)
    ax.text(-33, 86, 'INSIDE', fontsize=9, color=GREY); ax.text(40, 86, 'OUTSIDE', fontsize=9, color=GREY)
    # callouts for the 3 steps + drip
    for (x, z, t) in ((0.4, 95.9, '1/4" drip reveal'), (0.9, (A1+A2)/2, 'step 1: upper fascia +3/4"'), (1.6, (A2+TAE)/2, 'step 2: taenia +1 1/2"'),
                      (1.8, (FR+BED)/2, 'step 3: cornice - routed cove bed mould,'), (3.8, (BED+COR)/2, '5/4 corona,'), (4.4, (COR+TOP)/2, 'routed ovolo cap')):
        ax.plot([x, 27], [z, z], lw=0.4, color=GREY); ax.text(27.5, z, t, fontsize=6.8, va='center')
    ax.text(27.5, (TAE+FR)/2, 'frieze (flush with post face)', fontsize=6.8, va='center'); ax.plot([0.2, 27], [(TAE+FR)/2]*2, lw=0.4, color=GREY)
    ax.text(4, 82.5, 'SECTION THROUGH FRONT BEAM + EAVE  (larger scale)', ha='left', fontsize=10, weight='bold')
    ax.set_xlim(-34, 58); ax.set_ylim(81, 134); ax.set_aspect('equal'); ax.axis('off')

fig, axs = plt.subplots(1, 2, figsize=(19, 10.5), gridspec_kw=dict(width_ratios=[1.0, 1.05], wspace=0.03))
elevation(axs[0]); section(axs[1])
fig.suptitle('Post + entablature concept v2  -  Doric column proportions (Ware), entablature 18 3/4" (~1/5 column, Tuscan split) = 2-ply LVL + fur-down, HardieTrim',
             fontsize=12.5, x=0.01, ha='left', y=0.98)
fig.text(0.01, 0.02, 'Concept only. LVL, uplift hardware and post core by the engineer. Hardie trim held 1/4" off the slab (HardieTrim HZ10). '
         'Routed profiles: ovolo, cove, roundover only; prime every cut edge.', fontsize=8.5, color=GREY)
fig.savefig(sys.argv[1], dpi=105, bbox_inches='tight', facecolor='white'); print('saved')
