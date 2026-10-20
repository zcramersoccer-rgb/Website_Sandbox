# Van Hove range hood - photoreal proposal renders (Luxurious Renovations, 175 Civitas St, Mount Pleasant SC)
# Blender 4.2+.   blender -b -P build_scene.py                 -> builds vanhove-hood.blend next to this file
#                 blender -b -P build_scene.py -- render       -> also renders the three options into ./renders
# The .blend holds one scene per finish ("A Marmorino satin", "B Limewash", "C Brass band"): pick the scene, F12.
# Dimensions come from HANDOFF.md (inches). Internally metres, scene units imperial.
import bpy, bmesh, os, sys, math, random
from mathutils import Vector, Matrix
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, 'textures')
IN = 0.0254
def v(x, y, z): return Vector((x*IN, y*IN, z*IN))

# ------------------------------------------------------------------ reset
bpy.ops.wm.read_factory_settings(use_empty=True)
base = bpy.context.scene; base.name = 'A Marmorino satin'
kitchen = bpy.data.collections.new('Kitchen'); base.collection.children.link(kitchen)

def link(ob, coll): coll.objects.link(ob); return ob
def mesh_obj(name, bm, mat, coll, smooth=False, bevel=None):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = smooth
    if mat: me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); link(ob, coll)
    if bevel:
        bv = ob.modifiers.new('Bevel', 'BEVEL'); bv.width = bevel*IN; bv.segments = 3
        bv.limit_method = 'ANGLE'; bv.angle_limit = math.radians(30); bv.harden_normals = False
    return ob
def box(bm, x0, x1, y0, y1, z0, z1):
    """axis box in inches (any corner order)"""
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    M = Matrix.Translation(v((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)) @ Matrix.Diagonal(((x1-x0)*IN, (y1-y0)*IN, (z1-z0)*IN, 1))
    bmesh.ops.create_cube(bm, size=1.0, matrix=M)
def cyl(bm, x, y, z, r, depth, axis='Z', segs=24):
    R = {'Z': Matrix.Identity(4), 'Y': Matrix.Rotation(math.pi/2, 4, 'X'), 'X': Matrix.Rotation(math.pi/2, 4, 'Y')}[axis]
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r*IN, radius2=r*IN, depth=depth*IN,
                          matrix=Matrix.Translation(v(x, y, z)) @ R)

# ------------------------------------------------------------------ material helpers
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
    def co(s, scale=1.0, rot=(0, 0, 0)):
        tc = s.N.new('ShaderNodeTexCoord'); mp = s.N.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (scale, scale, scale) if isinstance(scale, (int, float)) else scale
        mp.inputs['Rotation'].default_value = rot; s.L.new(tc.outputs['Object'], mp.inputs['Vector']); return mp.outputs[0]
    def img(s, path, vec, color=True, blend=0.25):
        t = s.N.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(path, check_existing=True)
        if not color: t.image.colorspace_settings.name = 'Non-Color'
        t.projection = 'BOX'; t.projection_blend = blend; s.L.new(vec, t.inputs['Vector']); return t
    def normal_map(s, tex_out, strength):
        nm = s.N.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = strength
        s.L.new(tex_out, nm.inputs['Color']); s.L.new(nm.outputs[0], s.b.inputs['Normal']); return nm

def srgb(h):
    c = [int(h[i:i+2], 16)/255 for i in (1, 3, 5)]
    return tuple(x/12.92 if x <= 0.04045 else ((x+0.055)/1.055)**2.4 for x in c)
def mean_lum(path):
    im = bpy.data.images.load(path, check_existing=True); w, h = im.size
    px = np.empty(w*h*4, np.float32); im.pixels.foreach_get(px); px = px.reshape(-1, 4)
    return float((0.2126*px[:, 0]+0.7152*px[:, 1]+0.0722*px[:, 2]).mean())
def acg(name, kind):
    for r in ('4K', '2K'):
        p = os.path.join(TEX, name, f'{name}_{r}-JPG_{kind}.jpg')
        if os.path.exists(p): return p

def tinted(t, path, vec, target, contrast):
    """photo-scan colour turned into luminance variation around the target colour (keeps the scan's real texture)"""
    tx = t.img(path, vec); m = mean_lum(path)
    bw = t.node('ShaderNodeRGBToBW'); t.L.new(tx.outputs['Color'], bw.inputs[0])
    f = t.math('ADD', 1.0, t.math('MULTIPLY', t.math('SUBTRACT', t.math('DIVIDE', bw.outputs[0], m), 1.0), contrast))
    return t.mix((*target, 1), f, 1.0, 'MULTIPLY')

PLASTER_TARGET = srgb('#D6C5AB')                       # warm earthy beige from the brief
def trowel_passes(t, scale, stretch=(1.0, 1.0, 1.0)):
    """overlapping hand-trowel passes: warped, smoothed Voronoi cells (one random value per pass) + the faint ridge
    where passes overlap. Returns (cell random colour, ridge 0-1)."""
    base = t.co(1.0)
    wn = t.node('ShaderNodeTexNoise', i_Scale=2.5, i_Detail=3.0); t.L.new(base, wn.inputs['Vector'])
    wv = t.vmath('ADD', t.vmath('MULTIPLY', base, stretch), t.vmath('MULTIPLY', t.vmath('SUBTRACT', wn.outputs['Color'], (0.5, 0.5, 0.5)), (0.22, 0.22, 0.22)))
    vc = t.node('ShaderNodeTexVoronoi', feature='SMOOTH_F1', i_Scale=scale, i_Smoothness=0.9, i_Randomness=1.0); t.L.new(wv, vc.inputs['Vector'])
    ve = t.node('ShaderNodeTexVoronoi', feature='DISTANCE_TO_EDGE', i_Scale=scale, i_Randomness=1.0); t.L.new(wv, ve.inputs['Vector'])
    return vc.outputs['Color'], t.mapr(ve.outputs['Distance'], 0.0, 0.09, 1.0, 0.0, 'SMOOTHSTEP')

PLASTER_TARGET = srgb('#D6C5AB')                       # warm earthy beige from the brief
def mat_marmorino(name='Marmorino satin'):
    """Option A (Concrete034 4K scan): compressed steel-trowelled lime with fine marble - smooth stone, soft satin
    sheen, cloudy depth. Each trowel pass gets its own slight tone and burnish; passes overlap in faint ridges."""
    m = bpy.data.materials.new(name); t = NT(m); vec = t.co(1.4)
    col = tinted(t, acg('Concrete034', 'Color'), vec, PLASTER_TARGET, 0.5)
    cl = t.node('ShaderNodeTexNoise', i_Scale=1.1, i_Detail=4.0, i_Roughness=0.55); t.L.new(t.co(1.0), cl.inputs['Vector'])
    cloud = t.mapr(cl.outputs['Fac'], 0.3, 0.7, 0.90, 1.08)                     # cloudy movement (1-2 ft)
    cl2 = t.node('ShaderNodeTexNoise', i_Scale=4.0, i_Detail=6.0, i_Roughness=0.6); t.L.new(t.co(1.0), cl2.inputs['Vector'])
    cloud = t.mix(cloud, t.mapr(cl2.outputs['Fac'], 0.3, 0.7, 0.95, 1.04), 1.0, 'MULTIPLY')   # smaller mottling
    cell, ridge = trowel_passes(t, 5.5, (1.0, 1.0, 1.6))
    cr = t.node('ShaderNodeSeparateColor'); t.L.new(cell, cr.inputs[0])
    passes = t.mapr(cr.outputs[0], 0.0, 1.0, 0.95, 1.05)
    col = t.mix(t.mix(col, cloud, 1.0, 'MULTIPLY'), passes, 1.0, 'MULTIPLY')
    col = t.mix(col, t.mapr(ridge, 0, 1, 1.0, 0.985), 1.0, 'MULTIPLY')
    # layered Venetian clouds: deeper, warmer translucent patches floating under lighter burnished veils
    deep = tuple(c*f for c, f in zip(PLASTER_TARGET, (0.84, 0.82, 0.79))) + (1,)
    pale = tuple(min(1, c*f) for c, f in zip(PLASTER_TARGET, (1.07, 1.07, 1.06))) + (1,)
    cv = t.node('ShaderNodeTexNoise', i_Scale=1.8, i_Detail=3.0, i_Roughness=0.5, i_Distortion=0.0); t.L.new(t.co(1.0), cv.inputs['Vector'])
    cv2 = t.node('ShaderNodeTexNoise', i_Scale=5.0, i_Detail=3.0, i_Roughness=0.5, i_Distortion=0.0); t.L.new(t.co(1.0), cv2.inputs['Vector'])
    cfac = t.math('ADD', t.math('MULTIPLY', cv.outputs['Fac'], 0.85), t.math('MULTIPLY', cv2.outputs['Fac'], 0.15))
    col = t.mix(col, t.mix(col, deep, 1.0, 'MULTIPLY'), t.mapr(cfac, 0.42, 0.72, 0.0, 0.85, 'SMOOTHSTEP'))
    col = t.mix(col, pale, t.mapr(cfac, 0.45, 0.28, 0.0, 0.6, 'SMOOTHSTEP'))
    t.set(t.b.inputs['Base Color'], col)
    rt = t.img(acg('Concrete034', 'Roughness'), vec, False)
    r = t.math('ADD', t.mapr(rt.outputs['Color'], 0.0, 1.0, 0.26, 0.40), t.mapr(cr.outputs[1], 0.0, 1.0, -0.07, 0.07))
    r = t.math('ADD', r, t.mapr(cl.outputs['Fac'], 0.35, 0.65, -0.03, 0.04))
    r = t.math('SUBTRACT', r, t.mapr(cfac, 0.5, 0.7, 0.0, 0.06))                 # deeper clouds are more burnished
    t.set(t.b.inputs['Roughness'], t.math('SUBTRACT', r, t.math('MULTIPLY', ridge, 0.06)))  # ridges burnish shinier
    disp = t.img(acg('Concrete034', 'Displacement'), vec, False)
    h = t.math('ADD', disp.outputs['Color'], t.math('MULTIPLY', ridge, 0.2))
    bp = t.node('ShaderNodeBump', i_Strength=0.16, i_Distance=0.0005); t.L.new(h, bp.inputs['Height'])
    nm = t.node('ShaderNodeNormalMap', i_Strength=0.07); t.L.new(t.img(acg('Concrete034', 'NormalGL'), vec, False).outputs['Color'], nm.inputs['Color'])
    t.L.new(nm.outputs[0], bp.inputs['Normal']); t.L.new(bp.outputs[0], t.b.inputs['Normal'])
    t.b.inputs['Coat Weight'].default_value = 0.22                                # black-soap burnish
    t.set(t.b.inputs['Coat Roughness'], t.mapr(cr.outputs[2], 0.0, 1.0, 0.22, 0.36))
    return m

def mat_limewash(name='Lime plaster + limewash'):
    """Option B (Plaster006 4K scan): sand-finish lime under 2-3 brushed limewash coats, linseed sealed.
    A chalky, lighter wash layer sits patchily over a slightly deeper base, with crossed brush strokes."""
    m = bpy.data.materials.new(name); t = NT(m); vec = t.co(1.2)
    target = tuple(c*f for c, f in zip(PLASTER_TARGET, (0.93, 0.90, 0.84)))
    scan = tinted(t, acg('Plaster006', 'Color'), vec, (1, 1, 1), 0.6)
    under = (target[0]*0.88, target[1]*0.86, target[2]*0.82, 1); over = (min(1, target[0]*1.07), min(1, target[1]*1.07), min(1, target[2]*1.05), 1)
    strokes = []
    for ang in (35, -35):
        n = t.node('ShaderNodeTexNoise', i_Scale=1.0, i_Detail=7.0, i_Roughness=0.62)
        t.L.new(t.co((3.0, 3.0, 26.0), (0, math.radians(ang), 0)), n.inputs['Vector']); strokes.append(n.outputs['Fac'])
    cov = t.node('ShaderNodeTexNoise', i_Scale=1.8, i_Detail=8.0, i_Roughness=0.65); t.L.new(t.co(1.0), cov.inputs['Vector'])
    c = t.math('ADD', t.math('MULTIPLY', cov.outputs['Fac'], 0.5), t.math('MULTIPLY', t.math('ADD', strokes[0], strokes[1]), 0.25))
    wash = t.mapr(c, 0.40, 0.62, 0.0, 1.0, 'SMOOTHSTEP')                         # where the wash coat is thicker
    col = t.mix(under, over, wash)
    col = t.mix(col, scan, 1.0, 'MULTIPLY')
    bl = t.node('ShaderNodeTexNoise', i_Scale=2.2, i_Detail=4.0, i_Roughness=0.6); t.L.new(t.co(1.0), bl.inputs['Vector'])
    col = t.mix(col, t.mapr(bl.outputs['Fac'], 0.32, 0.68, 0.92, 1.08), 1.0, 'MULTIPLY')
    t.set(t.b.inputs['Base Color'], col)
    rt = t.img(acg('Plaster006', 'Roughness'), vec, False)
    t.set(t.b.inputs['Roughness'], t.math('ADD', t.mapr(rt.outputs['Color'], 0.0, 1.0, 0.84, 0.94), t.math('MULTIPLY', wash, 0.03)))
    disp = t.img(acg('Plaster006', 'Displacement'), vec, False)
    bp = t.node('ShaderNodeBump', i_Strength=0.22, i_Distance=0.0006); t.L.new(disp.outputs['Color'], bp.inputs['Height'])
    nm = t.node('ShaderNodeNormalMap', i_Strength=0.2); t.L.new(t.img(acg('Plaster006', 'NormalGL'), vec, False).outputs['Color'], nm.inputs['Color'])
    t.L.new(nm.outputs[0], bp.inputs['Normal']); t.L.new(bp.outputs[0], t.b.inputs['Normal'])
    t.b.inputs['Specular IOR Level'].default_value = 0.35
    return m

def mat_brass(name='Satin brass'):
    """Option C band: new (unaged, lacquered) satin brass. Brass F0 colour, scan only for faint tone variation,
    horizontal anisotropic brushing so highlights stretch sideways like a real brushed band."""
    m = bpy.data.materials.new(name); t = NT(m); vec = t.co(3.0)
    c = tinted(t, acg('Metal042A', 'Color'), vec, (0.90, 0.68, 0.30), 0.12)
    t.set(t.b.inputs['Base Color'], c)
    t.b.inputs['Metallic'].default_value = 1.0
    r = t.img(acg('Metal042A', 'Roughness'), vec, False)
    t.set(t.b.inputs['Roughness'], t.mapr(r.outputs['Color'], 0, 1, 0.22, 0.29))
    t.b.inputs['Anisotropic'].default_value = 0.6
    tg = t.node('ShaderNodeTangent', direction_type='RADIAL', axis='Z'); t.L.new(tg.outputs[0], t.b.inputs['Tangent'])
    br = t.node('ShaderNodeTexNoise', i_Scale=1.0, i_Detail=6.0); t.L.new(t.co((2.0, 600.0, 600.0)), br.inputs['Vector'])
    bp = t.node('ShaderNodeBump', i_Strength=0.04, i_Distance=0.0003); t.L.new(br.outputs['Fac'], bp.inputs['Height'])
    t.L.new(bp.outputs[0], t.b.inputs['Normal'])
    t.b.inputs['Coat Weight'].default_value = 0.3; t.b.inputs['Coat Roughness'].default_value = 0.15   # clear lacquer
    return m

def mat_simple(name, color, rough, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name); t = NT(m)
    t.b.inputs['Base Color'].default_value = (*color, 1); t.b.inputs['Roughness'].default_value = rough
    t.b.inputs['Metallic'].default_value = metal; t.b.inputs['Coat Weight'].default_value = coat
    return m, t
def mat_stainless():
    m, t = mat_simple('Brushed stainless', (0.58, 0.58, 0.57), 0.25, 1.0)
    br = t.node('ShaderNodeTexNoise', i_Scale=1.0, i_Detail=4.0); t.L.new(t.co((1.5, 400.0, 400.0)), br.inputs['Vector'])
    bp = t.node('ShaderNodeBump', i_Strength=0.06, i_Distance=0.0004); t.L.new(br.outputs['Fac'], bp.inputs['Height'])
    t.L.new(bp.outputs[0], t.b.inputs['Normal']); return m
def mat_plaster_wall(name, hexcol, rough, scan='Plaster001', contrast=0.25, scale=1.0):
    m = bpy.data.materials.new(name); t = NT(m); vec = t.co(scale)
    t.set(t.b.inputs['Base Color'], tinted(t, acg(scan, 'Color'), vec, srgb(hexcol), contrast))
    t.b.inputs['Roughness'].default_value = rough
    t.normal_map(t.img(acg(scan, 'NormalGL'), vec, False).outputs['Color'], 0.12); return m
def mat_floor():
    m = bpy.data.materials.new('Heart pine floor'); t = NT(m); vec = t.co(1/2.0)    # Poly Haven scan is 2 m square
    c = t.img(os.path.join(TEX, 'wood_floor_worn_diff_2k.jpg'), vec, blend=0.0)
    t.set(t.b.inputs['Base Color'], t.mix(c.outputs['Color'], (1.0, 0.86, 0.66, 1), 0.5, 'MULTIPLY'))   # warmer amber
    r = t.img(os.path.join(TEX, 'wood_floor_worn_rough_2k.jpg'), vec, False, 0.0)
    t.set(t.b.inputs['Roughness'], t.mapr(r.outputs['Color'], 0, 1, 0.32, 0.6))
    t.normal_map(t.img(os.path.join(TEX, 'wood_floor_worn_nor_gl_2k.jpg'), vec, False, 0.0).outputs['Color'], 0.6)
    t.b.inputs['Coat Weight'].default_value = 0.25; t.b.inputs['Coat Roughness'].default_value = 0.2; return m
def mat_granite():
    m = bpy.data.materials.new('Typhoon Bordeaux granite'); t = NT(m)
    tx = t.img(os.path.join(TEX, 'typhoon_bordeaux_tile.jpg'), t.co((1/0.75, 1/1.03, 1/1.03)), blend=0.2)
    tx.extension = 'REPEAT'; t.set(t.b.inputs['Base Color'], tx.outputs['Color'])
    t.b.inputs['Roughness'].default_value = 0.15; t.b.inputs['Coat Weight'].default_value = 0.6; t.b.inputs['Coat Roughness'].default_value = 0.05
    return m

M_A, M_B, M_BRASS = mat_marmorino(), mat_limewash(), mat_brass()
M_RIVET, _ = mat_simple('Polished brass rivet heads', (0.90, 0.68, 0.30), 0.12, 1.0, 0.3)
M_SS = mat_stainless()
M_IRON, _ = mat_simple('Cast iron', (0.025, 0.025, 0.025), 0.6)
M_BURNER, _ = mat_simple('Burner caps', (0.015, 0.015, 0.015), 0.35)
M_TOP, _ = mat_simple('Cooktop', (0.02, 0.02, 0.022), 0.3, 0.0, 0.5)
M_CAB, _ = mat_simple('Cabinet paint warm white', srgb('#EEE8DA'), 0.5)
M_KNOB, _ = mat_simple('Satin nickel', (0.62, 0.60, 0.56), 0.3, 1.0)
M_GLASS, _ = mat_simple('Oven glass', (0.01, 0.01, 0.012), 0.05, 0.0, 1.0)
M_KNOBBLK, _ = mat_simple('Range knobs', (0.03, 0.03, 0.03), 0.35)
M_WALL = mat_plaster_wall('Wall paint warm off-white', '#ECE6DA', 0.88, contrast=0.12, scale=0.8)
M_SPLASH = mat_plaster_wall('Backsplash matte cream', '#E6DCC8', 0.8, contrast=0.3, scale=1.4)
M_CEIL, _ = mat_simple('Ceiling white', srgb('#F2F0EA'), 0.9)
M_FLOOR, M_GRANITE = mat_floor(), mat_granite()
M_TOE, _ = mat_simple('Toe kick', (0.03, 0.028, 0.026), 0.7)
M_LED = bpy.data.materials.new('LED strip'); t_ = NT(M_LED); t_.b.inputs['Emission Color'].default_value = (1.0, 0.72, 0.45, 1); t_.b.inputs['Emission Strength'].default_value = 3.0
M_WINFRAME, _ = mat_simple('Window frame', srgb('#F2F0EA'), 0.45)
M_WINGLASS = bpy.data.materials.new('Window glass'); tg = NT(M_WINGLASS); tg.b.inputs['Transmission Weight'].default_value = 1.0; tg.b.inputs['Roughness'].default_value = 0.0

# ------------------------------------------------------------------ hood geometry (inches)
HOOD_BOT, BAND_H, CAP_H, CROWN_UNDER = 66.0, 9.0, 1.25, 114.0
CAP_TOP = HOOD_BOT + BAND_H + CAP_H                      # 76.25
SWEEP_H = CROWN_UNDER - CAP_TOP                          # 37.75
def s_of_t(t):                                           # t: 0 at top of chimney, 1 at the cap
    if t <= 0.32: return 0.0
    u = (t-0.32)/0.68; return u**2.4                     # concave flare
def build_sweep():
    bm = bmesh.new(); rings = []; N = 90; NS, NF = 12, 24
    ts = [0.32*i/14 for i in range(14)] + [0.32 + 0.68*(i/N)**0.8 for i in range(0, N+1)]
    for t in ts:
        s = s_of_t(t); w = 18 + 18*s; d = 11.5 + 7.5*s; z = CROWN_UNDER - t*SWEEP_H
        pts = [(-w/2, -d*k/NS) for k in range(NS)] + [(-w/2 + w*k/NF, -d) for k in range(NF)] + [(w/2, -d + d*k/NS) for k in range(NS+1)]
        rings.append([bm.verts.new(v(x, y, z)) for x, y in pts])
    for a, b in zip(rings, rings[1:]):
        for i in range(len(a)-1): bm.faces.new((a[i], a[i+1], b[i+1], b[i]))
    bot = rings[-1]; bm.faces.new([bot[0], bot[NS], bot[NS+NF], bot[-1]])    # underside (sits on the cap)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:]); return bm
def build_cap():
    bm = bmesh.new(); box(bm, -18.75, 18.75, 0, -19.75, HOOD_BOT+BAND_H, CAP_TOP); return bm
def build_band():
    """36 x 19 x 9 band with a small bead groove 1 in above the bottom edge"""
    bm = bmesh.new()
    box(bm, -18, 18, 0, -19, HOOD_BOT, HOOD_BOT+0.82)
    box(bm, -17.82, 17.82, 0, -18.82, HOOD_BOT+0.82, HOOD_BOT+1.18)     # 3/16 in deep groove
    box(bm, -18, 18, 0, -19, HOOD_BOT+1.18, HOOD_BOT+BAND_H); return bm
def build_rivets():
    bm = bmesh.new(); zc = HOOD_BOT + 1.18 + (BAND_H-1.18)/2
    for i in range(8):
        x = -18 + 36*(i+0.5)/8                                   # 3/4 in domed heads standing ~1/4 in proud
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=0.375*IN,
                                  matrix=Matrix.Translation(v(x, -19.0, zc)) @ Matrix.Diagonal((1, 0.65, 1, 1)))
    return bm

WOBBLE = bpy.data.textures.new('hand-applied plaster wobble', 'CLOUDS'); WOBBLE.noise_scale = 0.16; WOBBLE.noise_depth = 2
def hand_applied(ob, subdiv):
    """real troweled plaster is never dead flat: <1 mm long-wave undulation so reflections ripple like a real hood"""
    if subdiv: sd = ob.modifiers.new('Subdiv', 'SUBSURF'); sd.subdivision_type = 'SIMPLE'; sd.levels = sd.render_levels = subdiv
    dp = ob.modifiers.new('Hand applied', 'DISPLACE'); dp.texture = WOBBLE; dp.strength = 0.0009; dp.mid_level = 0.5
    dp.texture_coords = 'GLOBAL'
def make_hood(tag, body, band, rivets):
    coll = bpy.data.collections.new(f'Hood {tag}')
    sw = mesh_obj(f'Hood_{tag}_sweep', build_sweep(), body, coll, smooth=True, bevel=0.25); hand_applied(sw, 0)
    cp = mesh_obj(f'Hood_{tag}_cap', build_cap(), body, coll, smooth=True, bevel=0.25); hand_applied(cp, 4)
    bd = mesh_obj(f'Hood_{tag}_band', build_band(), band, coll, smooth=True, bevel=0.2)
    if band is not M_BRASS: hand_applied(bd, 4)
    if rivets: mesh_obj(f'Hood_{tag}_rivets', build_rivets(), M_RIVET, coll, smooth=True)
    sub = sw.modifiers.new('Smooth', 'WEIGHTED_NORMAL'); sub.keep_sharp = True
    return coll

# ------------------------------------------------------------------ kitchen (inches; wall face y=0, room toward -y)
LEFT_X0, LEFT_X1 = -18.875-38.0, -18.875                 # upper left run 38 in
RIGHT_X0, RIGHT_X1 = 18.875, 18.875+17.0                 # upper right run 17 in; opening 37.75 in
ROOM_X0, ROOM_X1, ROOM_Y = -112.0, RIGHT_X1, -170.0
CEIL = 119.0
def shaker(bm, x0, x1, z0, z1, yface, frame=2.5, t=0.75, recess=0.25):
    """5-piece shaker door/drawer front on the plane y=yface (front at yface - t)"""
    yf = yface - t
    box(bm, x0, x1, yface, yface - (t-recess), z0, z1)                              # panel (recessed)
    box(bm, x0, x0+frame, yface, yf, z0, z1); box(bm, x1-frame, x1, yface, yf, z0, z1)  # stiles
    box(bm, x0+frame, x1-frame, yface, yf, z0, z0+frame); box(bm, x0+frame, x1-frame, yface, yf, z1-frame, z1)  # rails
def knob(bm, x, z, yface):
    cyl(bm, x, yface-0.75-0.5, z, 0.25, 1.0, 'Y', 16)
    bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=0.6*IN, matrix=Matrix.Translation(v(x, yface-0.75-1.15, z)))

cab = bmesh.new(); doors = bmesh.new(); knobs = bmesh.new()
# uppers: 12 in deep, 54 in AFF to the crown underside
for x0, x1, nd in ((LEFT_X0, LEFT_X1, 2), (RIGHT_X0, RIGHT_X1, 1)):
    box(cab, x0, x1, 0, -12, 54, CROWN_UNDER)
    wdt = (x1-x0)/nd
    for i in range(nd):
        a, b = x0+i*wdt+0.0625, x0+(i+1)*wdt-0.0625
        shaker(doors, a, b, 54.125, CROWN_UNDER-0.125, -12)
        kx = b-1.75 if (nd == 2 and i == 0) or (nd == 1) else a+1.75
        if nd == 1: kx = a+1.75                                                     # right run hinges right, knob toward hood
        knob(knobs, kx, 57.0, -12)
# bases: 34.5 in + 1.5 in top; 24 in deep, 4 in toe kick
toe = bmesh.new()
for x0, x1 in ((ROOM_X0+40, -15.0), (15.0, RIGHT_X1)):
    box(cab, x0, x1, 0, -21, 4, 34.5); box(toe, x0, x1, 0, -21, 0, 4)
    box(cab, x0, x1, -21, -24, 4, 34.5)
    n = max(1, round((x1-x0)/20)); wdt = (x1-x0)/n
    for i in range(n):
        a, b = x0+i*wdt+0.0625, x0+(i+1)*wdt-0.0625
        shaker(doors, a, b, 28.0, 34.25, -24, frame=2.0)                             # drawer
        shaker(doors, a, b, 4.25, 27.75, -24)                                        # door
        knob(knobs, (a+b)/2, 31.1, -24); knob(knobs, a+1.75 if i % 2 else b-1.75, 24.5, -24)
mesh_obj('Cabinet boxes', cab, M_CAB, kitchen, bevel=0.06)
mesh_obj('Cabinet doors (shaker)', doors, M_CAB, kitchen, bevel=0.06)
mesh_obj('Cabinet knobs', knobs, M_KNOB, kitchen, smooth=True)
mesh_obj('Toe kick', toe, M_TOE, kitchen)
# crown: 4.75 in, continuous over the uppers and the hood, cove profile projecting 3.5 in
prof = [(0, 0), (-0.6, 0), (-0.6, 0.4)] + [(-0.6 - 2.6*math.sin(a), 0.4 + 3.6*(1-math.cos(a))) for a in [i*math.pi/2/10 for i in range(1, 11)]] + [(-3.5, 4.2), (-3.5, 4.75), (0, 4.75)]
crown = bmesh.new()
def crown_run(x0, x1, yface):
    vs0 = [crown.verts.new(v(x0, yface+py, CROWN_UNDER+pz)) for py, pz in prof]
    vs1 = [crown.verts.new(v(x1, yface+py, CROWN_UNDER+pz)) for py, pz in prof]
    for i in range(len(prof)): crown.faces.new((vs0[i], vs0[(i+1) % len(prof)], vs1[(i+1) % len(prof)], vs1[i]))
    crown.faces.new(vs0); crown.faces.new(list(reversed(vs1)))
crown_run(LEFT_X0-3.5, RIGHT_X1, -12)
# left end return back to the wall
for i in range(1):
    vsA = [crown.verts.new(v(LEFT_X0+py, -12-3.5, CROWN_UNDER+pz)) for py, pz in prof]
    vsB = [crown.verts.new(v(LEFT_X0+py, 0, CROWN_UNDER+pz)) for py, pz in prof]
    for k in range(len(prof)): crown.faces.new((vsA[k], vsA[(k+1) % len(prof)], vsB[(k+1) % len(prof)], vsB[k]))
bmesh.ops.recalc_face_normals(crown, faces=crown.faces[:])
mesh_obj('Crown', crown, M_CAB, kitchen, smooth=False)
fl_ = bmesh.new(); box(fl_, LEFT_X1, RIGHT_X0, 0, -12.0, CROWN_UNDER, CROWN_UNDER+4.75); mesh_obj('Crown backer over hood', fl_, M_CAB, kitchen)
# frieze filler between crown and ceiling
fr = bmesh.new(); box(fr, LEFT_X0-3.5, RIGHT_X1, 0, -15.5, CROWN_UNDER+4.75, CEIL); mesh_obj('Soffit', fr, M_WALL, kitchen)
# countertop
ct = bmesh.new()
box(ct, ROOM_X0+40, -15.0, 0, -25.5, 34.5, 36.0); box(ct, 15.0, RIGHT_X1, 0, -25.5, 34.5, 36.0)
mesh_obj('Countertop', ct, M_GRANITE, kitchen, bevel=0.2)
# room shell
sh = bmesh.new()
box(sh, ROOM_X0, ROOM_X1, 0, 0.5, 0, CEIL)                                         # back wall (y 0..0.5)
mesh_obj('Back wall', sh, M_WALL, kitchen)
sp = bmesh.new()
box(sp, ROOM_X0+40, -15.0, -0.02, 0.0, 36.0, 54.0); box(sp, 15.0, ROOM_X1, -0.02, 0.0, 36.0, 54.0)   # backsplash 36-54
box(sp, -15.0, 15.0, -0.02, 0.0, 36.0, HOOD_BOT)                                   # behind the range up to the hood
mesh_obj('Backsplash', sp, M_SPLASH, kitchen)
rw = bmesh.new(); box(rw, ROOM_X1, ROOM_X1+0.5, 0, ROOM_Y, 0, CEIL); mesh_obj('Right wall', rw, M_WALL, kitchen)
lw = bmesh.new()                                                                    # left wall with a window (the daylight)
for (y0, y1, z0, z1) in ((0, -26, 0, CEIL), (-86, ROOM_Y, 0, CEIL), (-26, -86, 0, 38), (-26, -86, 98, CEIL)):
    box(lw, ROOM_X0-0.5, ROOM_X0, y0, y1, z0, z1)
mesh_obj('Left wall', lw, M_WALL, kitchen)
wf = bmesh.new()
for (y0, y1, z0, z1) in ((-26, -28, 38, 98), (-84, -86, 38, 98), (-26, -86, 38, 40), (-26, -86, 96, 98), (-55, -57, 40, 96), (-28, -84, 67, 68.5)):
    box(wf, ROOM_X0-0.5, ROOM_X0+0.75, y0, y1, z0, z1)
mesh_obj('Window frame', wf, M_WINFRAME, kitchen, bevel=0.1)
wg = bmesh.new(); box(wg, ROOM_X0-0.1, ROOM_X0, -28, -84, 40, 96)
wgo = mesh_obj('Window glass', wg, M_WINGLASS, kitchen); wgo.visible_shadow = False   # let daylight through (no caustics)
fl = bmesh.new(); box(fl, ROOM_X0, ROOM_X1, 0.5, ROOM_Y, -0.5, 0); mesh_obj('Floor', fl, M_FLOOR, kitchen)
fw = bmesh.new(); box(fw, ROOM_X0, ROOM_X1, ROOM_Y, ROOM_Y-0.5, 0, CEIL); mesh_obj('Front wall (behind camera)', fw, M_WALL, kitchen)
ce = bmesh.new(); box(ce, ROOM_X0, ROOM_X1, 0.5, ROOM_Y, CEIL, CEIL+0.5); mesh_obj('Ceiling', ce, M_CEIL, kitchen)
# under-cabinet LED strips (2700K, low)
led = bmesh.new()
for x0, x1 in ((LEFT_X0+1, LEFT_X1-1), (RIGHT_X0+1, RIGHT_X1-1)): box(led, x0, x1, -9.5, -10.25, 53.9, 54.0)
mesh_obj('LED strips', led, M_LED, kitchen)

# ------------------------------------------------------------------ 30 in pro range (Monogram ZGP304NTSS look)
rg = bmesh.new(); top = bmesh.new(); grate = bmesh.new(); burn = bmesh.new(); kn = bmesh.new(); gl = bmesh.new()
box(rg, -15, 15, -1.0, -27.0, 4.0, 35.0)                                           # body
box(rg, -15, 15, -0.5, -3.5, 35.0, 40.0)                                           # low backguard
box(rg, -15, 15, -27.0, -28.0, 5.0, 26.0)                                          # oven door face
box(rg, -14.6, 14.6, -26.0, -28.5, 28.0, 33.6)                                     # control panel lip
box(top, -15, 15, -3.5, -27.0, 35.0, 35.5)                                         # cooktop surface
box(gl, -10.5, 10.5, -28.0, -28.05, 10.0, 22.0)                                    # oven window
cyl(rg, 0, -30.2, 25.2, 0.55, 26.0, 'X', 24)                                       # tubular handle
for x in (-11.5, 11.5): cyl(rg, x, -29.1, 25.2, 0.35, 2.4, 'Y', 12)                # handle stand-offs
for i, x in enumerate((-11.0, -6.6, -2.2, 2.2, 6.6, 11.0)):
    cyl(kn, x, -29.2, 30.8, 0.95, 1.4, 'Y', 28); cyl(kn, x, -30.0, 30.8, 0.18, 0.3, 'Y', 8)
for (x, y) in ((-7.5, -9.0), (7.5, -9.0), (-7.5, -21.0), (7.5, -21.0)):
    cyl(burn, x, y, 35.85, 1.9, 0.7, 'Z', 32); cyl(burn, x, y, 36.3, 1.3, 0.25, 'Z', 32)
for gx0, gx1 in ((-14.6, -0.15), (0.15, 14.6)):                                    # two continuous cast-iron grates
    box(grate, gx0, gx1, -4.0, -4.6, 36.35, 37.1); box(grate, gx0, gx1, -26.0, -26.6, 36.35, 37.1)
    box(grate, gx0, gx0+0.6, -4.0, -26.6, 36.35, 37.1); box(grate, gx1-0.6, gx1, -4.0, -26.6, 36.35, 37.1)
    for k in range(1, 4):
        y = -4.0 - 22.6*k/4; box(grate, gx0, gx1, y+0.3, y-0.3, 36.35, 37.1)
    for k in range(1, 3):
        x = gx0 + (gx1-gx0)*k/3; box(grate, x-0.3, x+0.3, -4.0, -26.6, 36.35, 37.1)
mesh_obj('Range body', rg, M_SS, kitchen, bevel=0.08)
mesh_obj('Range cooktop', top, M_TOP, kitchen)
mesh_obj('Range grates', grate, M_IRON, kitchen, bevel=0.05)
mesh_obj('Range burners', burn, M_BURNER, kitchen, smooth=True)
mesh_obj('Range knobs', kn, M_SS, kitchen, smooth=True)
mesh_obj('Range oven window', gl, M_GLASS, kitchen)

# ------------------------------------------------------------------ hoods per option + scenes
hA = make_hood('A', M_A, M_A, False)
hB = make_hood('B', M_B, M_B, False)
hC = make_hood('C', M_A, M_BRASS, True)
base.collection.children.link(hA)
sB = bpy.data.scenes.new('B Limewash'); sC = bpy.data.scenes.new('C Brass band')
for scn, h in ((sB, hB), (sC, hC)):
    scn.collection.children.link(kitchen); scn.collection.children.link(h)

# ------------------------------------------------------------------ world, lights, cameras (in kitchen collection)
w = bpy.data.worlds.new('Interior'); w.use_nodes = True; wn = w.node_tree
env = wn.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(TEX, 'cayley_interior_2k.hdr'))
bg = [n for n in wn.nodes if n.type == 'BACKGROUND'][0]; wn.links.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.4
def light(name, kind, loc, energy, color, rot=(0, 0, 0), **kw):
    ld = bpy.data.lights.new(name, kind); ld.energy = energy; ld.color = color
    for k, val in kw.items(): setattr(ld, k, val)
    ob = bpy.data.objects.new(name, ld); ob.location = loc; ob.rotation_euler = rot; link(ob, kitchen)
    ob.visible_camera = False; return ob
# window daylight from camera-left: large area light just outside the left window, aimed into the room
light('Window daylight', 'AREA', v(ROOM_X0-14, -56, 68), 170, (1.0, 0.97, 0.92), (0, math.radians(-90), 0),   # emits +X, into the room
      shape='RECTANGLE', size=60*IN, size_y=58*IN)
light('Room bounce (behind camera)', 'AREA', v(-10, -150, 100), 15, (1.0, 0.97, 0.93), (math.radians(62), 0, 0), shape='RECTANGLE', size=110*IN, size_y=60*IN)
for nm_, x0, x1 in (('Under-cab L', LEFT_X0+1, LEFT_X1-1), ('Under-cab R', RIGHT_X0+1, RIGHT_X1-1)):
    light(nm_, 'AREA', v((x0+x1)/2, -9.9, 53.8), 3*(x1-x0)/36, (1.0, 0.70, 0.42), (0, 0, 0), shape='RECTANGLE', size=(x1-x0)*IN, size_y=0.8*IN)
light('Recessed can over hood', 'SPOT', v(0, -26, CEIL-0.5), 30, (1.0, 0.86, 0.70), (math.radians(14), 0, 0), 
      spot_size=math.radians(95), spot_blend=1.0, shadow_soft_size=1.0*IN)              # 3000K, tilted onto the chimney face
can = bmesh.new(); cyl(can, 0, -26, CEIL-0.05, 2.6, 0.1, 'Z', 32); mesh_obj('Recessed can trim', can, M_CEIL, kitchen, smooth=True)
cams = {}
def camera(name, eye, look_xy, lens=35, shift_y=0.0):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = 36; cd.sensor_fit = 'HORIZONTAL'
    cd.shift_y = shift_y; cd.clip_start = 0.05; cd.clip_end = 100
    ob = bpy.data.objects.new(name, cd); link(ob, kitchen); ob.location = v(*eye)
    d = Vector((look_xy[0]*IN - ob.location.x, look_xy[1]*IN - ob.location.y, 0))       # level camera: verticals stay vertical
    ob.rotation_euler = (math.radians(90), 0, math.atan2(d.y, d.x) - math.pi/2); cams[name] = ob; return ob
# 35 mm, eye 60 in. To frame hood + crown + uppers + range + a bit of counter at 35 mm the camera stands ~14 ft back;
# lens shift (not tilt) centres the frame on the hood while keeping verticals plumb.
camera('CAM 3-4 view', (-46, -172, 60), (0, 0), 35, 0.082)
camera('CAM straight-on', (0, -176, 60), (0, 0), 35, 0.080)
camera('CAM hood straight-on', (0, -118, 60), (0, 0), 35, 0.255)
camera('CAM closeup', (-20, -44, 78), (2, -12), 50, 0.0)

def setup(scn, cam):
    scn.world = w; scn.camera = cam; r = scn.render; r.engine = 'CYCLES'
    r.resolution_x, r.resolution_y, r.resolution_percentage = 1920, 1080, 100
    scn.cycles.samples = 256; scn.cycles.use_denoising = True; scn.cycles.denoiser = 'OPENIMAGEDENOISE'
    scn.cycles.use_adaptive_sampling = True; scn.cycles.adaptive_threshold = 0.01
    scn.cycles.max_bounces = 12; scn.cycles.sample_clamp_indirect = 6.0; scn.cycles.caustics_reflective = False; scn.cycles.caustics_refractive = False
    scn.view_settings.view_transform = 'AgX'; scn.view_settings.look = 'AgX - Medium High Contrast'; scn.view_settings.exposure = -0.25
    scn.unit_settings.system = 'IMPERIAL'; scn.unit_settings.length_unit = 'INCHES'
for scn in (base, sB, sC): setup(scn, cams['CAM hood straight-on'])

out = os.path.join(HERE, 'vanhove-hood.blend')
bpy.ops.wm.save_as_mainfile(filepath=out, relative_remap=True)
try: bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_mainfile()
except Exception as e: print('relative paths:', e)
print('SAVED', out)

if '--' in sys.argv and 'render' in sys.argv[sys.argv.index('--')+1:]:
    os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
    for scn, fn in ((base, 'option-A-marmorino-satin.png'), (sB, 'option-B-limewash.png'), (sC, 'option-C-brass-band.png')):
        scn.render.filepath = os.path.join(HERE, 'renders', fn); bpy.ops.render.render(write_still=True, scene=scn.name)
