# 116 Sun Up Way - hip-roof pavilion with outdoor kitchen (Luxurious Renovations). Design-review model.
# Blender 4.2+:  blender -b -P build_pavilion.py   -> builds sunup-pavilion.blend next to this file
# Inches internally converted to metres. Plan: posts 12 x 16 ft on centre (11-1/4" sq), 16 x 20 roof (2 ft overhang),
# 4:12 hip, back wall on the long side (+Y = north-east), kitchen at +X end, open front toward -Y (south-west).
import bpy, bmesh, os, sys, math, random
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, 'textures')
IN = 0.0254
def v(x, y, z): return Vector((x*IN, y*IN, z*IN))

# ---------------------------------------------------------------- key dimensions (inches)
PX, PY = 96.0, 72.0                  # post centre lines: x = +-96, y = +-72 (back row +72)
P = 11.25; PH = P/2                  # post / beam width
OX, OY = PX + PH, PY + PH            # beam outer-face rectangle half sizes (101.625, 77.625)
IX, IY = PX - PH, PY - PH            # beam inner faces (90.375, 66.375)
RX, RY = 120.0, 96.0                 # roof edge (fascia face) half sizes - 2 ft overhang
BEAM_BOT, BEAM_TOP = 96.0, 96.0 + 18.75
PITCH = 4/12
TG = 0.75                            # T&G thickness
ROOF_T = 8.4                         # rafter (2x8 plumb) + sheathing + shingle above rafter underside
HOUSE_BLUE = (0.40, 0.61, 0.64)   # house light aqua from the yard photos, about sRGB #A0CED6 (linear RGB)
STAIN = tuple(float(x) for x in os.environ.get('PAV_STAIN', '0.44,0.27,0.14').split(','))   # stain A: light honey-neutral on pine (linear) - client pick

def U(s): return BEAM_TOP + s*PITCH                          # rafter underside, s = inches inside the beam outer face

# ---------------------------------------------------------------- reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene; scn.name = 'Pavilion'
colls = {}
def coll(name):
    if name not in colls:
        c = bpy.data.collections.new(name); scn.collection.children.link(c); colls[name] = c
    return colls[name]
def mesh_obj(name, bm, mat, cname, smooth=False, bevel=None, mats=None):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = smooth
    for m in (mats or [mat]):
        if m: me.materials.append(m)
    ob = bpy.data.objects.new(name, me); coll(cname).objects.link(ob)
    if bevel:
        bv = ob.modifiers.new('Bevel', 'BEVEL'); bv.width = bevel*IN; bv.segments = 2
        bv.limit_method = 'ANGLE'; bv.angle_limit = math.radians(40)
    return ob
def box(bm, x0, x1, y0, y1, z0, z1):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    M = Matrix.Translation(v((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)) @ Matrix.Diagonal(((x1-x0)*IN, (y1-y0)*IN, (z1-z0)*IN, 1))
    bmesh.ops.create_cube(bm, size=1.0, matrix=M)
def cyl(bm, x, y, z, r, depth, axis='Z', segs=24, r2=None):
    R = {'Z': Matrix.Identity(4), 'Y': Matrix.Rotation(math.pi/2, 4, 'X'), 'X': Matrix.Rotation(math.pi/2, 4, 'Y')}[axis]
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r*IN, radius2=(r if r2 is None else r2)*IN, depth=depth*IN,
                          matrix=Matrix.Translation(v(x, y, z)) @ R)
def loft_ring(bm, cx, cy, hx, hy, prof):
    """mitred rectangular ring: each (d, z) of the closed profile becomes a rectangle offset d (outward +) at height z"""
    loops = []
    for d, z in prof:
        ax, ay = hx + d, hy + d
        loops.append([bm.verts.new(v(cx + sx*ax, cy + sy*ay, z)) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))])
    for i in range(len(loops)):
        a, b = loops[i], loops[(i+1) % len(loops)]
        for k in range(4):
            bm.faces.new((a[k], a[(k+1) % 4], b[(k+1) % 4], b[k]))
def bar(bm, p0, p1, w, hb, ht, hb1=None):
    """box along segment p0->p1 (inches): width w horizontal-perpendicular, from hb below to ht above the line"""
    p0, p1 = Vector(p0), Vector(p1); d = (p1 - p0).normalized()
    side = d.cross(Vector((0, 0, 1)))
    side = Vector((1, 0, 0)) if side.length < 1e-6 else side.normalized(); up = side.cross(d).normalized()
    pts = []
    for a, hbx in ((p0, hb), (p1, hb if hb1 is None else hb1)):
        for sw in (-w/2, w/2):
            for sh in (-hbx, ht):
                pts.append(bm.verts.new((a + side*sw + up*sh)*IN))
    f = lambda i, j, k, l: bm.faces.new((pts[i], pts[j], pts[k], pts[l]))
    f(0, 1, 3, 2); f(4, 6, 7, 5); f(0, 4, 5, 1); f(2, 3, 7, 6); f(0, 2, 6, 4); f(1, 5, 7, 3)

def hip_tail(bm, sx, sy, w=4.5, drop0=3.0, drop1=3.0, top=0.5):
    """soffit hip trim from the beam's outer corner into the fascia's inside corner. The end is cut as a V so each side
    stops on a fascia face (nothing passes through the fascia); the drop tapers to finish flush with the fascia bottom."""
    fx, fy = sx*(RX - 0.75), sy*(RY - 0.75)                    # inside corner of the fascia
    p0 = Vector((sx*OX, sy*OY)); C = Vector((fx, fy)); L = (C - p0).length; d = (C - p0)/L
    side = Vector((d.y, -d.x))
    def zc(t): return U(-(t/math.sqrt(2))) - TG              # crease height t inches along the hip (plan)
    def drop(t): return drop0 + (drop1 - drop0)*t/L
    def edge_end(off):                                      # where an edge offset `off` hits a fascia face
        o = p0 + side*off; ts = []
        if abs(d.x) > 1e-9: ts.append((fx - o.x)/d.x)
        if abs(d.y) > 1e-9: ts.append((fy - o.y)/d.y)
        return min(t for t in ts if t > 0)
    def vv(pxy, t, h): return bm.verts.new(v(pxy.x, pxy.y, zc(t) + h))
    pts = {}
    for name, off in (('l', w/2), ('r', -w/2)):
        o = p0 + side*off; te = edge_end(off)
        pts[name] = [vv(o, 0, -drop0), vv(o, 0, top), vv(o + d*te, te, -drop(te)), vv(o + d*te, te, top)]
    cb, ct = vv(C, L, -drop1), vv(C, L, top)
    lb0, lt0, lb1, lt1 = pts['l']; rb0, rt0, rb1, rt1 = pts['r']
    for f in ((lb0, rb0, rt0, lt0), (lb0, lt0, lt1, lb1), (rb0, rb1, rt1, rt0),
              (lb0, lb1, cb, rb1, rb0), (lt0, rt0, rt1, ct, lt1), (lb1, lt1, ct, cb), (cb, ct, rt1, rb1)):
        bm.faces.new(f)

# ---------------------------------------------------------------- material helpers
class NT:
    def __init__(s, m):
        m.use_nodes = True; s.nt = m.node_tree; s.N = s.nt.nodes; s.L = s.nt.links
        s.N.clear(); s.out = s.N.new('ShaderNodeOutputMaterial'); s.b = s.N.new('ShaderNodeBsdfPrincipled')
        s.L.new(s.b.outputs[0], s.out.inputs['Surface'])
    def set(s, sock, val):
        if hasattr(val, 'is_output'): s.L.new(val, sock)
        else: sock.default_value = val
    def node(s, t, **kw):
        n = s.N.new(t)
        for k, val in kw.items():
            if k.startswith('i_'): s.set(n.inputs[k[2:].replace('_', ' ')], val)
            else: setattr(n, k, val)
        return n
    def math(s, op, a, b=0.0):
        n = s.N.new('ShaderNodeMath'); n.operation = op; s.set(n.inputs[0], a); s.set(n.inputs[1], b); return n.outputs[0]
    def vmath(s, op, a, b=(0, 0, 0)):
        n = s.N.new('ShaderNodeVectorMath'); n.operation = op; s.set(n.inputs[0], a); s.set(n.inputs[1], b); return n.outputs[0]
    def mapr(s, x, a, b, c, d, interp='LINEAR'):
        n = s.N.new('ShaderNodeMapRange'); n.interpolation_type = interp; n.clamp = True; s.set(n.inputs['Value'], x)
        for i, val in zip(('From Min', 'From Max', 'To Min', 'To Max'), (a, b, c, d)): n.inputs[i].default_value = val
        return n.outputs['Result']
    def mix(s, a, b, fac, mode='MIX'):
        n = s.N.new('ShaderNodeMix'); n.data_type = 'RGBA'; n.blend_type = mode
        s.set(n.inputs[0], fac); s.set(n.inputs[6], a); s.set(n.inputs[7], b); return n.outputs[2]
    def co(s, scale=1.0, kind='Object'):
        tc = s.N.new('ShaderNodeTexCoord'); mp = s.N.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (scale, scale, scale) if isinstance(scale, (int, float)) else scale
        s.L.new(tc.outputs[kind], mp.inputs['Vector']); return mp.outputs[0]
    def img(s, name, vec, color=True, blend=0.3):
        t = s.N.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(os.path.join(TEX, name), check_existing=True)
        if not color: t.image.colorspace_settings.name = 'Non-Color'
        t.projection = 'BOX'; t.projection_blend = blend; s.L.new(vec, t.inputs['Vector']); return t
    def bump(s, h, strength, dist, normal=None):
        bp = s.node('ShaderNodeBump', i_Strength=strength, i_Distance=dist); s.L.new(h, bp.inputs['Height'])
        if normal is not None: s.L.new(normal, bp.inputs['Normal'])
        s.L.new(bp.outputs[0], s.b.inputs['Normal']); return bp

def simple(name, color, rough, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name); t = NT(m)
    t.b.inputs['Base Color'].default_value = (*color, 1); t.b.inputs['Roughness'].default_value = rough
    t.b.inputs['Metallic'].default_value = metal; t.b.inputs['Coat Weight'].default_value = coat
    return m, t

def mat_paint(name, color, rough=0.42):
    """satin exterior paint on fiber cement: faint sanded texture"""
    m, t = simple(name, color, rough)
    n = t.node('ShaderNodeTexNoise', i_Scale=900.0, i_Detail=4.0); t.L.new(t.co(1.0), n.inputs['Vector'])
    t.bump(n.outputs['Fac'], 0.04, 0.0003)
    return m
def mat_lime():
    m = bpy.data.materials.new('Lime plaster - island + hood'); t = NT(m); vec = t.co(1.1)
    c = t.img('Plaster006_2K-JPG_Color.jpg', vec); bw = t.node('ShaderNodeRGBToBW'); t.L.new(c.outputs['Color'], bw.inputs[0])
    tone = t.mapr(bw.outputs[0], 0.2, 0.8, 0.88, 1.06)
    cl = t.node('ShaderNodeTexNoise', i_Scale=2.0, i_Detail=6.0, i_Roughness=0.6); t.L.new(t.co(1.0), cl.inputs['Vector'])
    col = t.mix((0.80, 0.75, 0.66, 1), tone, 1.0, 'MULTIPLY')
    col = t.mix(col, t.mapr(cl.outputs['Fac'], 0.3, 0.7, 0.94, 1.04), 1.0, 'MULTIPLY')
    t.set(t.b.inputs['Base Color'], col); t.b.inputs['Roughness'].default_value = 0.86
    nm = t.node('ShaderNodeNormalMap', i_Strength=0.35); t.L.new(t.img('Plaster006_2K-JPG_NormalGL.jpg', vec, False).outputs['Color'], nm.inputs['Color'])
    t.L.new(nm.outputs[0], t.b.inputs['Normal']); return m
def mat_pine():
    """beaded 1x6 pine T&G, medium-light stain. UV: u along the boards, v across (inches)"""
    m = bpy.data.materials.new('Beaded pine T&G - stained'); t = NT(m)
    uv = t.N.new('ShaderNodeUVMap')
    sep = t.node('ShaderNodeSeparateXYZ'); t.L.new(uv.outputs[0], sep.inputs[0])
    vb = t.math('DIVIDE', sep.outputs['Y'], 5.125)                    # board index (5-1/8" face)
    idx = t.math('FLOOR', vb); fr = t.math('FRACT', vb)
    rnd = t.node('ShaderNodeTexWhiteNoise', noise_dimensions='1D'); t.L.new(idx, rnd.inputs['W'])
    # grain: stretched noise along u, offset per board
    gv = t.node('ShaderNodeCombineXYZ'); t.L.new(t.math('MULTIPLY', sep.outputs['X'], 0.04), gv.inputs['X'])
    t.L.new(t.math('ADD', t.math('MULTIPLY', sep.outputs['Y'], 1.2), t.math('MULTIPLY', rnd.outputs['Value'], 50.0)), gv.inputs['Y'])
    t.L.new(rnd.outputs['Value'], gv.inputs['Z'])
    gr = t.node('ShaderNodeTexNoise', i_Scale=1.0, i_Detail=8.0, i_Roughness=0.65, i_Distortion=0.6); t.L.new(gv.outputs[0], gr.inputs['Vector'])
    wave = t.node('ShaderNodeTexWave', wave_type='BANDS', bands_direction='Y', i_Scale=0.35, i_Distortion=6.0, i_Detail=4.0)
    t.L.new(gv.outputs[0], wave.inputs['Vector'])
    grain = t.math('ADD', t.math('MULTIPLY', gr.outputs['Fac'], 0.6), t.math('MULTIPLY', wave.outputs['Fac'], 0.4))
    tone = t.mapr(grain, 0.25, 0.75, 0.78, 1.12)
    board = t.mapr(rnd.outputs['Value'], 0, 1, 0.86, 1.12)
    col = t.mix((*STAIN, 1), t.math('MULTIPLY', tone, board), 1.0, 'MULTIPLY')
    # seam groove (at board edge) and bead (mid board)
    seam = t.math('MAXIMUM', t.mapr(fr, 0.0, 0.025, 1.0, 0.0), t.mapr(fr, 0.975, 1.0, 0.0, 1.0))
    bead = t.mapr(t.math('ABSOLUTE', t.math('SUBTRACT', fr, 0.5)), 0.0, 0.025, 1.0, 0.0)
    col = t.mix(col, (0.03, 0.017, 0.008, 1), t.math('MULTIPLY', seam, 0.85))
    col = t.mix(col, (0.10, 0.055, 0.025, 1), t.math('MULTIPLY', bead, 0.35))
    t.set(t.b.inputs['Base Color'], col); t.b.inputs['Roughness'].default_value = 0.55
    h = t.math('SUBTRACT', t.math('MULTIPLY', grain, 0.15), t.math('ADD', seam, t.math('MULTIPLY', bead, 0.5)))
    t.bump(h, 0.35, 0.002); return m
def mat_shingle():
    """architectural (laminated) shingles: staggered random-width tabs, charcoal blend. UV as the ceiling."""
    m = bpy.data.materials.new('Architectural shingles'); t = NT(m)
    uv = t.N.new('ShaderNodeUVMap'); sep = t.node('ShaderNodeSeparateXYZ'); t.L.new(uv.outputs[0], sep.inputs[0])
    row = t.math('FLOOR', t.math('DIVIDE', sep.outputs['Y'], 5.625)); fr = t.math('FRACT', t.math('DIVIDE', sep.outputs['Y'], 5.625))
    rr = t.node('ShaderNodeTexWhiteNoise', noise_dimensions='1D'); t.L.new(row, rr.inputs['W'])
    xs = t.math('ADD', sep.outputs['X'], t.math('MULTIPLY', rr.outputs['Value'], 40.0))
    vor = t.node('ShaderNodeTexVoronoi', voronoi_dimensions='1D', i_Scale=0.12, i_Randomness=0.9); t.L.new(xs, vor.inputs['W'])
    cv = t.node('ShaderNodeSeparateColor'); t.L.new(vor.outputs['Color'], cv.inputs[0])
    tab = t.math('ADD', cv.outputs[0], t.math('MULTIPLY', rr.outputs['Value'], 0.3))
    base = t.mix((0.022, 0.022, 0.024, 1), (0.055, 0.053, 0.050, 1), t.mapr(tab, 0.2, 1.1, 0.0, 1.0))      # charcoal blend like the house roof
    gran = t.node('ShaderNodeTexNoise', i_Scale=40.0, i_Detail=2.0); t.L.new(uv.outputs[0], gran.inputs['Vector'])
    col = t.mix(base, t.mapr(gran.outputs['Fac'], 0.3, 0.7, 0.85, 1.15), 1.0, 'MULTIPLY')
    shadow = t.mapr(fr, 0.0, 0.12, 0.45, 1.0)
    col = t.mix(col, shadow, 1.0, 'MULTIPLY')
    t.set(t.b.inputs['Base Color'], col); t.b.inputs['Roughness'].default_value = 0.85
    t.bump(t.math('ADD', fr, t.math('MULTIPLY', gran.outputs['Fac'], 0.2)), 0.3, 0.004); return m
def mat_slab(broom):
    m = bpy.data.materials.new('Concrete - ' + ('broom border' if broom else 'salt finish')); t = NT(m); vec = t.co(1.0)
    c = t.img('Concrete034_2K-JPG_Color.jpg', vec); bw = t.node('ShaderNodeRGBToBW'); t.L.new(c.outputs['Color'], bw.inputs[0])
    col = t.mix((0.50, 0.48, 0.44, 1), t.mapr(bw.outputs[0], 0.2, 0.8, 0.9, 1.08), 1.0, 'MULTIPLY')
    if broom:
        st = t.node('ShaderNodeTexNoise', i_Scale=1.0, i_Detail=6.0); t.L.new(t.co((60.0, 1.5, 60.0)), st.inputs['Vector'])
        h = st.outputs['Fac']; col = t.mix(col, t.mapr(h, 0.3, 0.7, 0.92, 1.05), 1.0, 'MULTIPLY'); t.bump(h, 0.25, 0.001)
    else:
        sv = t.node('ShaderNodeTexVoronoi', i_Scale=90.0, i_Randomness=1.0); t.L.new(t.co(1.0), sv.inputs['Vector'])
        sz = t.node('ShaderNodeTexWhiteNoise'); t.L.new(sv.outputs['Position'], sz.inputs['Vector'])
        pit = t.math('MULTIPLY', t.mapr(sv.outputs['Distance'], 0.0, 0.18, 1.0, 0.0), t.math('GREATER_THAN', sz.outputs['Value'], 0.55))
        col = t.mix(col, (0.30, 0.29, 0.27, 1), t.math('MULTIPLY', pit, 0.5))
        t.bump(t.math('MULTIPLY', pit, -1.0), 0.5, 0.002)
    t.set(t.b.inputs['Base Color'], col); t.b.inputs['Roughness'].default_value = 0.8; return m
def mat_granite():
    m, t = simple('Black granite - leathered', (0.018, 0.018, 0.019), 0.5)
    n = t.node('ShaderNodeTexNoise', i_Scale=60.0, i_Detail=6.0, i_Roughness=0.6); t.L.new(t.co(1.0), n.inputs['Vector'])
    sp = t.node('ShaderNodeTexVoronoi', i_Scale=400.0); t.L.new(t.co(1.0), sp.inputs['Vector'])
    t.set(t.b.inputs['Base Color'], t.mix((0.016, 0.016, 0.017, 1), (0.06, 0.06, 0.062, 1), t.mapr(sp.outputs['Distance'], 0.0, 0.08, 0.6, 0.0)))
    t.set(t.b.inputs['Roughness'], t.mapr(n.outputs['Fac'], 0.35, 0.65, 0.32, 0.62))
    t.bump(n.outputs['Fac'], 0.25, 0.0015); return m
def mat_stainless():
    m, t = simple('Brushed stainless', (0.60, 0.60, 0.59), 0.27, 1.0)
    br = t.node('ShaderNodeTexNoise', i_Scale=1.0, i_Detail=4.0); t.L.new(t.co((1.5, 400.0, 400.0)), br.inputs['Vector'])
    t.bump(br.outputs['Fac'], 0.05, 0.0004); return m
def emit(name, color, strength):
    m = bpy.data.materials.new(name); t = NT(m)
    t.b.inputs['Base Color'].default_value = (*color, 1)
    t.b.inputs['Emission Color'].default_value = (*color, 1); t.b.inputs['Emission Strength'].default_value = strength
    return m
def mat_lawn():
    m = bpy.data.materials.new('Lawn'); t = NT(m)
    n = t.node('ShaderNodeTexNoise', i_Scale=0.4, i_Detail=8.0); t.L.new(t.co(1.0), n.inputs['Vector'])
    f = t.node('ShaderNodeTexNoise', i_Scale=300.0, i_Detail=2.0); t.L.new(t.co(1.0), f.inputs['Vector'])
    col = t.mix((0.075, 0.105, 0.035, 1), (0.15, 0.17, 0.06, 1), t.mapr(n.outputs['Fac'], 0.35, 0.65, 0, 1))
    col = t.mix(col, t.mapr(f.outputs['Fac'], 0.3, 0.7, 0.7, 1.2), 1.0, 'MULTIPLY')
    t.set(t.b.inputs['Base Color'], col); t.b.inputs['Roughness'].default_value = 0.95
    t.bump(f.outputs['Fac'], 0.5, 0.01); return m

M_TRIM = mat_paint('Hardie trim - white', (0.80, 0.80, 0.78))
M_SIDING = mat_paint('House aqua (from photos)', HOUSE_BLUE, 0.5)
M_LIME = mat_lime(); M_PINE = mat_pine(); M_SHINGLE = mat_shingle()
M_SALT, M_BROOM = mat_slab(False), mat_slab(True)
M_GRANITE = mat_granite(); M_SS = mat_stainless()
M_GAP, _ = simple('Saw cut / shadow gap', (0.03, 0.03, 0.03), 0.9)
M_TV, _ = simple('TV screen', (0.006, 0.006, 0.007), 0.08, 0.0, 1.0)
M_BLACK, _ = simple('Black satin', (0.02, 0.02, 0.02), 0.4)
M_LANT, _ = simple('Lantern - aged copper', (0.12, 0.07, 0.04), 0.45, 1.0)
M_GLASS = bpy.data.materials.new('Lantern glass'); tg = NT(M_GLASS); tg.b.inputs['Transmission Weight'].default_value = 1.0; tg.b.inputs['Roughness'].default_value = 0.02
M_FLAME = emit('Lantern flame bulb', (1.0, 0.62, 0.28), 40.0)
M_LED = emit('LED tape 2700K', (1.0, 0.72, 0.45), 18.0)
M_CAN = emit('Soffit light lens', (1.0, 0.82, 0.62), 25.0)
M_FABRIC, _ = simple('Sectional fabric - oatmeal', (0.62, 0.58, 0.50), 0.9)
M_PILLOW, _ = simple('Pillow - navy', (0.03, 0.06, 0.14), 0.9)
M_TEAK, _ = simple('Teak', (0.30, 0.17, 0.08), 0.55)
M_RUG, _ = simple('Rug - jute', (0.48, 0.38, 0.24), 0.95)
M_FANBODY, _ = simple('Fan - matte black', (0.018, 0.018, 0.018), 0.45)
M_LAWN = mat_lawn()

# ---------------------------------------------------------------- slab (top at z=0), saw cuts as 1/8" shadow gaps
XL = [-RX, -OX, 0.0, OX, RX]; YL = [-RY, -OY, 0.0, OY, RY]; g = 0.0625
salt, broom = bmesh.new(), bmesh.new()
for i in range(4):
    for j in range(4):
        inner = 1 <= i <= 2 and 1 <= j <= 2
        x0 = XL[i] + (g if i > 0 else 0); x1 = XL[i+1] - (g if i < 3 else 0)
        y0 = YL[j] + (g if j > 0 else 0); y1 = YL[j+1] - (g if j < 3 else 0)
        box(salt if inner else broom, x0, x1, y0, y1, -4.0, 0.0)
mesh_obj('Slab - salt finish', salt, M_SALT, 'Slab', bevel=0.12)
mesh_obj('Slab - broom border', broom, M_BROOM, 'Slab', bevel=0.12)
gp = bmesh.new(); box(gp, -RX+0.1, RX-0.1, -RY+0.1, RY-0.1, -4.0, -1.0); mesh_obj('Slab - saw cut bottoms', gp, M_GAP, 'Slab')
ground = bmesh.new(); bmesh.ops.create_grid(ground, x_segments=1, y_segments=1, size=1200*IN, matrix=Matrix.Translation(v(0, 0, -0.6)))
mesh_obj('Lawn', ground, M_LAWN, 'Site')

BASE_R = 0.75
BASE_PROF = [(-0.05, 0.25), (1.0, 0.25)] + [(0.25 + BASE_R*math.cos(math.radians(a)), 5.75 - BASE_R + BASE_R*math.sin(math.radians(a))) for a in range(0, 91, 15)] + [(-0.05, 5.75)]
# ---------------------------------------------------------------- posts (simplified trim)
for sx in (-1, 1):
    for sy in (-1, 1):
        cx, cy = sx*PX, sy*PY
        bm = bmesh.new()
        box(bm, cx-PH, cx+PH, cy-PH, cy+PH, 5.0, 90.6)                                  # shaft
        loft_ring(bm, cx, cy, PH, PH, BASE_PROF)                                                  # base band
        loft_ring(bm, cx, cy, PH, PH, [(-0.05, 90.5), (0.75, 90.5), (0.75, 94.0), (-0.05, 94.0)])              # neck band
        loft_ring(bm, cx, cy, PH, PH, [(-0.05, 94.0), (1.875, 94.0), (1.875, 95.6), (1.4, 96.0), (-0.05, 96.0)]) # abacus
        mesh_obj(f'Post {"LR"[sx > 0]}{"FB"[sy > 0]}', bm, M_TRIM, 'Structure + trim', bevel=0.06)

# ---------------------------------------------------------------- beam ring with the 3-step trim, both faces
B, T = BEAM_BOT, BEAM_TOP
# outside: fillet +1", band +1-3/4", cap +3" (bevelled under), cap top tucked just under the sloped soffit
# inside: same steps, cap carries a 3/4" lip that hides the LED tape
ENT = os.environ.get('PAV_ENT', 'D')
# outside profiles (d = projection from the post/beam face, z), bottom up. 'arch' ends where the frieze starts;
# 'corn' is the cornice, kept under the sloped soffit outside. Inside, the cornice is raised to the beam top and
# carries a 3/4" lip that hides the LED tape.
ENTS = {
 'A': ([(0, B-0.25), (0, B+5.375), (1.0, B+5.375), (1.0, B+7.875), (0, B+7.875)],                     # current: fillet / band / cap
       [(0, T-8.0), (1.75, T-8.0), (1.75, T-4.5), (3.0, T-3.25), (3.0, T-2.0), (0, T-2.0)]),
 'B': ([(0, B-0.25), (0, B+2.75), (0.75, B+2.75), (0.75, B+5.375), (0, B+5.375)],                     # classical: 2-fascia architrave,
       [(0, B+10.75), (0.5, B+10.75), (1.5, B+11.75), (1.5, B+12.75), (3.0, B+12.75), (3.0, B+15.75),  # plain frieze, bed + corona + cap
        (3.5, B+15.75), (3.5, B+16.75), (0, B+16.75)]),
 'D': ([(0, B-0.25), (0, B+2.75), (0.75, B+2.75), (0.75, B+5.375), (0, B+5.375)],                     # client pick: B's 2-step architrave,
       [(0, B+10.75), (1.75, B+10.75), (1.75, B+14.25), (3.0, B+15.5), (3.0, B+16.75), (0, B+16.75)]),  # plain frieze, A's band + bevelled cap at B's height
 'C': ([(0, B-0.25), (0.75, B-0.25), (0.75, B+5.375), (0, B+5.375)],                                  # simple: thick architrave band,
       [(0, B+11.0), (0.75, B+11.0), (2.0, B+12.25), (2.0, B+16.75), (0, B+16.75)]),                   # plain frieze, one crown band
}
arch, corn = ENTS[ENT]
dc = max(d for d, z in corn); dz = T - corn[-1][1]
outer = arch + corn + [(0, T)]
inner_up = arch + [(d, z + dz) for d, z in corn]
mir = [(-P - d, z) for d, z in reversed(inner_up)]
inner = [(-P - dc + 0.75, T), (-P - dc + 0.75, T + 0.75), (-P - dc, T + 0.75)] + mir[1:]
prof = outer + inner + [(-10.5, B-0.25), (-10.5, B), (-0.75, B), (-0.75, B-0.25)]
bm = bmesh.new(); loft_ring(bm, 0, 0, OX, OY, prof); mesh_obj('Beam ring + entablature', bm, M_TRIM, 'Structure + trim', bevel=0.05)
led = bmesh.new()
loft_ring(led, 0, 0, OX, OY, [(-11.6, T+0.02), (-12.3, T+0.02), (-12.3, T+0.12), (-11.6, T+0.12)])
mesh_obj('LED tape (inside, behind cap)', led, M_LED, 'Lighting')

# ---------------------------------------------------------------- roof: ceiling/soffit surface, shingles, fascia, gutters
def hip_surface(edge_d, dz, name, mat):
    """hip surface over rectangle (OX+edge_d, OY+edge_d); height U(s)+dz; UV u along eave, v up-slope (inches)"""
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    ex, ey = OX + edge_d, OY + edge_d; ze = U(-edge_d) + dz; zr = U(OY) + dz; rx = OX - OY
    c = {'FL': (-ex, -ey, ze), 'FR': (ex, -ey, ze), 'BR': (ex, ey, ze), 'BL': (-ex, ey, ze), 'RR': (rx, 0, zr), 'RL': (-rx, 0, zr)}
    V = {k: bm.verts.new(v(*p)) for k, p in c.items()}
    k_ = math.sqrt(1 + PITCH**2)
    faces = [(('FL', 'FR', 'RR', 'RL'), lambda p: (p[0], (p[1] + ey)*k_)), (('BR', 'BL', 'RL', 'RR'), lambda p: (-p[0], (ey - p[1])*k_)),
             (('BL', 'FL', 'RL'), lambda p: (-p[1], (p[0] + ex)*k_)), (('FR', 'BR', 'RR'), lambda p: (p[1], (ex - p[0])*k_))]
    for keys, fuv in faces:
        f = bm.faces.new([V[k] for k in keys])
        for lp in f.loops:
            p = lp.vert.co / IN; lp[uvl].uv = fuv(p)
    return mesh_obj(name, bm, mat, 'Roof')
ceil = hip_surface(RX - OX - 0.75, -TG, 'Ceiling + soffit - beaded T&G', M_PINE)       # underside of T&G, inside fascia
roof = hip_surface(RX - OX + 1.0, ROOF_T, 'Roof - architectural shingles', M_SHINGLE)
for ob in (ceil, roof):                                                                # give the shingle/ceiling some thickness
    so = ob.modifiers.new('Thickness', 'SOLIDIFY'); so.thickness = (0.5 if ob is roof else TG)*IN; so.offset = 1.0 if ob is roof else -1.0
SOFFIT_HIP_DROP = float(os.environ.get('PAV_SOFFIT_HIP_DROP', '1.0'))   # hip drop under the soffit = fascia drop below the soffit
z_fb = U(-(RX - OX)) - TG - SOFFIT_HIP_DROP
bm = bmesh.new(); loft_ring(bm, 0, 0, RX, RY, [(-0.75, z_fb), (0, z_fb), (0, U(-(RX - OX)) + ROOF_T - 0.1), (-0.75, U(-(RX - OX)) + ROOF_T - 0.1)])
mesh_obj('Fascia - Hardie 1x10', bm, M_TRIM, 'Roof', bevel=0.05)
FT = U(-(RX - OX)) + ROOF_T - 0.1
bm = bmesh.new(); loft_ring(bm, 0, 0, RX, RY, [(-0.05, FT - 3.5), (0.75, FT - 3.5), (0.75, FT), (-0.05, FT)])
mesh_obj('Fascia cap 1x4 (behind gutter)', bm, M_TRIM, 'Roof', bevel=0.05)
# half-round 6" gutter, white, all four sides
zg = U(-(RX - OX)) + ROOF_T - 1.2; arc = []
for k in range(13):
    a = math.pi + k*math.pi/12; arc.append((3.85 + 3.0*math.cos(a), zg + 3.0*math.sin(a)))
inner = [(3.85 + 2.85*math.cos(math.pi + k*math.pi/12), zg + 2.85*math.sin(math.pi + k*math.pi/12)) for k in range(12, -1, -1)]
bm = bmesh.new(); loft_ring(bm, 0, 0, RX, RY, arc + inner); mesh_obj('Gutter - 6in half-round', bm, M_TRIM, 'Roof', smooth=True)
# copper cup rain chains from the gutter outlets (back corners + front corner past the kitchen) into stone basins
M_COPPER, _ = simple('Rain chain - copper', (0.55, 0.28, 0.14), 0.35, 1.0)
M_STONE, _ = simple('Basin stone', (0.32, 0.30, 0.27), 0.8)
M_GRAVEL, _ = simple('River rock', (0.25, 0.23, 0.20), 0.9)
ch, bs, gv = bmesh.new(), bmesh.new(), bmesh.new()
for (x, y) in ((-(RX - 9), RY + 3.85), (RX - 9, RY + 3.85), (RX - 9, -(RY + 3.85))):
    z = zg - 3.2
    while z > 9.0:
        cyl(ch, x, y, z - 1.5, 1.4, 3.0, segs=12, r2=0.55); cyl(ch, x, y, z - 3.4, 0.12, 0.9, segs=6); z -= 4.0
    cyl(bs, x, y, 2.5, 9.0, 7.0, segs=32, r2=10.5)
    cyl(gv, x, y + (6 if y > 0 else -6), -0.3, 22.0, 0.8, segs=28)
mesh_obj('Rain chains - copper cups', ch, M_COPPER, 'Roof', smooth=True)
mesh_obj('Rain chain basins', bs, M_STONE, 'Roof', bevel=0.4)
mesh_obj('River rock pads', gv, M_GRAVEL, 'Site', bevel=0.3)
# exposed hips (4-1/2" wide, 3" below the ceiling) and ridge (5-1/2" wide, 4" below)
bm = bmesh.new(); rx = OX - OY
for sx in (-1, 1):
    for sy in (-1, 1):
        p0 = (sx*IX, sy*IY, U(P) - TG); p1 = (sx*rx, 0, U(OY) - TG)
        bar(bm, p0, p1, 4.5, 3.0, 4.0)
        hip_tail(bm, sx, sy, drop0=SOFFIT_HIP_DROP, drop1=SOFFIT_HIP_DROP)
bar(bm, (-rx - 2.5, 0, U(OY) - TG), (rx + 2.5, 0, U(OY) - TG), 5.5, 4.0, 3.0)
mesh_obj('Exposed hips + ridge - painted', bm, M_TRIM, 'Roof', bevel=0.12)

# ---------------------------------------------------------------- back wall: shiplap inside (house blue), lap siding outside
WY0, WY1 = PY - 3.75, PY + 3.75
bm = bmesh.new(); box(bm, -IX, IX, WY0 + 0.75, WY1 - 0.4, 0.0, B - 0.25); mesh_obj('Back wall framing', bm, M_GAP, 'Back wall')
bm = bmesh.new(); z = 5.75
while z < B - 0.25:
    box(bm, -IX, IX, WY0, WY0 + 0.75, z + 0.0625, min(z + 7.25, B - 0.25)); z += 7.375
mesh_obj('Shiplap 1x8 - inside', bm, M_SIDING, 'Back wall', bevel=0.04)
bm = bmesh.new(); box(bm, -IX, IX, WY0 - 0.75, WY0, 0.25, 5.75); mesh_obj('Baseboard Hardie 1x6 - wall', bm, M_TRIM, 'Back wall', bevel=0.05)
bm = bmesh.new(); z = 1.0
while z < B - 0.25:
    z1 = min(z + 8.25, B - 0.25)
    vs = [bm.verts.new(v(x, y, zz)) for (x, y, zz) in ((-IX, WY1 - 0.4, z1), (IX, WY1 - 0.4, z1), (IX, WY1 + 0.32, z), (-IX, WY1 + 0.32, z))]
    vb = [bm.verts.new(v(x, y, zz)) for (x, y, zz) in ((-IX, WY1 - 0.4, z), (IX, WY1 - 0.4, z))]
    bm.faces.new(vs); bm.faces.new((vs[3], vs[2], vb[1], vb[0])); bm.faces.new((vb[0], vb[1], vs[1], vs[0]))
    bm.faces.new((vs[0], vs[3], vb[0])); bm.faces.new((vs[1], vb[1], vs[2]))
    z += 7.0
mesh_obj('Lap siding Hardie 7in exposure - outside', bm, M_SIDING, 'Back wall')

# TV, soundbar, shelves (stained to match the ceiling), Charleston lanterns
bm = bmesh.new(); box(bm, -30.7, 30.7, WY0 - 1.4, WY0, 42.7, 77.3); mesh_obj('TV 70in', bm, M_BLACK, 'Back wall', bevel=0.1)
bm = bmesh.new(); box(bm, -30.2, 30.2, WY0 - 1.45, WY0 - 1.35, 43.2, 76.8); mesh_obj('TV screen', bm, M_TV, 'Back wall')
bm = bmesh.new(); box(bm, -21, 21, WY0 - 4.5, WY0 - 0.5, 37.5, 40.5); mesh_obj('Soundbar', bm, M_BLACK, 'Back wall', bevel=0.3)
bm = bmesh.new(); uvs = []
SC = (IX + 30.7)/2
for sx in (-1, 1):
    for zz in (52.0,):
        box(bm, sx*SC - 15, sx*SC + 15, WY0 - 10, WY0, zz, zz + 1.75)
shelf = mesh_obj('Floating shelves - stained pine', bm, M_PINE, 'Back wall', bevel=0.1)
shelf.data.uv_layers.new(name='UVMap')
for poly in shelf.data.polygons:
    for li in poly.loop_indices:
        co = shelf.data.vertices[shelf.data.loops[li].vertex_index].co / IN
        shelf.data.uv_layers[0].data[li].uv = (co.x, co.z*3 + co.y)
lant, glass, flame = bmesh.new(), bmesh.new(), bmesh.new(); k = 0.8           # lantern scale (about 16" tall body)
for sx in (-1, 1):
    cx, cy, cz = sx*SC, WY0 - 8.0*k, 72.0
    box(lant, cx - 4.5*k, cx + 4.5*k, cy - 4.5*k, cy + 4.5*k, cz - 10.5*k, cz - 9.5*k)
    box(lant, cx - 5.0*k, cx + 5.0*k, cy - 5.0*k, cy + 5.0*k, cz + 8.0*k, cz + 9.0*k)
    cyl(lant, cx, cy, cz + 11.5*k, 6.6*k, 5.0*k, segs=4, r2=0.8*k)
    cyl(lant, cx, cy, cz + 14.6*k, 0.6*k, 1.5*k, segs=12)
    for ax_, ay_ in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        box(lant, cx + ax_*4.5*k - 0.3, cx + ax_*4.5*k + 0.3, cy + ay_*4.5*k - 0.3, cy + ay_*4.5*k + 0.3, cz - 9.5*k, cz + 8.0*k)
    box(lant, cx - 0.8, cx + 0.8, cy + 4.5*k, WY0 - 0.6, cz + 2.0*k, cz + 3.5*k)
    box(lant, cx - 2.2, cx + 2.2, WY0 - 0.9, WY0 - 0.1, cz - 3.0*k, cz + 7.0*k)
    box(glass, cx - 4.3*k, cx + 4.3*k, cy - 4.3*k, cy + 4.3*k, cz - 9.5*k, cz + 8.0*k)
    cyl(flame, cx, cy, cz - 3.0*k, 0.9*k, 4.0*k, segs=12, r2=0.15)
for ob in (mesh_obj('Lanterns - Charleston style', lant, M_LANT, 'Lighting', bevel=0.08),):
    for p in ob.data.polygons: p.use_smooth = False
mesh_obj('Lantern glass', glass, M_GLASS, 'Lighting')
mesh_obj('Lantern flame bulbs', flame, M_FLAME, 'Lighting', smooth=True)

# ---------------------------------------------------------------- kitchen island (+X end), lime plaster, Hardie base, black leathered top
KX0, KX1 = IX, IX + 29.0                    # body: front flush with inside face of posts; granite to 120-3/8
KY0, KY1 = -IY, IY
bm = bmesh.new(); box(bm, KX0, KX1, KY0, KY1, 5.75, 34.75); mesh_obj('Island body - lime plaster', bm, M_LIME, 'Kitchen', bevel=0.25)
bm = bmesh.new(); box(bm, KX0 - 0.75, KX1 + 0.75, KY0 - 0.75, KY1 + 0.75, 0.25, 5.75); mesh_obj('Island baseboard Hardie 1x6', bm, M_TRIM, 'Kitchen', bevel=0.05)
bm = bmesh.new(); box(bm, KX0 - 1.0, KX1 + 1.0, KY0 - 1.0, KY1 + 1.0, 34.75, 36.0); top = mesh_obj('Countertop - black granite leathered', bm, M_GRANITE, 'Kitchen', bevel=0.12)
# run along the counter, from the back-wall corner (y=+66.375) toward the front: 12 / ice 24 / cab 24 / drawers 18 / grill 36 / 18.75
segs = [('c', 12), ('ice', 24), ('cab', 24), ('drw', 18), ('grill', 36), ('c', 18.75)]
ss, hw, dk = bmesh.new(), bmesh.new(), bmesh.new()
y = KY1; GRILL_Y = None
for kind, w in segs:
    y0, y1 = y - w, y; yc = (y0 + y1)/2
    if kind == 'ice':
        box(ss, KX0 + 3, KX0 + 21, y0 + 2, y1 - 2, 35.95, 36.25)                                     # flush lid
        box(ss, KX0 - 0.75, KX0, y0 + 1.5, y1 - 1.5, 8.0, 31.5)                                     # door
        box(hw, KX0 - 1.6, KX0 - 0.75, y1 - 4, y1 - 3.4, 22, 30)
    if kind == 'cab':
        for a, b_ in ((y0 + 1.5, yc - 0.25), (yc + 0.25, y1 - 1.5)):
            box(ss, KX0 - 0.75, KX0, a, b_, 8.0, 31.5)
        box(hw, KX0 - 1.6, KX0 - 0.75, yc - 1.5, yc - 0.9, 22, 30); box(hw, KX0 - 1.6, KX0 - 0.75, yc + 0.9, yc + 1.5, 22, 30)
    if kind == 'drw':
        for (za, zb) in ((8.0, 15.5), (16.0, 23.5), (24.0, 31.5)):
            box(ss, KX0 - 0.75, KX0, y0 + 1.5, y1 - 1.5, za, zb); box(hw, KX0 - 1.6, KX0 - 0.75, yc - 4, yc + 4, zb - 2.0, zb - 1.4)
    if kind == 'grill':
        GRILL_Y = yc
        box(ss, KX0 - 1.0, KX0 + 22.0, y0 + 0.5, y1 - 0.5, 27.5, 36.2)                              # firebox + control panel
        lid = bmesh.new(); box(lid, KX0 + 0.5, KX0 + 22.5, y0 + 1.0, y1 - 1.0, 36.2, 46.0)            # lid, rounded by bevel
        lo = mesh_obj('Grill lid', lid, M_SS, 'Kitchen', smooth=True)
        bv = lo.modifiers.new('Round', 'BEVEL'); bv.width = 4.0*IN; bv.segments = 8
        box(hw, KX0 - 3.0, KX0 - 2.2, y0 + 4, y1 - 4, 41.0, 41.8)                                   # handle
        for k in range(4):
            cyl(dk, KX0 - 1.6, y0 + 6 + k*8, 31.5, 0.9, 1.2, axis='X', segs=16)                     # knobs
        for a, b_ in ((y0 + 2.0, yc - 0.25), (yc + 0.25, y1 - 2.0)):                                # LP bottle access doors
            box(ss, KX0 - 0.75, KX0, a, b_, 8.0, 25.5)
        box(hw, KX0 - 1.6, KX0 - 0.75, yc - 1.5, yc - 0.9, 14, 22); box(hw, KX0 - 1.6, KX0 - 0.75, yc + 0.9, yc + 1.5, 14, 22)
    y = y0
for sy in (-1, 1):                                                                                 # LP vent panels low on both ends
    box(ss, KX0 + 14, KX0 + 24, sy*(KY1 + 0.75), sy*(KY1 + 0.95), 6.5, 10.5)
mesh_obj('Kitchen stainless', ss, M_SS, 'Kitchen', bevel=0.08)
mesh_obj('Kitchen hardware', hw, M_SS, 'Kitchen', bevel=0.1)
mesh_obj('Grill knobs', dk, M_BLACK, 'Kitchen', smooth=True)
# lime-plaster hood over the grill: straight sides, tapered front, rises behind the beam to the soffit
HW = 21.0; hy0, hy1 = GRILL_Y - HW, GRILL_Y + HW
zs = lambda x: U(OX - x) - TG                                    # soffit underside at plan x (outside the beam)
prof_xz = [(IX - 4.0, 72.0), (RX - 1.5, 72.0), (RX - 1.5, zs(RX - 1.5)), (OX, zs(OX)), (OX, B - 0.25), (IX, B - 0.25), (IX - 4.0, 78.0)]
bm = bmesh.new()
f0 = [bm.verts.new(v(x, hy0, z)) for x, z in prof_xz]; f1 = [bm.verts.new(v(x, hy1, z)) for x, z in prof_xz]
bm.faces.new(f0); bm.faces.new(list(reversed(f1)))
for i in range(len(prof_xz)):
    j = (i + 1) % len(prof_xz); bm.faces.new((f0[i], f0[j], f1[j], f1[i]))
mesh_obj('Hood - lime plaster', bm, M_LIME, 'Kitchen', bevel=0.3)
bm = bmesh.new(); box(bm, IX - 2.5, RX - 4.0, hy0 + 2.5, hy1 - 2.5, 71.9, 72.05); M_BAFFLE, _ = simple('Hood baffle filters', (0.12, 0.12, 0.12), 0.45, 1.0); mesh_obj('Hood liner + filters', bm, M_BAFFLE, 'Kitchen')
bm = bmesh.new(); cyl(bm, RX - 12, GRILL_Y, U(-(RX - 12 - OX)) + ROOF_T + 4, 5.0, 10.0, segs=20); mesh_obj('Hood roof jack', bm, M_BLACK, 'Kitchen')

# ---------------------------------------------------------------- lounge furniture, rug, fan
M_CUSH, _ = simple('Outdoor cushions - white canvas', (0.70, 0.68, 0.63), 0.92)
tk, cu, pil = bmesh.new(), bmesh.new(), bmesh.new()
def teak_seat(cx, cy, w, d, rot_deg, pillows=()):
    """outdoor teak sofa/club chair facing local -y -> rotated; seat 17" high, cushions 5", back cushions"""
    tb, cb, pb = bmesh.new(), bmesh.new(), bmesh.new()
    box(tb, -w/2, w/2, -d/2 + 3, d/2, 8.0, 11.0)                                  # seat deck
    for x in (-w/2, w/2 - 2.5):
        box(tb, x, x + 2.5, -d/2, d/2, 0.0, 24.0)                                 # arm / leg panels
        box(tb, x - 0.25, x + 2.75, -d/2, d/2, 24.0, 25.25)                       # arm caps
    box(tb, -w/2 + 2.5, w/2 - 2.5, d/2 - 2.0, d/2, 8.0, 30.0)                      # back frame
    box(cb, -w/2 + 2.5, w/2 - 2.5, -d/2 + 1.0, d/2 - 2.0, 11.0, 17.0)               # seat cushion
    box(cb, -w/2 + 2.5, w/2 - 2.5, d/2 - 8.0, d/2 - 2.0, 17.0, 31.0)               # back cushion
    for px in pillows: box(pb, px - 8, px + 8, d/2 - 10.5, d/2 - 7.5, 17.0, 32.0)
    M = Matrix.Translation(v(cx, cy, 0)) @ Matrix.Rotation(math.radians(rot_deg), 4, 'Z')
    for src, dst in ((tb, tk), (cb, cu), (pb, pil)):
        bmesh.ops.transform(src, matrix=M, verts=src.verts[:])
        me = bpy.data.meshes.new('tmp'); src.to_mesh(me); dst.from_mesh(me); bpy.data.meshes.remove(me); src.free()
# sofa faces the TV (local -y forward -> rotate 180 so it faces +y)
teak_seat(-4, -PY + 14.0, 86, 34, 180, pillows=(-28, 28))
# two club chairs on the open left side, angled toward the TV and the coffee table
teak_seat(-70, -14, 32, 33, 110, pillows=(0,))
teak_seat(-66, 30, 32, 33, 75, pillows=(0,))
mesh_obj('Outdoor sofa + chairs - teak', tk, M_TEAK, 'Furniture', bevel=0.25)
mesh_obj('Outdoor cushions', cu, M_CUSH, 'Furniture', bevel=1.2)
mesh_obj('Pillows', pil, M_PILLOW, 'Furniture', bevel=1.5)
bm = bmesh.new(); box(bm, -30, 18, -22, 4, 14, 16); [box(bm, x - 1, x + 1, y - 1, y + 1, 0, 14) for x in (-28, 16) for y in (-20, 2)]
box(bm, -30, 18, -22, 4, 3, 4)
for (x, y) in ((-84, 9), (-58, -60)): box(bm, x - 9, x + 9, y - 9, y + 9, 20, 21.5); box(bm, x - 8, x + 8, y - 8, y + 8, 0, 20)
mesh_obj('Coffee + side tables - teak', bm, M_TEAK, 'Furniture', bevel=0.2)
bm = bmesh.new(); box(bm, -86, 44, -60, 40, 0.0, 0.4); mesh_obj('Outdoor rug', bm, M_RUG, 'Furniture', bevel=0.15)
fan = bmesh.new(); zr = U(OY) - TG - 4.0
cyl(fan, 0, 0, zr - 9, 0.5, 18, segs=12); cyl(fan, 0, 0, zr - 20, 5.5, 5.5, segs=32); cyl(fan, 0, 0, zr - 24, 3.0, 3, segs=24)
for k in range(5):
    a = k*2*math.pi/5; d = Vector((math.cos(a), math.sin(a), 0))
    bar(fan, (5.0*math.cos(a), 5.0*math.sin(a), zr - 20), (36*math.cos(a), 36*math.sin(a), zr - 20.6), 7.0, 0.2, 0.2)
mesh_obj('Ceiling fan 72in', fan, M_FANBODY, 'Lighting', smooth=False)
bm = bmesh.new(); cyl(bm, 0, 0, zr - 25.8, 2.8, 0.6, segs=24); mesh_obj('Fan light lens', bm, M_CAN, 'Lighting')

# ---------------------------------------------------------------- lights
def light(name, kind, loc, energy, color, rot=(0, 0, 0), **kw):
    ld = bpy.data.lights.new(name, kind); ld.energy = energy; ld.color = color
    for k, val in kw.items(): setattr(ld, k, val)
    ob = bpy.data.objects.new(name, ld); ob.location = loc; ob.rotation_euler = rot; coll('Lighting').objects.link(ob)
    return ob
cans = bmesh.new()
for (x, y) in ((-48, -RY + 9), (48, -RY + 9), (-RX + 9, -36), (-RX + 9, 36)):
    s = -(max(abs(x) - OX, abs(y) - OY)); z = U(s) - TG - 0.05
    cyl(cans, x, y, z, 1.6, 0.1, segs=20)
    light(f'Soffit can {x:+.0f},{y:+.0f}', 'SPOT', v(x, y, z - 0.3), 25, (1.0, 0.82, 0.62), spot_size=math.radians(70), spot_blend=0.6, shadow_soft_size=0.02)
mesh_obj('Soffit cans', cans, M_CAN, 'Lighting')
light('Fan light', 'POINT', v(0, 0, zr - 27), 35, (1.0, 0.82, 0.62), shadow_soft_size=0.06)

# ---------------------------------------------------------------- world + sun
w = bpy.data.worlds.new('Sky'); w.use_nodes = True; wn = w.node_tree
HDR = next((os.path.join(TEX, f) for f in ('noon_grass_8k.hdr', 'noon_grass_4k.hdr') if os.path.exists(os.path.join(TEX, f))), None)
if HDR is None: raise SystemExit('Missing sky HDRI: run fetch_textures.sh first (Poly Haven noon_grass)')
env = wn.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(HDR)
mp = wn.nodes.new('ShaderNodeMapping'); tc = wn.nodes.new('ShaderNodeTexCoord')
wn.links.new(tc.outputs['Generated'], mp.inputs['Vector']); wn.links.new(mp.outputs[0], env.inputs['Vector'])
mp.inputs['Rotation'].default_value = (0, 0, math.radians(200))
bg = [n for n in wn.nodes if n.type == 'BACKGROUND'][0]; wn.links.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
scn.world = w

# ---------------------------------------------------------------- cameras
def camera(name, eye, target, lens=35, shift=(0.0, 0.0), level=True):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = 36; cd.shift_x, cd.shift_y = shift; cd.clip_start = 0.05; cd.clip_end = 300
    ob = bpy.data.objects.new(name, cd); coll('Cameras').objects.link(ob); ob.location = v(*eye)
    d = v(*target) - ob.location
    if level: ob.rotation_euler = (math.radians(90), 0, math.atan2(d.y, d.x) - math.pi/2)
    else: ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob
cams = [camera('CAM_01 front 3-4', (-300, -360, 62), (10, 0, 62), 35, (0, 0.10)),
        camera('CAM_02 kitchen end', (380, -250, 62), (60, 0, 62), 35, (0, 0.10)),
        camera('CAM_03 interior to TV', (-10, -175, 56), (0, 72, 56), 24, (0, 0.12)),
        camera('CAM_04 interior to kitchen', (-70, 20, 58), (100, -25, 58), 24, (0, 0.12)),
        camera('CAM_05 ceiling + hips', (-50, -70, 48), (25, 25, 135), 20, level=False),
        camera('CAM_07 corner detail - trim + soffit hip', (-175, -190, 54), (-104, -80, 102), 50, level=False),
        camera('CAM_08 soffit corner looking up', (-150, -150, 60), (-112, -88, 108), 35, level=False),
        camera('CAM_09 lounge from the kitchen', (44, -40, 60), (-80, 25, 36), 24, level=False),
        camera('CAM_10 back 3-4 (NE)', (330, 360, 66), (0, 0, 70), 35, (0, 0.10)),
        camera('CAM_06 hood + island close', (8, 30, 62), (110, -30, 62), 28, (0, 0.10))]
scn.camera = cams[0]
r = scn.render; r.engine = 'CYCLES'; r.resolution_x, r.resolution_y = 1920, 1080
scn.cycles.samples = 128; scn.cycles.use_denoising = True; scn.cycles.denoiser = 'OPENIMAGEDENOISE'
scn.cycles.use_adaptive_sampling = True; scn.cycles.adaptive_threshold = 0.02; scn.cycles.max_bounces = 10
scn.cycles.sample_clamp_indirect = 8.0; scn.cycles.caustics_reflective = False; scn.cycles.caustics_refractive = False
scn.view_settings.view_transform = 'AgX'; scn.view_settings.look = 'AgX - Medium High Contrast'
scn.unit_settings.system = 'IMPERIAL'; scn.unit_settings.length_unit = 'FEET'

out = os.environ.get('PAV_OUT') or os.path.join(HERE, 'sunup-pavilion.blend')
bpy.ops.wm.save_as_mainfile(filepath=out, relative_remap=True)
try: bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_mainfile()
except Exception as e: print('relative paths:', e)
print('SAVED', out)
