# Cramers Landscaping pavilion - Blender scene setup v3  (Blender 4.2 LTS recommended, 3.6+ should work)
# Scripting workspace > Open > this file > Run Script.  Keep cramers_pavilion.glb in the same folder.
# Command line:  blender -b -P blender_setup.py            (builds the scene)
# Safe to re-run: it removes the previous import first.
#
# What changed from v2 (see CHANGES at the bottom of this file for the why):
#   - wood grain follows every individual board (beams, posts, siding, ceiling, benches) with board-to-board
#     color variation, growth rings and visible board seams, instead of one wavy pattern smeared over each wall
#   - shou sugi ban, Typhoon Bordeaux granite and salt-finish concrete rebuilt to read as the real materials
#   - real 3D lawn (instanced grass) + ground that runs to the horizon
#   - one sun: the HDRI's own sun is clamped out and replaced by a sun lamp placed exactly where it was
#   - optional photo textures for the cedar and the countertop (CEDAR_PHOTO / GRANITE_PHOTO)
import bpy, bmesh, os, math, json, random, urllib.request
from mathutils import Vector, Euler

GLB_PATH      = r""    # optional full path to cramers_pavilion.glb
USE_POLYHAVEN = True   # downloads a CC0 sky HDRI from Poly Haven (False = procedural Nishita sky, no internet)
USE_GRASS     = True   # instanced 3D grass around the pavilion (False = flat lawn shader only)
RENDER_ALL    = False  # True = render every CAM_ view into /renders when the script finishes
SAMPLES       = 256
RES           = (2400, 1350)
SUN_AZIMUTH   = -120.0 # degrees, direction the sun comes FROM (0=+X, -90=front/-Y). -120 = front-left
SUN_ELEVATION = 45.0   # degrees above the horizon; None = use the HDRI's own sun height
HDRI_NAME     = 'noon_grass'   # Poly Haven HDRI: open field ringed by a distant tree line
HDRI_RES      = '8k'           # it is also the visible backdrop: 2k is ~6 px/degree and looks blurry behind a 2400 px render
CAM_SUN       = {'CAM_06_Back_Right': 75.0}   # per-shot sun azimuth overrides (the back view is otherwise all in shade)
CAM_BG_TURN   = {'CAM_06_Back_Right': 60.0}   # per-shot backdrop turn (deg); CAM_06 otherwise has a ballfield stand over the roof
CAM_EXPOSURE  = {'CAM_01_Cover': 0.3, 'CAM_02_Bar_Stool_View': 0.9, 'CAM_03_Front_Right': 0.4,   # per-shot exposure (stops),
                 'CAM_04_Sauna_Doorway': 0.0, 'CAM_05_Sauna_Back_Bench': 0.0, 'CAM_06_Back_Right': 0.3, 'CAM_07_Bathroom': 0.3}  # like a photographer would
CEDAR_PHOTO   = r""    # optional photo of your cedar boards (jpg/png) - replaces the procedural cedar color
GRANITE_PHOTO = r"textures/typhoon_bordeaux_tile.jpg"   # tile made from the owner's photo of their Typhoon Bordeaux slab ("" = procedural)
GRANITE_TILE_M = (0.75, 1.03)   # real size of that tile in metres (across the bar, along the bar)

# ------------------------------------------------------------------ locate files
def base_dir():
    try: return os.path.dirname(os.path.abspath(__file__))
    except NameError: pass
    for t in bpy.data.texts:
        if t.filepath and t.filepath.endswith('.py'): return os.path.dirname(bpy.path.abspath(t.filepath))
    if bpy.data.filepath: return os.path.dirname(bpy.data.filepath)
    return os.getcwd()
BASE=os.path.dirname(GLB_PATH) if GLB_PATH else base_dir()
if not os.path.exists(os.path.join(BASE,'cramers_pavilion.glb')) and os.path.exists(os.path.join(os.getcwd(),'cramers_pavilion.glb')): BASE=os.getcwd()
GLB=GLB_PATH or os.path.join(BASE,'cramers_pavilion.glb')
if not os.path.exists(GLB): raise FileNotFoundError('cramers_pavilion.glb not found next to the script - set GLB_PATH at the top.')
TEX=os.path.join(BASE,'textures'); os.makedirs(TEX,exist_ok=True)
sc=bpy.context.scene

# ------------------------------------------------------------------ clean up a previous run, import
GROUPS=('Cramers_Pavilion','Pavilion','Roof','Enclosure','Enclosure_Siding','Sauna_Interior','Bath_Fixtures','Doors','Fan','Outdoor_Shower','Site')
for ob in list(bpy.data.objects):
    nm=ob.name.split('.')[0]
    if nm in GROUPS or nm.split('__')[0] in GROUPS or nm.startswith(('CAM_','LT_','CP_')) or nm in ('Sun','Cube','Light','Camera'):
        bpy.data.objects.remove(ob,do_unlink=True)
for coll in (bpy.data.meshes,bpy.data.materials,bpy.data.lights,bpy.data.cameras,bpy.data.node_groups):
    for d in list(coll):
        if d.users==0: coll.remove(d)
bpy.ops.import_scene.gltf(filepath=GLB)
sc.unit_settings.system='IMPERIAL'; sc.unit_settings.length_unit='FEET'
meshes=[ob for ob in bpy.data.objects if ob.type=='MESH' and ob.name.split('__')[0] in GROUPS]
def matname(ob): return ob.name.split('__')[-1].split('.')[0]

# ------------------------------------------------------------------ model edits on top of REV 14 (owner review)
from mathutils import Vector as V2, Matrix
def link_new(src,me,name):
    o=bpy.data.objects.new(name,me); (src.users_collection[0] if src.users_collection else sc.collection).objects.link(o)
    o.matrix_world=src.matrix_world.copy(); meshes.append(o); return o
def split_off(src,keep,name,mat):
    """move the faces matching keep(face) out of src into a new object with material mat"""
    me2=src.data.copy(); b2=bmesh.new(); b2.from_mesh(me2)
    bmesh.ops.delete(b2,geom=[f for f in b2.faces if not keep(f)],context='FACES'); b2.to_mesh(me2); b2.free()
    b1=bmesh.new(); b1.from_mesh(src.data)
    bmesh.ops.delete(b1,geom=[f for f in b1.faces if keep(f)],context='FACES'); b1.to_mesh(src.data); b1.free()
    me2.materials.clear(); me2.materials.append(mat); return link_new(src,me2,name)

# 1) bar baseboard (cedar kick plinth under the charred bar) -> black stain
pc=bpy.data.objects.get('Pavilion__cedar'); bstain=bpy.data.materials.get('black_stain')
if pc and bstain:
    split_off(pc,lambda f:all(0.35<v.co.x<0.72 and -4.48<v.co.y<-1.31 and v.co.z<0.145 for v in f.verts),
              'Pavilion__black_stain.bar_base',bstain)

# 1b) stray panel: a full-height cedar plane at x=5.309 stood 6 cm inside the enclosure's left wall, through both
#     the bath and the sauna (it cut through the vanity, mirror, sauna shelf and hooks). Remove it.
if pc:
    b=bmesh.new(); b.from_mesh(pc.data)
    stray=[f for f in b.faces if all(abs(v.co.x-5.309)<0.002 for v in f.verts) and min(v.co.z for v in f.verts)<0.01]
    bmesh.ops.delete(b,geom=stray,context='FACES'); b.to_mesh(pc.data); b.free()

# 1c) bathroom: cedar like the pavilion - flat T&G walls, beaded T&G ceiling (was painted drywall). The paint mesh also
#     ran behind the sauna's cedar walls (coplanar); that part is trimmed off so it can't flicker through.
bp=bpy.data.objects.get('Enclosure__bath_wall_paint')
wb=bpy.data.materials.get('cedar_wall_boards'); tg=bpy.data.materials.get('cedar_tg_ceiling')
if bp and wb and tg:
    b=bmesh.new(); b.from_mesh(bp.data); bmesh.ops.remove_doubles(b,verts=b.verts,dist=0.0004)
    bmesh.ops.bisect_plane(b,geom=b.verts[:]+b.edges[:]+b.faces[:],plane_co=(0,-2.40,0),plane_no=(0,-1,0),clear_outer=True)
    b.to_mesh(bp.data); b.free()
    on=lambda f,i,val:all(abs(v.co[i]-val)<0.004 for v in f.verts)
    split_off(bp,lambda f:on(f,0,5.246) or on(f,0,6.882) or on(f,1,-2.377) or on(f,1,-0.343),'Enclosure__cedar_wall_boards.bath',wb)
    split_off(bp,lambda f:on(f,2,2.438),'Enclosure__cedar_tg_ceiling.bathceiling',tg)

# 2) post bases like the West Ashley cabana: board-wrapped upper block on a wider plinth whose bottom edge is relieved
#    between the corners so it stands on feet (v2: plain solid boxes). Built along each base's real outline, so the
#    L-shaped bases of the posts engaged in the enclosure walls get the same treatment.
BASE_T=0.019; FOOT=0.05; FOOT_H=0.018
def outlines(bm,faces):
    """connected groups of horizontal faces -> CCW outline loops (2D) per group"""
    fs=set(faces); groups=[]; seen=set()
    for f0 in faces:
        if f0 in seen: continue
        g=[]; st=[f0]
        while st:
            f=st.pop()
            if f in seen: continue
            seen.add(f); g.append(f); st.extend(x for e in f.edges for x in e.link_faces if x in fs and x not in seen)
        groups.append(g)
    res=[]
    for g in groups:
        gs=set(g); nxt={}
        for f in g:
            for l in f.loops:
                if sum(1 for x in l.edge.link_faces if x in gs)==1: nxt[l.vert]=l.link_loop_next.vert
        while nxt:
            a0=next(iter(nxt)); pts=[a0]; a=nxt.pop(a0)
            while a is not a0 and a in nxt: pts.append(a); a=nxt.pop(a)
            P=[p.co.xy.copy() for p in pts]
            area=sum(P[i-1].x*P[i].y-P[i].x*P[i-1].y for i in range(len(P)))
            if area<0: P.reverse()
            Q=[]
            for i in range(len(P)):
                d1=(P[i]-P[i-1]).normalized(); d2=(P[(i+1)%len(P)]-P[i]).normalized()
                if abs(d1.cross(d2))>1e-4 or d1.dot(d2)<0: Q.append(P[i])
            if len(Q)>=3: res.append(Q)
    return res
def wrap_boards(bm,loop,z0,z1,feet):
    for i in range(len(loop)):
        a,b=loop[i],loop[(i+1)%len(loop)]; d=b-a; L=d.length
        if L<1e-3: continue
        u=d/L; inw=V2((-u.y,u.x))                     # CCW loop: inside is on the left
        s0=BASE_T                                       # every board butts into the previous one at its start
        prof=[(s0,z0)]
        if feet and L>2*FOOT+2*FOOT_H+0.03:
            prof+=[(FOOT,z0),(FOOT+FOOT_H,z0+FOOT_H),(L-FOOT-FOOT_H,z0+FOOT_H),(L-FOOT,z0)]
        prof+=[(L,z0),(L,z1),(s0,z1)]
        vo=[bm.verts.new((a.x+u.x*s,a.y+u.y*s,z)) for s,z in prof]
        vi=[bm.verts.new((a.x+u.x*s+inw.x*BASE_T,a.y+u.y*s+inw.y*BASE_T,z)) for s,z in prof]
        n=len(prof); bm.faces.new(vo); bm.faces.new(list(reversed(vi)))
        for k in range(n): bm.faces.new((vo[k],vo[(k+1)%n],vi[(k+1)%n],vi[k]))
pv=bpy.data.objects.get('Pavilion__cedar_vertical')
if pv:
    an=bmesh.new(); an.from_mesh(pv.data); bmesh.ops.remove_doubles(an,verts=an.verts,dist=0.0004)
    hz=lambda f,z,s:all(abs(v.co.z-z)<1e-3 for v in f.verts) and f.normal.z*s>0.9
    plinths=outlines(an,[f for f in an.faces if hz(f,0.0,-1)])
    uppers=outlines(an,[f for f in an.faces if hz(f,0.4330,1) or hz(f,0.4318,1)])
    zt=max((v.co.z for v in an.verts if v.co.z<0.44 and v.co.z>0.30),default=0.433); zm=0.1524
    an.free()
    if plinths and uppers:
        b=bmesh.new(); b.from_mesh(pv.data)
        bmesh.ops.delete(b,geom=[f for f in b.faces if f.calc_center_median().z<0.425],context='FACES'); b.to_mesh(pv.data); b.free()
        nb=bmesh.new()
        for lp in plinths: wrap_boards(nb,lp,0.0,zm,True)
        for lp in uppers:  wrap_boards(nb,lp,zm,zt,False)
        bmesh.ops.recalc_face_normals(nb,faces=nb.faces[:])
        me=bpy.data.meshes.new('post_bases'); nb.to_mesh(me); nb.free(); me.materials.append(pv.data.materials[0])
        link_new(pv,me,'Pavilion__cedar_vertical.bases')
        print(f'post bases rebuilt: {len(plinths)} plinths with feet, {len(uppers)} upper blocks')

# 3) sauna: the walk-in between the heater guard and the end of the lower bench was 22 cm. Pull the lower bench's
#    front end back 46 cm (front posts move back, the middle pair goes) -> ~68 cm clear past the heater.
SAUNA_BENCH_PULL=0.46
sauna=bpy.data.objects.get('Sauna_Interior__sauna_cedar')
if sauna:
    b=bmesh.new(); b.from_mesh(sauna.data)
    junk=[v for v in b.verts if (5.92<v.co.x<6.065 and -4.51<v.co.y<-4.365 and 0.555<v.co.z<0.99)      # cube "bucket" + stick
                             or (6.20<v.co.x<6.26 and -4.11<v.co.y<-4.00 and v.co.z<0.53)]           # middle bench posts
    bmesh.ops.delete(b,geom=junk,context='VERTS')
    # the floor kick board runs across the front of BOTH benches: stop it at the upper bench's front post
    # instead of dragging its end back with the lower bench (that left it lying diagonally across the floor)
    kick=[f for f in b.faces if all(v.co.z<0.1405 and -4.585<v.co.y<-4.555 for v in f.verts)]
    kx0=min((v.co.x for f in kick for v in f.verts),default=5.246)
    bmesh.ops.delete(b,geom=kick,context='FACES')
    for v in b.verts:
        if 5.85<v.co.x<6.29 and -4.60<v.co.y<-4.40 and v.co.z<0.565: v.co.y+=SAUNA_BENCH_PULL
    def box(x0,x1,y0,y1,z0,z1):
        bmesh.ops.create_cube(b,size=1.0,matrix=Matrix.Translation(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2))@Matrix.Diagonal((x1-x0,y1-y0,z1-z0,1)))
    box(kx0,5.845,-4.579,-4.560,0.0,0.14)                                                 # under the upper bench
    box(5.855,6.281,-4.579+SAUNA_BENCH_PULL,-4.560+SAUNA_BENCH_PULL,0.0,0.14)             # front of the shortened lower bench
    b.to_mesh(sauna.data); b.free()

# 4) bathroom: swap the water heater (was back-left corner) and the cedar shelves (were back wall, right of it)
wh=bpy.data.objects.get('Bath_Fixtures__appliance_white'); shv=bpy.data.objects.get('Bath_Fixtures__cedar')
if wh and shv:
    wh.data.transform(Matrix.Translation((6.882-5.745,0,0)))   # heater -> back-right corner, against the wall at x 6.88
    shv.data.transform(Matrix.Translation((5.246-5.791,0,0)))  # shelves -> start at the left wall

# ------------------------------------------------------------------ weld, rebuild boards, write grain attributes, bevels
# Every wood part gets two per-face-corner attributes the shaders read:
#   grain = position in the board's own frame (x runs ALONG the grain), plus a random per-board offset
#   board = (random value per board, 0-1 position across the board width, 1 if it's a flat board in a sheet;
#            2 = a big panel face: y holds the across position in metres and the shader cuts 5.5 in boards)
# Solid parts (beams, posts, slats) take the grain from their longest dimension. Flat sheets (siding, wall
# boards, T&G ceiling, sauna paneling) are split back into individual boards and each board runs along its
# own long edge - so a horizontal siding board, a vertical post and a ceiling board all get the right grain.
WOOD=('cedar','cedar_vertical','cedar_lap_siding','cedar_wall_boards','cedar_tg_ceiling','sauna_cedar','vanity_cedar','charred_cedar','black_stain')
def grain_attributes(bm,seed,horizontal=False):
    """frames follow the members' real directions, so sloped beams/rafters get grain parallel to their edges"""
    rng=random.Random(seed)
    bmesh.ops.join_triangles(bm,faces=bm.faces[:],angle_face_threshold=0.01,angle_shape_threshold=math.pi,
                             cmp_seam=False,cmp_sharp=False,cmp_uvs=False,cmp_vcols=False,cmp_materials=False)
    gl=bm.loops.layers.float_vector.new('grain'); bl=bm.loops.layers.float_vector.new('board')
    def long_dir(edges):
        es=[e for e in edges if e.calc_length()>1e-5]
        if horizontal:
            hz=[e for e in es if abs((e.verts[1].co-e.verts[0].co).normalized().z)<0.3]
            es=hz or es
        e=max(es,key=lambda e:e.calc_length()); d=(e.verts[1].co-e.verts[0].co).normalized()
        return d
    def pick():  # random distance to the tree's pith -> flat-sawn arches, slight taper -> cathedrals
        return (rng.uniform(0,40), rng.choice((-1,1))*rng.uniform(0.04,0.22), rng.choice((-1,1))*rng.uniform(0.04,0.22),
                rng.uniform(-0.012,0.012), rng.uniform(-0.012,0.012), rng.random())
    seen=set()
    for f0 in bm.faces:
        if f0 in seen: continue
        isl=[]; st=[f0]
        while st:
            f=st.pop()
            if f in seen: continue
            seen.add(f); isl.append(f)
            for e in f.edges: st.extend(g for g in e.link_faces if g not in seen)
        vs={v for f in isl for v in f.verts}
        ctr=sum((v.co for v in vs),Vector())/len(vs)
        solid=all(len(e.link_faces)==2 for f in isl for e in f.edges)
        U=long_dir({e for f in isl for e in f.edges})
        side=[f for f in isl if abs(f.normal.dot(U))<0.2]
        Vn=(max(side,key=lambda f:f.calc_area()).normal.copy() if side else U.orthogonal()).normalized()
        Wn=U.cross(Vn).normalized(); ip=pick()
        for f in isl:
            fu=long_dir(f.edges); fn=f.normal.copy().normalized(); fw=fn.cross(fu).normalized()
            if fw.z<-1e-4 or (abs(fw.z)<=1e-4 and (fw.x+fw.y)<0): fw=-fw          # 'across' runs bottom -> top
            pu=[v.co.dot(fu) for v in f.verts]; pw=[v.co.dot(fw) for v in f.verts]
            eu,ew=max(pu)-min(pu),max(pw)-min(pw)
            fc=f.calc_center_median()
            if eu>0.45 and ew>0.45:
                # a whole wall / panel modelled as one face: the shader cuts it into 5.5 in boards along its long side.
                # every face on the same wall plane shares one layout (a wall split into triangles used to get a
                # different board pattern per triangle -> a visible diagonal break across the wall)
                key=(round(fn.x,2),round(fn.y,2),round(fn.z,2),round(fc.dot(fn),2))
                pr=random.Random(hash(key)^seed); o=(pr.uniform(0,40),pr.choice((-1,1))*pr.uniform(0.04,0.22),pr.choice((-1,1))*pr.uniform(0.04,0.22),0,0,pr.random())
                fc=fn*fc.dot(fn)      # shared frame origin for the whole plane
                for l in f.loops:
                    p=l.vert.co-fc
                    l[gl]=(l.vert.co.dot(fu)+o[0], p.dot(fn)+o[1], p.dot(fw)+o[2]); l[bl]=(o[5], l.vert.co.dot(fw), 2.0)
                continue
            if solid: A,B,C,c,o,acr=U,Vn,Wn,ctr,ip,None
            else:     A,B,C,c,o,acr=fu,fn,fw,fc,pick(),(min(pw),max(ew,1e-6))
            for l in f.loops:
                p=l.vert.co-c; u=p.dot(A)
                l[gl]=(l.vert.co.dot(A)+o[0], p.dot(B)+o[1]+o[3]*u, p.dot(C)+o[2]+o[4]*u)
                l[bl]=(o[5], 0.5 if acr is None else (l.vert.co.dot(C)-acr[0])/acr[1], 0.0 if acr is None else 1.0)

LAP_BUTT=0.013   # 1/2 in butt: each lap-siding board tilts out at its bottom edge, with a real underside, like bevel siding
def lap_tilt(bm,center=(6.06,-2.90)):
    bmesh.ops.join_triangles(bm,faces=bm.faces[:],angle_face_threshold=0.01,angle_shape_threshold=math.pi,
                             cmp_seam=False,cmp_sharp=False,cmp_uvs=False,cmp_vcols=False,cmp_materials=False)
    bmesh.ops.split_edges(bm,edges=bm.edges[:])
    for f in list(bm.faces):
        if len(f.verts)!=4 or abs(f.normal.z)>0.3: continue
        zs=[v.co.z for v in f.verts]
        if max(zs)-min(zs)<0.05: continue
        c=f.calc_center_median(); n=Vector((f.normal.x,f.normal.y,0)).normalized()
        if n.dot(Vector((c.x-center[0],c.y-center[1],0)))<0: n=-n
        zmid=(max(zs)+min(zs))/2; bot=[v for v in f.verts if v.co.z<zmid]
        if len(bot)!=2: continue
        old=[v.co.copy() for v in bot]
        for v in bot: v.co+=n*LAP_BUTT
        a=bm.verts.new(old[0]); b_=bm.verts.new(old[1])
        bf=bm.faces.new((bot[0],bot[1],b_,a))
        bf.normal_update()
        if bf.normal.z>0: bf.normal_flip()

BEVEL_GROUPS=('Pavilion','Enclosure_Siding','Sauna_Interior','Bath_Fixtures','Doors')
for k,ob in enumerate(meshes):
    me=ob.data
    try:
        bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=0.0004)
        if matname(ob)=='cedar_lap_siding': lap_tilt(bm)
        if matname(ob) in WOOD: grain_attributes(bm,1000+k,horizontal=ob.name.endswith(('.bases','.bath')))  # base trim boards wrap horizontally
        bm.to_mesh(me); bm.free()
        ROUND=('appliance_white','porcelain','white_device')        # water heater, toilet, sink: smooth, keep crisp rims
        for p in me.polygons: p.use_smooth=matname(ob) in ROUND
        if matname(ob) in ROUND:
            sb=bmesh.new(); sb.from_mesh(me)
            for e in sb.edges:
                if len(e.link_faces)==2 and e.calc_face_angle(0)>math.radians(35): e.smooth=False
            sb.to_mesh(me); sb.free()
        if getattr(me,'has_custom_normals',False):
            try: me.free_normals_split()
            except Exception:
                bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True); bpy.context.view_layer.objects.active=ob
                try: bpy.ops.mesh.customdata_custom_splitnormals_clear()
                except Exception: pass
    except Exception as e: print('weld skipped',ob.name,e)
    if ob.name.split('__')[0] in BEVEL_GROUPS and 'glass' not in ob.name and 'light' not in ob.name:
        bv=ob.modifiers.new('Bevel','BEVEL'); bv.width=0.004; bv.segments=2; bv.limit_method='ANGLE'; bv.angle_limit=math.radians(30)

# ------------------------------------------------------------------ sauna bucket: the model's stand-in was a 12 cm cube with a
# 1 cm stick standing straight up out of it (removed above), which rendered like a glitch. Stave bucket + bands + resting ladle,
# on the (shortened) lower bench.
metal=bpy.data.materials.get('black_metal')
if sauna:
    import mathutils
    cx,cy,z0=5.992,-4.438+SAUNA_BENCH_PULL,0.559
    def part(name,build,mat,grain=False):
        b=bmesh.new(); build(b)
        if grain: grain_attributes(b,77)
        me=bpy.data.meshes.new(name); b.to_mesh(me); b.free(); me.materials.append(mat)
        o=bpy.data.objects.new(name,me); sauna.users_collection[0].objects.link(o); return o
    def bucket(b):
        bmesh.ops.create_cone(b,cap_ends=True,cap_tris=False,segments=20,radius1=0.07,radius2=0.084,depth=0.17)
        top=[f for f in b.faces if f.normal.z>0.9]; bmesh.ops.delete(b,geom=top,context='FACES')
        bmesh.ops.translate(b,verts=b.verts[:],vec=(cx,cy,z0+0.085))
    bk=part('Sauna_Interior__bucket',bucket,sauna.data.materials[0],grain=True)
    so=bk.modifiers.new('Wall','SOLIDIFY'); so.thickness=0.009; so.offset=-1
    def bands(b):
        for zz,rr in ((0.035,0.0735),(0.135,0.0805)):
            bmesh.ops.create_cone(b,cap_ends=False,segments=20,radius1=rr+0.002,radius2=rr+0.0025,depth=0.012,
                                  matrix=mathutils.Matrix.Translation((cx,cy,z0+zz)))
    bd=part('Sauna_Interior__bucket_bands',bands,metal or sauna.data.materials[0])
    so=bd.modifiers.new('Wall','SOLIDIFY'); so.thickness=0.002
    def ladle(b):
        R=mathutils.Matrix.Translation((cx+0.03,cy-0.01,z0+0.16))@mathutils.Matrix.Rotation(math.radians(28),4,'Y')
        bmesh.ops.create_cone(b,cap_ends=True,segments=10,radius1=0.0085,radius2=0.0075,depth=0.40,matrix=R@mathutils.Matrix.Translation((0,0,0.12)))
        bmesh.ops.create_uvsphere(b,u_segments=14,v_segments=8,radius=0.03,matrix=R@mathutils.Matrix.Translation((0,0,-0.09)))
    ld=part('Sauna_Interior__ladle',ladle,sauna.data.materials[0],grain=True)
    for p in ld.data.polygons: p.use_smooth=True

# ------------------------------------------------------------------ node helpers
class NT:
    """tiny wrapper so material graphs read top-to-bottom"""
    def __init__(s,nt): s.nt=nt; s.N=nt.nodes; s.L=nt.links
    def node(s,typ,**kw):
        n=s.N.new(typ)
        for k,v in kw.items():
            if k.startswith('i_'): s.set(n.inputs[k[2:].replace('_',' ')],v)
            else: setattr(n,k,v)
        return n
    def set(s,sock,v):
        if hasattr(v,'is_output') or hasattr(v,'links'): s.L.new(v,sock)
        else: sock.default_value=v
    def math(s,op,a,b=0.0,clamp=False):
        n=s.N.new('ShaderNodeMath'); n.operation=op; n.use_clamp=clamp; s.set(n.inputs[0],a); s.set(n.inputs[1],b); return n.outputs[0]
    def vmath(s,op,a,b=(0,0,0)):
        n=s.N.new('ShaderNodeVectorMath'); n.operation=op; s.set(n.inputs[0],a); s.set(n.inputs[1],b); return n.outputs[0]
    def mapr(s,x,a,b,c,d,interp='SMOOTHSTEP'):
        n=s.N.new('ShaderNodeMapRange'); n.interpolation_type=interp; n.clamp=True
        s.set(n.inputs['Value'],x); n.inputs['From Min'].default_value=a; n.inputs['From Max'].default_value=b
        n.inputs['To Min'].default_value=c; n.inputs['To Max'].default_value=d; return n.outputs['Result']
    def ramp(s,x,stops,interp='LINEAR'):
        r=s.N.new('ShaderNodeValToRGB'); r.color_ramp.interpolation=interp; el=r.color_ramp.elements
        def col(c): return (c,c,c,1) if isinstance(c,(int,float)) else (*c,1)
        el[0].position,el[0].color=stops[0][0],col(stops[0][1]); el[1].position,el[1].color=stops[-1][0],col(stops[-1][1])
        for pos,c in stops[1:-1]: e=el.new(pos); e.color=col(c)
        s.set(r.inputs['Fac'],x); return r.outputs['Color']
    def mix(s,a,b,fac,mode='MIX'):
        n=s.N.new('ShaderNodeMix'); n.data_type='RGBA'; n.blend_type=mode; n.clamp_result=False
        s.set(n.inputs[0],fac); s.set(n.inputs[6],a); s.set(n.inputs[7],b); return n.outputs[2]
    def mul(s,a,b): return s.mix(a,b,1.0,'MULTIPLY')
    def attr(s,name):
        n=s.N.new('ShaderNodeAttribute'); n.attribute_type='GEOMETRY'; n.attribute_name=name; return n
    def sepxyz(s,v):
        n=s.N.new('ShaderNodeSeparateXYZ'); s.set(n.inputs[0],v); return n.outputs
    def objco(s):
        return s.N.new('ShaderNodeTexCoord').outputs['Object']
def fresh(m):
    """clear a material to a single Principled BSDF"""
    m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    out=nt.nodes.new('ShaderNodeOutputMaterial'); b=nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(b.outputs[0],out.inputs['Surface']); return NT(nt),b,out
def bump(t,b,height,strength,dist):
    bp=t.node('ShaderNodeBump',i_Strength=strength,i_Distance=dist); t.set(bp.inputs['Height'],height)
    t.set(b.inputs['Normal'],bp.outputs['Normal']); return bp

# ------------------------------------------------------------------ wood
BOARD_W=0.1397   # 5.5 in face width for panels that were modelled as one big face
def board_inputs(t):
    """returns grain vector, per-board random, 0-1 across-board position, sheet flag (0 solid / 1 board)"""
    g=t.attr('grain').outputs['Vector']; bd=t.sepxyz(t.attr('board').outputs['Vector']); rnd0,acr0,sh0=bd[0],bd[1],bd[2]
    virt=t.math('GREATER_THAN',sh0,1.5)
    pos=t.math('DIVIDE',acr0,BOARD_W); idx=t.math('FLOOR',pos)
    wn=t.node('ShaderNodeTexWhiteNoise',noise_dimensions='1D'); t.set(wn.inputs['W'],t.math('ADD',idx,t.math('MULTIPLY',rnd0,17.0)))
    acr=t.math('ADD',acr0,t.math('MULTIPLY',virt,t.math('SUBTRACT',t.math('FRACT',pos),acr0)))
    rnd=t.math('ADD',rnd0,t.math('MULTIPLY',virt,t.math('SUBTRACT',wn.outputs['Value'],rnd0)))
    off=t.vmath('MULTIPLY',t.vmath('SUBTRACT',wn.outputs['Color'],(0.5,0.5,0.5)),(60.0,0.4,0.4))
    sv=t.N.new('ShaderNodeVectorMath'); sv.operation='SCALE'; t.set(sv.inputs[0],off); t.set(sv.inputs['Scale'],virt)
    g=t.vmath('ADD',g,sv.outputs[0])   # each virtual board gets its own slice of log
    return g,rnd,acr,t.math('MINIMUM',sh0,1.0),virt
# tones = list of linear-RGB colors picked per board; western red cedar runs from blonde to deep red-brown.
def wood(m,tones,rough=0.55,rings=0.30,lap=False,groove=0.75,ring_scale=70.0,streak=0.18,photo=None,coat=0.0,knots=0.0,sawn=0.0,jitter=0.11,groove_w=0.045,bead=False,lap_dark=0.55):
    t,b,out=fresh(m)
    g,rnd,across,sheet,_=board_inputs(t)
    # wobble the growth rings with low-frequency noise stretched along the grain
    st=t.vmath('MULTIPLY',g,(0.35,4.0,4.0))
    wn=t.node('ShaderNodeTexNoise',i_Scale=1.0,i_Detail=3.0); t.set(wn.inputs['Vector'],st)
    warp=t.vmath('MULTIPLY',t.vmath('SUBTRACT',wn.outputs['Color'],(0.5,0.5,0.5)),(0.0,0.07,0.07))
    gw=t.vmath('ADD',g,warp)
    wv=t.node('ShaderNodeTexWave',wave_type='RINGS',rings_direction='X',wave_profile='SAW',i_Scale=ring_scale,i_Distortion=0.0)
    t.set(wv.inputs['Vector'],gw)
    late=t.ramp(wv.outputs['Fac'],[(0.0,0.0),(0.55,0.08),(0.88,1.0),(1.0,0.35)])      # latewood band
    # fine fibre streaks + mid-scale blotches, both stretched along the grain
    fs=t.node('ShaderNodeTexNoise',i_Scale=1.0,i_Detail=6.0); t.set(fs.inputs['Vector'],t.vmath('MULTIPLY',g,(1.5,90.0,90.0)))
    fib=t.mapr(fs.outputs['Fac'],0.3,0.7,1.0-streak,1.0+streak*0.4,'LINEAR')
    bl=t.node('ShaderNodeTexNoise',i_Scale=1.0,i_Detail=2.0); t.set(bl.inputs['Vector'],t.vmath('MULTIPLY',g,(0.6,6.0,6.0)))
    blot=t.mapr(bl.outputs['Fac'],0.3,0.7,0.84,1.10,'LINEAR')
    if photo:
        img=bpy.data.images.load(photo,check_existing=True)
        tx=t.node('ShaderNodeTexImage',extension='MIRROR'); tx.image=img
        # photo x runs along the board: 1 photo width per ~1.2 m of board, random slice per board
        sx=t.sepxyz(g); uvx=t.math('MULTIPLY',sx[0],1/1.2); uvy=t.math('ADD',t.math('MULTIPLY',across,0.18),t.math('MULTIPLY',rnd,0.82))
        cv=t.node('ShaderNodeCombineXYZ'); t.set(cv.inputs[0],uvx); t.set(cv.inputs[1],uvy); t.set(tx.inputs['Vector'],cv.outputs[0])
        tone=tx.outputs['Color']
    else:
        stops=[(i/(len(tones)-1),c) for i,c in enumerate(tones)]
        tone=t.ramp(rnd,stops,'CONSTANT' if len(tones)>2 else 'LINEAR')
        tone=t.mix(tone,t.ramp(t.math('FRACT',t.math('MULTIPLY',rnd,7.31)),[(0,1-jitter),(1,1+jitter*0.8)]),1.0,'MULTIPLY')
    col=t.mix(tone,t.mix((1,1,1,1),(1-rings,1-rings*1.05,1-rings*1.15,1),late,'MIX'),1.0,'MULTIPLY')
    col=t.mix(col,fib,1.0,'MULTIPLY'); col=t.mix(col,blot,1.0,'MULTIPLY')
    # board seams (flat sheets only): thin dark V-groove at both long edges; lap siding also gets its drip shadow
    edge=t.math('MINIMUM',across,t.math('SUBTRACT',1.0,across))
    grv=t.math('MULTIPLY',t.mapr(edge,0.0,groove_w,1.0,0.0),sheet)
    if bead:   # beaded T&G: a second, finer bead line down the middle of every board
        grv=t.math('MAXIMUM',grv,t.math('MULTIPLY',t.mapr(t.math('ABSOLUTE',t.math('SUBTRACT',across,0.5)),0.0,0.016,0.85,0.0),sheet))
    shade=t.math('SUBTRACT',1.0,t.math('MULTIPLY',grv,groove))
    if lap:
        lapsh=t.math('MULTIPLY',t.mapr(across,0.0,0.22,1.0,0.0),sheet)
        shade=t.math('MULTIPLY',shade,t.math('SUBTRACT',1.0,t.math('MULTIPLY',lapsh,lap_dark)))
    col=t.mix(col,shade,1.0,'MULTIPLY')
    kn=None
    if knots:
        # small tight knots (West Ashley cabana cedar): dark core, warm halo, a few per metre of board
        # 2D in (along grain, across): a knot is a branch running through the board, so it shows on every face it crosses
        gx=t.sepxyz(g); kc=t.node('ShaderNodeCombineXYZ'); t.set(kc.inputs[0],t.math('MULTIPLY',gx[0],4.0)); t.set(kc.inputs[1],t.math('MULTIPLY',t.math('ADD',gx[1],gx[2]),7.0))
        kv=t.node('ShaderNodeTexVoronoi',voronoi_dimensions='2D',feature='F1',i_Scale=1.0,i_Randomness=0.9); t.set(kv.inputs['Vector'],kc.outputs[0])
        live=t.math('LESS_THAN',t.sepxyz(kv.outputs['Color'])[0],knots)
        ksize=t.mapr(t.sepxyz(kv.outputs['Color'])[1],0.0,1.0,0.05,0.13,'LINEAR')
        kd=t.math('DIVIDE',kv.outputs['Distance'],ksize)
        core=t.math('MULTIPLY',live,t.mapr(kd,0.82,0.92,1.0,0.0))
        rim=t.math('MULTIPLY',live,t.math('MULTIPLY',t.mapr(kd,0.80,0.92,0.0,1.0),t.mapr(kd,0.92,1.10,1.0,0.0)))
        halo=t.math('MULTIPLY',live,t.mapr(kd,1.0,2.0,1.0,0.0))
        col=t.mix(col,(0.80,0.68,0.58,1),halo,'MULTIPLY')
        ko=t.ramp(t.sepxyz(kv.outputs['Color'])[2],[(0.0,(0.16,0.065,0.022)),(1.0,(0.26,0.11,0.035))])
        ko=t.mix(ko,t.mapr(kd,0.0,0.85,0.55,1.05),1.0,'MULTIPLY')   # darker heart
        col=t.mix(col,ko,core)
        col=t.mix(col,(0.05,0.02,0.008,1),t.math('MULTIPLY',rim,0.8))
        kn=core
    t.set(b.inputs['Base Color'],col)
    rn=t.node('ShaderNodeTexNoise',i_Scale=1.0,i_Detail=2.0); t.set(rn.inputs['Vector'],t.vmath('MULTIPLY',g,(0.8,10.0,10.0)))
    r=t.math('ADD',t.mapr(rn.outputs['Fac'],0.3,0.7,rough-0.07,rough+0.07,'LINEAR'),t.math('MULTIPLY',grv,0.3))
    t.set(b.inputs['Roughness'],t.math('ADD',r,t.math('MULTIPLY',late,0.06)))
    if coat: b.inputs['Coat Weight'].default_value=coat; b.inputs['Coat Roughness'].default_value=0.25
    h=t.math('SUBTRACT',t.math('ADD',t.math('MULTIPLY',late,0.25),t.math('MULTIPLY',fs.outputs['Fac'],0.35)),t.math('MULTIPLY',grv,2.5))
    if sawn:
        # rough-sawn / resawn face: torn fibres along the grain plus faint band-saw marks across it
        fz=t.node('ShaderNodeTexNoise',i_Scale=1.0,i_Detail=8.0,i_Roughness=0.7); t.set(fz.inputs['Vector'],t.vmath('MULTIPLY',g,(3.0,180.0,180.0)))
        h=t.math('ADD',h,t.math('MULTIPLY',fz.outputs['Fac'],0.6*sawn))
    if lap: h=t.math('ADD',h,t.math('MULTIPLY',across,t.math('MULTIPLY',sheet,1.2)))
    if kn is not None: h=t.math('SUBTRACT',h,t.math('MULTIPLY',kn,0.4))
    bump(t,b,h,0.35,0.0015)

def charred(m):
    """shou sugi ban: long slim alligator blocks along the grain, near-black cracks, faint silvery sheen on the block faces;
    flat panels (the bar front) also get 5.5 in board seams so they read as charred boards, not one slab"""
    t,b,out=fresh(m)
    g,rnd,across,sheet,virt=board_inputs(t)
    cg=t.vmath('MULTIPLY',g,(11.0,95.0,95.0))
    v=t.node('ShaderNodeTexVoronoi',feature='DISTANCE_TO_EDGE',i_Scale=1.0,i_Randomness=0.85); t.set(v.inputs['Vector'],cg)
    vc=t.node('ShaderNodeTexVoronoi',feature='F1',i_Scale=1.0,i_Randomness=0.85); t.set(vc.inputs['Vector'],cg)
    crack=t.mapr(v.outputs['Distance'],0.0,0.045,1.0,0.0)
    cellv=t.sepxyz(vc.outputs['Color'])[0]
    nz=t.node('ShaderNodeTexNoise',i_Scale=1.0,i_Detail=8.0); t.set(nz.inputs['Vector'],t.vmath('MULTIPLY',g,(2.0,40.0,40.0)))
    wv=t.node('ShaderNodeTexWave',wave_type='RINGS',rings_direction='X',wave_profile='SAW',i_Scale=55.0); t.set(wv.inputs['Vector'],g)
    face=t.ramp(cellv,[(0.0,(0.019,0.018,0.017)),(1.0,(0.027,0.025,0.023))])
    face=t.mix(face,t.mapr(nz.outputs['Fac'],0.3,0.7,0.8,1.2,'LINEAR'),1.0,'MULTIPLY')
    face=t.mix(face,t.mapr(wv.outputs['Fac'],0.6,1.0,1.0,0.65),1.0,'MULTIPLY')
    edge=t.math('MINIMUM',across,t.math('SUBTRACT',1.0,across))
    seam=t.math('MULTIPLY',sheet,t.mapr(edge,0.0,0.03,1.0,0.0))
    dark=t.math('MAXIMUM',crack,seam)
    t.set(b.inputs['Base Color'],t.mix(face,(0.003,0.0028,0.0025,1),dark))
    t.set(b.inputs['Roughness'],t.mix(t.mapr(nz.outputs['Fac'],0.3,0.7,0.38,0.6,'LINEAR'),(0.95,0.95,0.95,1),dark))
    b.inputs['Specular IOR Level'].default_value=0.55
    h=t.math('SUBTRACT',t.math('ADD',t.mapr(v.outputs['Distance'],0.0,0.06,0.0,1.0),t.math('MULTIPLY',nz.outputs['Fac'],0.4)),t.math('MULTIPLY',seam,2.0))
    bump(t,b,h,0.3,0.002)

def granite(m,photo=None):
    """Typhoon Bordeaux style: flowing burgundy / wine / cream / grey swirls, built from 3-6 mm crystals
    (random per-crystal tone, black biotite, garnet), polished with a clear coat"""
    t,b,out=fresh(m); co=t.objco()
    if photo:
        # the photo tile is ~1 m long but the bar is 3.1 m: sample it twice (second copy turned 180 deg and shifted)
        # and blend the two through soft noise so the same cream cluster doesn't visibly repeat down the bar
        img=bpy.data.images.load(photo,check_existing=True)
        sc_=(1/GRANITE_TILE_M[0],1/GRANITE_TILE_M[1],1/GRANITE_TILE_M[1])
        ta=t.node('ShaderNodeTexImage',projection='BOX',projection_blend=0.2,extension='REPEAT'); ta.image=img
        t.set(ta.inputs['Vector'],t.vmath('MULTIPLY',co,sc_))
        tb=t.node('ShaderNodeTexImage',projection='BOX',projection_blend=0.2,extension='REPEAT'); tb.image=img
        t.set(tb.inputs['Vector'],t.vmath('MULTIPLY',t.vmath('ADD',t.vmath('MULTIPLY',co,(-1,-1,1)),(0.31,0.47,0.0)),sc_))
        nz=t.node('ShaderNodeTexNoise',i_Scale=1.6,i_Detail=2.0); t.set(nz.inputs['Vector'],co)
        hs=t.node('ShaderNodeHueSaturation'); hs.inputs['Saturation'].default_value=1.18; hs.inputs['Value'].default_value=0.94
        t.set(hs.inputs['Color'],t.mix(ta.outputs['Color'],tb.outputs['Color'],t.mapr(nz.outputs['Fac'],0.44,0.56,0.0,1.0)))
        t.set(b.inputs['Base Color'],hs.outputs['Color'])
    else:
        w1=t.node('ShaderNodeTexNoise',i_Scale=1.3,i_Detail=3.0); t.set(w1.inputs['Vector'],co)
        c1=t.vmath('ADD',co,t.vmath('MULTIPLY',t.vmath('SUBTRACT',w1.outputs['Color'],(0.5,0.5,0.5)),(0.6,0.6,0.6)))
        w2=t.node('ShaderNodeTexNoise',i_Scale=5.0,i_Detail=6.0); t.set(w2.inputs['Vector'],c1)
        c2=t.vmath('ADD',c1,t.vmath('MULTIPLY',t.vmath('SUBTRACT',w2.outputs['Color'],(0.5,0.5,0.5)),(0.10,0.10,0.10)))
        # crystals: sample the swirl pattern once per crystal so the stone is granular, not smooth like marble
        cr=t.node('ShaderNodeTexVoronoi',feature='F1',i_Scale=170.0,i_Randomness=1.0); t.set(cr.inputs['Vector'],c2)
        cpos=cr.outputs['Position']   # feature-point position, already in input space
        p=t.node('ShaderNodeTexNoise',i_Scale=2.2,i_Detail=10.0,i_Roughness=0.6); t.set(p.inputs['Vector'],cpos)
        cv=t.sepxyz(cr.outputs['Color'])
        pv=t.math('ADD',t.mapr(p.outputs['Fac'],0.32,0.68,0.0,1.0,'LINEAR'),t.math('MULTIPLY',t.math('SUBTRACT',cv[1],0.5),0.12))
        base=t.ramp(pv,[(0.00,(0.012,0.004,0.005)),(0.18,(0.045,0.008,0.010)),(0.32,(0.110,0.018,0.020)),
                        (0.44,(0.150,0.035,0.032)),(0.52,(0.300,0.200,0.160)),(0.58,(0.500,0.420,0.330)),
                        (0.68,(0.560,0.480,0.380)),(0.76,(0.330,0.270,0.240)),(0.84,(0.120,0.022,0.025)),
                        (1.00,(0.020,0.005,0.006))])
        base=t.mix(base,t.mapr(cv[2],0.0,1.0,0.72,1.22,'LINEAR'),1.0,'MULTIPLY')
        blk=t.math('LESS_THAN',cv[0],0.13); gar=t.math('MULTIPLY',t.math('GREATER_THAN',cv[0],0.13),t.math('LESS_THAN',cv[0],0.18))
        col=t.mix(base,(0.008,0.007,0.007,1),blk); col=t.mix(col,(0.13,0.018,0.025,1),gar)
        t.set(b.inputs['Base Color'],col)
    b.inputs['Roughness'].default_value=0.15
    b.inputs['Coat Weight'].default_value=1.0; b.inputs['Coat Roughness'].default_value=0.03; b.inputs['Coat IOR'].default_value=1.52

def concrete(m):
    """broom-free salt finish: light warm grey, soft mottling, scattered 3-8 mm salt pits"""
    t,b,out=fresh(m); co=t.objco()
    n1=t.node('ShaderNodeTexNoise',i_Scale=0.9,i_Detail=6.0,i_Roughness=0.55); t.set(n1.inputs['Vector'],co)
    base=t.ramp(n1.outputs['Fac'],[(0.30,(0.255,0.245,0.228)),(0.55,(0.300,0.290,0.272)),(0.72,(0.335,0.325,0.305))])
    n2=t.node('ShaderNodeTexNoise',i_Scale=140.0,i_Detail=2.0); t.set(n2.inputs['Vector'],co)
    fine=t.mapr(n2.outputs['Fac'],0.3,0.7,0.90,1.06,'LINEAR')
    vp=t.node('ShaderNodeTexVoronoi',feature='F1',i_Scale=32.0); t.set(vp.inputs['Vector'],co)
    pr=t.sepxyz(vp.outputs['Color'])[0]
    pit=t.math('MULTIPLY',t.mapr(vp.outputs['Distance'],0.05,0.17,1.0,0.0),t.math('LESS_THAN',pr,0.30))
    col=t.mix(base,fine,1.0,'MULTIPLY'); col=t.mix(col,t.mix((1,1,1,1),(0.62,0.61,0.60,1),pit),1.0,'MULTIPLY')
    t.set(b.inputs['Base Color'],col)
    t.set(b.inputs['Roughness'],t.math('ADD',0.80,t.math('MULTIPLY',pit,0.12)))
    bump(t,b,t.math('SUBTRACT',t.math('MULTIPLY',n2.outputs['Fac'],0.15),pit),0.45,0.003)

def lawn_ground(m):
    """ground under / beyond the grass: mown-turf colour with world-space variation and distance haze"""
    t,b,out=fresh(m)
    pos=t.N.new('ShaderNodeNewGeometry').outputs['Position']
    n1=t.node('ShaderNodeTexNoise',i_Scale=0.12,i_Detail=4.0); t.set(n1.inputs['Vector'],pos)
    base=t.ramp(n1.outputs['Fac'],[(0.3,(0.028,0.058,0.011)),(0.5,(0.040,0.078,0.015)),(0.7,(0.055,0.092,0.019))])
    n2=t.node('ShaderNodeTexNoise',i_Scale=6.0,i_Detail=8.0); t.set(n2.inputs['Vector'],pos)
    col=t.mix(base,t.mapr(n2.outputs['Fac'],0.3,0.7,0.70,1.12,'LINEAR'),1.0,'MULTIPLY')
    cam=t.N.new('ShaderNodeCameraData')
    haze=t.mapr(cam.outputs['View Distance'],60.0,1500.0,0.0,0.65)
    col=t.mix(col,(0.30,0.36,0.42,1),haze)
    t.set(b.inputs['Base Color'],col); b.inputs['Roughness'].default_value=0.95
    b.inputs['Specular IOR Level'].default_value=0.25
    bump(t,b,n2.outputs['Fac'],0.4,0.01)

def grass_blade(m):
    t,b,out=fresh(m)
    oi=t.N.new('ShaderNodeObjectInfo')
    col=t.ramp(oi.outputs['Random'],[(0.0,(0.045,0.095,0.016)),(0.35,(0.062,0.120,0.020)),(0.70,(0.082,0.140,0.024)),(1.0,(0.120,0.150,0.036))])
    pos=t.N.new('ShaderNodeNewGeometry').outputs['Position']
    n1=t.node('ShaderNodeTexNoise',i_Scale=0.12,i_Detail=4.0); t.set(n1.inputs['Vector'],pos)
    col=t.mix(col,t.mapr(n1.outputs['Fac'],0.3,0.7,0.80,1.15,'LINEAR'),1.0,'MULTIPLY')
    h=t.sepxyz(t.objco())[2]
    col=t.mix(col,t.mapr(h,0.0,0.07,0.55,1.10),1.0,'MULTIPLY')   # darker near the soil
    t.set(b.inputs['Base Color'],col); b.inputs['Roughness'].default_value=0.42
    b.inputs['Subsurface Weight'].default_value=0.0
    tr=t.N.new('ShaderNodeBsdfTranslucent'); t.set(tr.inputs['Color'],t.mix(col,(1.6,1.8,1.0,1),1.0,'MULTIPLY'))
    mx=t.N.new('ShaderNodeMixShader'); mx.inputs[0].default_value=0.30
    t.L.new(b.outputs[0],mx.inputs[1]); t.L.new(tr.outputs[0],mx.inputs[2]); t.L.new(mx.outputs[0],out.inputs['Surface'])

def simple(m,color=None,metal=None,rough=None):
    m.use_nodes=True; b=[n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'][0]
    if color:
        for l in list(b.inputs['Base Color'].links): m.node_tree.links.remove(l)
        b.inputs['Base Color'].default_value=(*color,1)
    if metal is not None: b.inputs['Metallic'].default_value=metal
    if rough is not None: b.inputs['Roughness'].default_value=rough
    return b
def emissive(m,strength,color=None):
    b=simple(m,color); col=tuple(b.inputs['Base Color'].default_value)
    b.inputs['Emission Color'].default_value=col; b.inputs['Emission Strength'].default_value=strength

def ok(p):
    if p and not os.path.isabs(p): p=os.path.join(BASE,p)
    return p if p and os.path.exists(p) else None
cedar_photo=ok(CEDAR_PHOTO); granite_photo=ok(GRANITE_PHOTO)
# per-board tone sets (linear RGB). Sealed western red cedar: honey, amber, salmon, red-brown, the odd dark board.
CEDAR       =[(0.56,0.22,0.050),(0.50,0.19,0.042),(0.60,0.25,0.058),(0.46,0.17,0.038),(0.54,0.215,0.050),(0.62,0.27,0.065),(0.52,0.20,0.045)]
CEDAR_SIDING=[(0.52,0.20,0.046),(0.46,0.172,0.039),(0.56,0.225,0.052),(0.43,0.158,0.035),(0.50,0.192,0.044),(0.58,0.24,0.056)]
CEDAR_CEIL  =[(0.60,0.25,0.060),(0.54,0.215,0.051),(0.64,0.28,0.068),(0.50,0.195,0.046),(0.58,0.24,0.057)]
SAUNA       =[(0.64,0.33,0.12),(0.58,0.29,0.10),(0.68,0.36,0.135),(0.54,0.26,0.09),(0.62,0.31,0.11)]   # unfinished, smooth, paler
VANITY      =[(0.12,0.050,0.022),(0.10,0.042,0.018),(0.14,0.060,0.027)]
BLACKSTAIN  =[(0.016,0.014,0.013),(0.013,0.012,0.011),(0.019,0.017,0.015)]
for m in bpy.data.materials:
    base=m.name.split('.')[0]
    try:
        if   base in ('cedar','cedar_vertical'): wood(m,CEDAR,rough=0.70,rings=0.26,ring_scale=40.0,photo=cedar_photo,knots=0.28,sawn=0.6,jitter=0.07)
        elif base=='cedar_lap_siding':  wood(m,CEDAR_SIDING,rough=0.66,rings=0.38,ring_scale=50.0,lap=True,lap_dark=0.25,groove=0.3,groove_w=0.01,photo=cedar_photo,knots=0.22,sawn=0.6,jitter=0.08)   # real lap geometry now
        elif base=='cedar_wall_boards': wood(m,CEDAR,rough=0.62,rings=0.38,ring_scale=50.0,groove=0.8,groove_w=0.018,photo=cedar_photo,knots=0.22,jitter=0.08)   # flat T&G: tight joint, no bead
        elif base=='cedar_tg_ceiling':  wood(m,CEDAR_CEIL,rings=0.38,ring_scale=50.0,bead=True,photo=cedar_photo,knots=0.18,jitter=0.08)   # beaded T&G
        elif base=='sauna_cedar':       wood(m,SAUNA,rough=0.72,rings=0.22,jitter=0.07)   # clear (knot-free) sauna grade
        elif base=='vanity_cedar':      wood(m,VANITY,rough=0.40,rings=0.35,coat=0.4)
        elif base=='black_stain':       wood(m,BLACKSTAIN,rough=0.42,rings=0.35,streak=0.25)
        elif base=='charred_cedar':     charred(m)
        elif base=='granite_typhoon_bordeaux': granite(m,granite_photo)
        elif base=='concrete_salt_finish': concrete(m)
        elif base=='lawn':              lawn_ground(m)
        elif base=='standing_seam_charcoal': simple(m,(0.040,0.043,0.047),0.85,0.38)
        elif base=='glass':
            b=simple(m,(1,1,1),0.0,0.0); b.inputs['Transmission Weight'].default_value=1.0; b.inputs['IOR'].default_value=1.5
        elif base=='quartz_white':      # vanity top -> black (honed/polished absolute-black look)
            b=simple(m,(0.010,0.010,0.011),0.0,0.18); b.inputs['Coat Weight'].default_value=0.6; b.inputs['Coat Roughness'].default_value=0.06
        elif base=='fan_bronze':        simple(m,(0.030,0.020,0.014),0.25,0.62)   # was half-metal/glossy: blades mirrored the sky white
        elif base=='mirror':            simple(m,(0.92,0.92,0.92),1.0,0.02)
        elif base=='lantern_glass':     emissive(m,6.0)
        elif base=='sauna_light':       emissive(m,4.0,(1.0,0.62,0.30))   # v2: strength 10 white -> clipped white square
        elif base=='led_strip':         emissive(m,25.0)
        elif base=='fan_light':         emissive(m,4.0)
    except Exception as e:
        print('material',m.name,'kept as imported:',e)

# ------------------------------------------------------------------ ground to the horizon + 3D lawn
lawn_ob=next((o for o in meshes if matname(o)=='lawn'),None)
lawn_mat=bpy.data.materials.get('lawn')
if lawn_ob:
    z=min((lawn_ob.matrix_world@v.co).z for v in lawn_ob.data.vertices)-0.006
    me=bpy.data.meshes.new('Site__ground_far'); S=3000.0
    me.from_pydata([(-S,-S,z),(S,-S,z),(S,S,z),(-S,S,z)],[],[(0,1,2,3)]); me.materials.append(lawn_mat)
    gf=bpy.data.objects.new('Site__ground_far',me); (lawn_ob.users_collection[0] if lawn_ob.users_collection else sc.collection).objects.link(gf)
if lawn_ob and USE_GRASS:
    # one clump = 16 curved, tapered blades; instanced ~200k times around the pavilion
    r=random.Random(7); bm=bmesh.new()
    for i in range(16):
        a=r.uniform(0,2*math.pi); rad=r.uniform(0,0.03); x0,y0=rad*math.cos(a),rad*math.sin(a)
        h=r.uniform(0.05,0.09); w=r.uniform(0.0016,0.0028); face=r.uniform(0,math.pi); lean=r.uniform(0.05,0.30)*h; ld=r.uniform(0,2*math.pi)
        px,py=math.cos(face),math.sin(face); rows=[]
        for k in range(5):
            s=k/4; cx=x0+lean*s*s*math.cos(ld); cy=y0+lean*s*s*math.sin(ld); cz=h*s*(1-0.12*s*s); hw=w*(1-s)**0.8
            rows.append((bm.verts.new((cx-px*hw,cy-py*hw,cz)),bm.verts.new((cx+px*hw,cy+py*hw,cz))) if k<4 else (bm.verts.new((cx,cy,cz)),))
        for k in range(3): bm.faces.new((rows[k][0],rows[k][1],rows[k+1][1],rows[k+1][0]))
        bm.faces.new((rows[3][0],rows[3][1],rows[4][0]))
    cm=bpy.data.meshes.new('CP_grass_clump'); bm.to_mesh(cm); bm.free()
    gm=bpy.data.materials.new('grass_blade'); grass_blade(gm); cm.materials.append(gm)
    for p in cm.polygons: p.use_smooth=True
    clump=bpy.data.objects.new('CP_grass_clump',cm); sc.collection.objects.link(clump)
    clump.hide_render=True; clump.hide_viewport=True; clump.location=(0,0,-50)
    ng=bpy.data.node_groups.new('CP_LawnGrass','GeometryNodeTree')
    ng.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry')
    ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    t=NT(ng); gi=t.N.new('NodeGroupInput'); go=t.N.new('NodeGroupOutput')
    # grass is scattered on its own 90 m patch centred on the pavilion and thins out with distance, so there is
    # no hard line where the lawn mesh ends; past ~40 m only the flat lawn shader remains (sub-pixel detail anyway)
    zl=min((lawn_ob.matrix_world@v.co).z for v in lawn_ob.data.vertices)
    gr=t.node('GeometryNodeMeshGrid',i_Size_X=90.0,i_Size_Y=90.0,i_Vertices_X=2,i_Vertices_Y=2)
    tg=t.N.new('GeometryNodeTransform'); t.L.new(gr.outputs['Mesh'],tg.inputs['Geometry']); tg.inputs['Translation'].default_value=(3.5,-3.0,zl)
    dp=t.node('GeometryNodeDistributePointsOnFaces',distribute_method='RANDOM',i_Density=320.0,i_Seed=11); t.L.new(tg.outputs[0],dp.inputs['Mesh'])
    pos=t.N.new('GeometryNodeInputPosition').outputs[0]; p=t.sepxyz(pos)
    m_=0.04   # keep blades 4 cm clear of the slab edge so none poke through it
    inside=t.math('MULTIPLY',t.math('MULTIPLY',t.math('GREATER_THAN',p[0],-0.33-m_),t.math('LESS_THAN',p[0],7.34+m_)),
                             t.math('MULTIPLY',t.math('GREATER_THAN',p[1],-6.12-m_),t.math('LESS_THAN',p[1],0.01+m_)))
    dist=t.N.new('ShaderNodeVectorMath'); dist.operation='DISTANCE'; t.L.new(pos,dist.inputs[0]); dist.inputs[1].default_value=(3.5,-3.0,0.0)
    thin=t.mapr(dist.outputs['Value'],12.0,42.0,0.0,1.0,'SMOOTHSTEP')
    rv=t.node('FunctionNodeRandomValue',data_type='FLOAT',i_Seed=3)
    cull=t.math('MAXIMUM',inside,t.math('LESS_THAN',rv.outputs[1],thin))
    dg=t.node('GeometryNodeDeleteGeometry',domain='POINT'); t.L.new(dp.outputs['Points'],dg.inputs['Geometry']); t.set(dg.inputs['Selection'],cull)
    oi=t.node('GeometryNodeObjectInfo'); oi.inputs['Object'].default_value=clump
    rr=t.node('FunctionNodeRandomValue',data_type='FLOAT_VECTOR',i_Seed=5); rr.inputs['Min'].default_value=(-0.15,-0.15,0); rr.inputs['Max'].default_value=(0.15,0.15,6.283)
    rs=t.node('FunctionNodeRandomValue',data_type='FLOAT',i_Seed=9); rs.inputs[2].default_value=0.75; rs.inputs[3].default_value=1.3
    io=t.N.new('GeometryNodeInstanceOnPoints'); t.L.new(dg.outputs[0],io.inputs['Points']); t.L.new(oi.outputs['Geometry'],io.inputs['Instance'])
    t.L.new(rr.outputs[0],io.inputs['Rotation']); t.L.new(rs.outputs[1],io.inputs['Scale'])
    jg=t.N.new('GeometryNodeJoinGeometry'); t.L.new(io.outputs[0],jg.inputs[0]); t.L.new(gi.outputs[0],jg.inputs[0]); t.L.new(jg.outputs[0],go.inputs[0])
    lawn_ob.modifiers.new('Grass','NODES').node_group=ng

# ------------------------------------------------------------------ optional Poly Haven HDRI (CC0)
def ph_json(url):
    req=urllib.request.Request(url,headers={'User-Agent':'cramers-pavilion-setup'})
    with urllib.request.urlopen(req,timeout=30) as r: return json.loads(r.read().decode())
def ph_get(url,dest):
    if os.path.exists(dest) and os.path.getsize(dest)>1000: return dest
    req=urllib.request.Request(url,headers={'User-Agent':'cramers-pavilion-setup'})
    with urllib.request.urlopen(req,timeout=120) as r, open(dest,'wb') as f: f.write(r.read())
    return dest
hdri=None
local=os.path.join(TEX,f'{HDRI_NAME}_{HDRI_RES}.hdr')
if os.path.exists(local): hdri=local
elif USE_POLYHAVEN:
    try:
        files=ph_json('https://api.polyhaven.com/files/'+HDRI_NAME)
        url=files['hdri'][HDRI_RES]['hdr']['url']; hdri=ph_get(url,local); print('Poly Haven HDRI downloaded')
    except Exception as e:
        print('Poly Haven download skipped (offline or API change) - using Nishita sky:',e)

# ------------------------------------------------------------------ world + ONE sun
# The HDRI contains its own sun (about half its light). v2 added a second sun lamp from a different angle on top,
# giving two suns / double shadows. Here the HDRI is clamped (sun removed) and a sun lamp is put exactly where the
# HDRI's sun was, with the same irradiance; the HDRI is rotated so that sun sits at SUN_AZIMUTH.
w=sc.world or bpy.data.worlds.new('World'); sc.world=w; w.use_nodes=True; wn=w.node_tree
for n in list(wn.nodes):
    if n.type not in ('BACKGROUND','OUTPUT_WORLD'): wn.nodes.remove(n)
bg=[n for n in wn.nodes if n.type=='BACKGROUND'][0]
sun_dir=None; sun_E=4.0; mp=None; m2=None; sky=None; s_phi=0.0; s_el=math.radians(SUN_ELEVATION or 45)
if hdri:
    import numpy as np
    img=bpy.data.images.load(hdri,check_existing=True); W,H=img.size
    px=np.empty(W*H*4,dtype=np.float32); img.pixels.foreach_get(px); px=px.reshape(H,W,4)
    lum=0.2126*px[...,0]+0.7152*px[...,1]+0.0722*px[...,2]
    CLAMP=float(max(np.percentile(lum,99.9)*1.2,3.0))
    el=((np.arange(H)+0.5)/H-0.5)*math.pi; dOm=(2*math.pi/W)*(math.pi/H)*np.cos(el)[:,None]
    iy,ix=np.unravel_index(np.argmax(lum),lum.shape)
    s_el=((iy+0.5)/H-0.5)*math.pi; s_phi=(0.5-(ix+0.5)/W)*2*math.pi
    sun_E=float(((lum-CLAMP).clip(min=0)*dOm).sum())          # irradiance of the clipped-off sun, facing it
    rot=s_phi-math.radians(SUN_AZIMUTH)
    if SUN_ELEVATION is not None: s_el=math.radians(SUN_ELEVATION)
    sun_dir=Vector((math.cos(math.radians(SUN_AZIMUTH))*math.cos(s_el),math.sin(math.radians(SUN_AZIMUTH))*math.cos(s_el),math.sin(s_el)))
    env=wn.nodes.new('ShaderNodeTexEnvironment'); env.image=img
    tc=wn.nodes.new('ShaderNodeTexCoord'); mp=wn.nodes.new('ShaderNodeMapping'); mp.inputs['Rotation'].default_value=(0,0,rot)
    wn.links.new(tc.outputs['Generated'],mp.inputs['Vector']); wn.links.new(mp.outputs['Vector'],env.inputs['Vector'])
    cl=wn.nodes.new('ShaderNodeVectorMath'); cl.operation='MINIMUM'; cl.inputs[1].default_value=(CLAMP,CLAMP,CLAMP)
    wn.links.new(env.outputs['Color'],cl.inputs[0]); wn.links.new(cl.outputs[0],bg.inputs['Color']); bg.inputs['Strength'].default_value=1.0
    print(f'HDRI sun: elevation {math.degrees(s_el):.1f} deg, irradiance {sun_E:.2f}, sky clamp {CLAMP:.2f}')
    # far ground: beyond ~60 m fade the lawn into the HDRI's own photographed field (same view direction, same
    # rotation and clamp), so the CG lawn runs seamlessly into the real tree line instead of a ruler-straight edge
    lm=bpy.data.materials.get('lawn')
    if lm:
        t=NT(lm.node_tree); out=[n for n in t.N if n.type=='OUTPUT_MATERIAL'][0]; surf=out.inputs['Surface'].links[0].from_socket
        geo=t.N.new('ShaderNodeNewGeometry'); vd=t.vmath('SCALE',geo.outputs['Incoming']); vd.node.inputs['Scale'].default_value=-1.0
        m2=t.N.new('ShaderNodeMapping'); m2.inputs['Rotation'].default_value=(0,0,rot); t.L.new(vd,m2.inputs['Vector'])
        e2=t.N.new('ShaderNodeTexEnvironment'); e2.image=img; t.L.new(m2.outputs['Vector'],e2.inputs['Vector'])
        c2=t.vmath('MINIMUM',e2.outputs['Color'],(CLAMP,CLAMP,CLAMP))
        em=t.N.new('ShaderNodeEmission'); t.L.new(c2,em.inputs['Color'])
        f2=t.mapr(t.N.new('ShaderNodeCameraData').outputs['View Distance'],60.0,260.0,0.0,1.0)
        ms=t.N.new('ShaderNodeMixShader'); t.L.new(f2,ms.inputs[0]); t.L.new(surf,ms.inputs[1]); t.L.new(em.outputs[0],ms.inputs[2])
        t.L.new(ms.outputs[0],out.inputs['Surface'])
else:
    sky=wn.nodes.new('ShaderNodeTexSky'); sky.sky_type='NISHITA'; sky.sun_disc=False
    sky.sun_elevation=math.radians(SUN_ELEVATION or 45); sky.sun_rotation=math.radians(SUN_AZIMUTH)
    wn.links.new(sky.outputs['Color'],bg.inputs['Color']); bg.inputs['Strength'].default_value=0.35
    e=math.radians(SUN_ELEVATION or 45); sun_dir=Vector((math.cos(math.radians(SUN_AZIMUTH))*math.cos(e),math.sin(math.radians(SUN_AZIMUTH))*math.cos(e),math.sin(e)))
sd=bpy.data.lights.new('Sun','SUN'); sd.energy=sun_E; sd.angle=math.radians(0.8); sd.color=(1.0,0.97,0.92)
sun=bpy.data.objects.new('Sun',sd); sc.collection.objects.link(sun)
sun.rotation_euler=(-sun_dir).to_track_quat('-Z','Y').to_euler()
def aim_sun(az_deg,frame=None,bg_turn=0.0):
    """point the sun lamp from az_deg and turn the HDRI (sky + far-ground blend) with it so they stay matched"""
    az=math.radians(az_deg)
    d=Vector((math.cos(az)*math.cos(s_el),math.sin(az)*math.cos(s_el),math.sin(s_el)))
    sun.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
    keyed=[(sun,'rotation_euler')]
    for node in (mp,m2):
        if node: node.inputs['Rotation'].default_value=(0,0,s_phi-az+math.radians(bg_turn)); keyed.append((node.inputs['Rotation'],'default_value'))
    if sky: sky.sun_rotation=az; keyed.append((sky,'sun_rotation'))
    if frame is not None:
        for owner,prop in keyed: owner.keyframe_insert(prop,frame=frame)

# ------------------------------------------------------------------ interior lights + cameras (meters, Blender coords)
for (name,loc,kind,watts,col) in [
    ('LT_Sauna',(6.064, -3.9929, 1.80),'POINT',18,(1.0, 0.72, 0.42)),   # soft fill only now; the recessed cans below do the lighting
    ('LT_Bath',(6.096, -1.3411, 2.3165),'POINT',40,(1.0, 0.9, 0.78)),
    ('LT_Sconce_L',(4.9987, -1.6459, 1.8288),'POINT',12,(1.0, 0.75, 0.45)),
    ('LT_Sconce_R',(4.9987, -4.1453, 1.8288),'POINT',12,(1.0, 0.75, 0.45)),
    ('LT_Fan',(2.7432, -2.8956, 2.570),'AREA',25,(1.0, 0.9, 0.8)),     # v2: point light 21 cm below the blades lit them white + threw blade shadows on the ceiling
]:
    ld=bpy.data.lights.new(name,kind); ld.energy=watts; ld.color=col
    if kind=='AREA': ld.shape='DISK'; ld.size=0.11          # area lights face down (-Z): nothing goes up into the blades
    else: ld.shadow_soft_size=0.25 if name=='LT_Sauna' else 0.08
    ob=bpy.data.objects.new(name,ld); ob.location=loc; sc.collection.objects.link(ob)
    ob.visible_camera=False; ob.visible_glossy=False; ob.visible_transmission=False           # the fixtures' own glowing glass is what you should see, not a light ball
# recessed cans in the sauna ceiling: brushed trim ring + warm frosted lens, each with a downward spot light
SAUNA_CANS=[(6.10,-4.80),(6.10,-3.90),(6.10,-3.00)]
if sauna:
    zc=max((sauna.matrix_world@v.co).z for v in sauna.data.vertices)        # ceiling underside (2.134 m)
    trim=bpy.data.materials.new('recessed_trim'); tb=simple(trim,(0.62,0.61,0.58),1.0,0.32)
    lens=bpy.data.materials.new('recessed_lens'); emissive(lens,7.0,(1.0,0.80,0.55)); simple(lens,None,0.0,0.4)
    tm=bmesh.new(); lm=bmesh.new()
    for (x,y) in SAUNA_CANS:
        bmesh.ops.create_cone(tm,cap_ends=True,segments=32,radius1=0.052,radius2=0.048,depth=0.006,matrix=Matrix.Translation((x,y,zc-0.003)))
        bmesh.ops.create_circle(lm,cap_ends=True,segments=32,radius=0.034,matrix=Matrix.Translation((x,y,zc-0.0065)))
    for nm_,bb,mt in (('Sauna_Interior__recessed_trim',tm,trim),('Sauna_Interior__recessed_lens',lm,lens)):
        bmesh.ops.recalc_face_normals(bb,faces=bb.faces[:])
        if nm_.endswith('lens'):
            for fc in bb.faces:
                if fc.normal.z>0: fc.normal_flip()
        me=bpy.data.meshes.new(nm_); bb.to_mesh(me); bb.free(); me.materials.append(mt)
        o=bpy.data.objects.new(nm_,me); sauna.users_collection[0].objects.link(o)
    for i,(x,y) in enumerate(SAUNA_CANS):
        ld=bpy.data.lights.new(f'LT_Sauna_Can_{i+1}','SPOT'); ld.energy=14; ld.color=(1.0,0.78,0.52)
        ld.spot_size=math.radians(110); ld.spot_blend=0.6; ld.shadow_soft_size=0.03
        ob=bpy.data.objects.new(ld.name,ld); ob.location=(x,y,zc-0.01); sc.collection.objects.link(ob)
        ob.visible_camera=False; ob.visible_glossy=False; ob.visible_transmission=False
# vanity light: black bar fixture with a frosted lens above the mirror + a soft area light
bm_=bpy.data.materials.get('black_metal')
if bm_:
    vb=bmesh.new(); yc=-1.415; zc=2.05
    bmesh.ops.create_cube(vb,size=1,matrix=Matrix.Translation((5.258,yc,zc))@Matrix.Diagonal((0.024,0.62,0.09,1)))         # backplate
    for dy in (-0.25,0.25):
        bmesh.ops.create_cube(vb,size=1,matrix=Matrix.Translation((5.30,yc+dy,zc))@Matrix.Diagonal((0.07,0.02,0.02,1)))    # arms
    for dy in (-0.31,0.31):
        bmesh.ops.create_cone(vb,cap_ends=True,segments=20,radius1=0.042,radius2=0.042,depth=0.012,
                              matrix=Matrix.Translation((5.345,yc+dy,zc))@Matrix.Rotation(math.radians(90),4,'X'))         # end caps
    me=bpy.data.meshes.new('vanity_light'); vb.to_mesh(me); vb.free(); me.materials.append(bm_)
    o=bpy.data.objects.new('Bath_Fixtures__vanity_light_bar',me); sc.collection.objects.link(o)
    vg=bmesh.new()
    bmesh.ops.create_cone(vg,cap_ends=True,segments=24,radius1=0.036,radius2=0.036,depth=0.60,
                          matrix=Matrix.Translation((5.345,yc,zc))@Matrix.Rotation(math.radians(90),4,'X'))
    me=bpy.data.meshes.new('vanity_lens'); vg.to_mesh(me); vg.free()
    lm_=bpy.data.materials.new('vanity_lens'); emissive(lm_,6.0,(1.0,0.86,0.68)); simple(lm_,None,0.0,0.35); me.materials.append(lm_)
    for p in me.polygons: p.use_smooth=True
    o=bpy.data.objects.new('Bath_Fixtures__vanity_light_lens',me); sc.collection.objects.link(o)
    ld=bpy.data.lights.new('LT_Vanity','AREA'); ld.shape='RECTANGLE'; ld.size=0.08; ld.size_y=0.60; ld.energy=35; ld.color=(1.0,0.85,0.66)
    lo=bpy.data.objects.new('LT_Vanity',ld); lo.location=(5.40,yc,zc); sc.collection.objects.link(lo)
    lo.rotation_euler=(0,math.radians(-60),0)         # aims out from the wall and down onto the vanity
    lo.visible_camera=False; lo.visible_glossy=False; lo.visible_transmission=False
cams=[]
for (name,eye,tgt,fov) in [
    ('CAM_01_Cover',(-1.9812, -14.9352, 2.2555),(3.5052, -2.4384, 1.8288),62),
    ('CAM_02_Bar_Stool_View',(-1.8288, -4.2672, 1.463),(3.048, -2.7432, 1.524),70),
    ('CAM_03_Front_Right',(3.9624, -12.192, 1.8898),(1.524, -1.524, 1.524),70),
    ('CAM_04_Sauna_Doorway',(5.9284, -5.4559, 1.8288),(5.8217, -3.048, 0.7925),100),
    ('CAM_05_Sauna_Back_Bench',(6.797, -2.5908, 1.9202),(5.7912, -5.273, 0.7925),100),
    ('CAM_06_Back_Right',(10.9728, 4.2672, 3.048),(4.572, -2.4384, 1.524),55),
    ('CAM_07_Bathroom',(6.80, -0.42, 1.75),(5.55, -1.95, 1.12),100),
]:
    cd=bpy.data.cameras.new(name); cd.sensor_fit='HORIZONTAL'; cd.angle=math.radians(fov); cd.clip_start=0.03; cd.clip_end=6000
    ob=bpy.data.objects.new(name,cd); sc.collection.objects.link(ob)
    ob.location=eye; ob.rotation_euler=(Vector(tgt)-Vector(eye)).to_track_quat('-Z','Y').to_euler(); cams.append(ob)
sc.camera=cams[0]
# one shot per frame: frame 1 = CAM_01 ... frame 6 = CAM_06 (timeline markers bind the camera), and the sun is keyed
# per frame so each view can have its own light. Press F12 on any frame 1-6, or render the animation for all six.
sc.timeline_markers.clear(); sc.frame_start=1; sc.frame_end=len(cams)
for i,cam in enumerate(cams):
    mk=sc.timeline_markers.new(cam.name,frame=i+1); mk.camera=cam
    aim_sun(CAM_SUN.get(cam.name,SUN_AZIMUTH),frame=i+1,bg_turn=CAM_BG_TURN.get(cam.name,0.0))
    sc.view_settings.exposure=CAM_EXPOSURE.get(cam.name,0.0); sc.view_settings.keyframe_insert('exposure',frame=i+1)
for idb in (sc,sun,sc.world.node_tree,bpy.data.materials.get('lawn') and bpy.data.materials['lawn'].node_tree):
    ad=getattr(idb,'animation_data',None) if idb else None
    if ad and ad.action:
        for fc in ad.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
sc.frame_set(1)

# ------------------------------------------------------------------ render settings (GPU if available)
sc.render.engine='CYCLES'
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences
    for kind in ('OPTIX','CUDA','METAL','HIP','ONEAPI'):
        try:
            prefs.compute_device_type=kind; prefs.get_devices()
            if any(d.type!='CPU' for d in prefs.devices):
                for d in prefs.devices: d.use=True
                sc.cycles.device='GPU'; print('Cycles device:',kind); break
        except Exception: pass
except Exception: pass
cy=sc.cycles
cy.samples=SAMPLES; cy.use_denoising=True; cy.use_adaptive_sampling=True; cy.adaptive_threshold=0.01
cy.max_bounces=10; cy.diffuse_bounces=4; cy.glossy_bounces=4; cy.transmission_bounces=8; cy.transparent_max_bounces=8
cy.sample_clamp_indirect=8.0; cy.caustics_reflective=False; cy.caustics_refractive=False
try: cy.denoiser='OPENIMAGEDENOISE'; cy.denoising_input_passes='RGB_ALBEDO_NORMAL'
except Exception: pass
sc.render.resolution_x,sc.render.resolution_y=RES; sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'

if RENDER_ALL:
    out=os.path.join(BASE,'renders'); os.makedirs(out,exist_ok=True)
    for i,cam in enumerate(cams):
        sc.frame_set(i+1); sc.camera=cam; sc.render.filepath=os.path.join(out,cam.name+'.png'); bpy.ops.render.render(write_still=True)
        print('rendered',cam.name)
    sc.camera=cams[0]
print('Cramers pavilion v3 ready. Frames 1-6 = CAM_01..CAM_06 (each with its own sun). F12 renders the current frame.')

# ==================================================================================================================
# CHANGES v2 -> v3 (found by rendering all six cameras and reviewing them)
#  WOOD GRAIN (all cedar): v2 used one wave texture in object space per material, so every wall showed the same
#    wavy "zebra" stripes running across the boards, bench tops / beam bottoms had no grain at all, and you could
#    not see individual boards. v3 rebuilds each board from the mesh, runs the grain along that board's own long
#    axis (siding/beams horizontal, posts vertical, ceiling boards front-to-back), gives each board its own tone
#    from a real cedar range, growth rings, fibre streaks and V-groove seams; lap siding gets its drip shadow line.
#    Wall/panel faces modelled as one big face are cut into virtual 5.5 in boards in the shader.
#  SHOU SUGI BAN: v2 voronoi read as a pebble / flagstone wall. v3: slim alligator blocks aligned with the grain,
#    even charcoal tone, thin cracks, faint sheen, and board seams on the bar front.
#  GRANITE: v2 was a smooth pink/red marble. v3: Typhoon Bordeaux-style burgundy/cream/grey swirls built from
#    individual crystals with black biotite and garnet flecks, clear-coat polish.
#  CONCRETE: Poly Haven concrete_floor_02 is a stained, worn floor - wrong for a new salt-finish slab. v3: clean light
#    grey with soft mottling and scattered salt pits, ~0.3 albedo (it read white in direct sun before).
#  LAWN: Poly Haven aerial_grass_rock is patchy dead grass and gravel, and the 31 m ground square ended in mid-air
#    with bare sky below the horizon. v3: instanced 3D grass, a ground plane to the horizon that fades into the
#    HDRI's own photographed field, colour matched to it.
#  SKY/SUN: the HDRI already contains a full-strength sun; v2 added a second sun lamp 30 deg away -> two suns,
#    double shadows, extra exposure. v3 clamps the HDRI sun out and puts one sun lamp at the measured HDRI
#    irradiance. Sky swapped to Poly Haven noon_grass (8k) so there is a real tree line instead of an empty horizon.
#  PER-SHOT LIGHT: frames 1-6 carry the six cameras; CAM_06 (back) gets its own sun so it isn't all in shade, and
#    each shot has its own exposure (the bar view looks into the shade under the roof).
#  FAN: its point light sat 21 cm below the blades -> lit them white and threw blade shadows across the ceiling.
#    Now a downward disc under the glass; blades satin instead of half-metallic.
#  SAUNA: light was 12 cm under the ceiling (blown hotspot) and visible as a glowing ball through the door glass;
#    lights are now hidden from camera/reflection/glass rays. Fixture glow warmed and dimmed. The bucket stand-in
#    (a cube with a stick standing straight up out of it) replaced with a stave bucket, bands and a resting ladle.
#
# OWNER REVIEW CHANGES (after the first v3 renders)
#  - Cedar matched to the West Ashley pool cabana: honey/amber clear-sealed WRC, tighter board-to-board range, small
#    brown knots, light rough-sawn fibre texture (sauna stays clear grade).
#  - Post bases rebuilt like the cabana: board-wrapped upper block on a wider plinth relieved between the corners
#    so it stands on feet; works on the L-shaped bases of the posts engaged in the walls too.
#  - Bar baseboard black. Countertop = tile made from the owner's photo of their Typhoon Bordeaux slab
#    (perspective-corrected, grommets/glare/shadow removed, seamless; two offset copies blended to hide repeats).
#  - Sauna: lower bench pulled back 46 cm (heater walkway 22 cm -> ~68 cm), new kick board, bucket moved;
#    three recessed cans in the ceiling. Bathroom: water heater and shelves swapped.
#  - Grain frames follow each member's real direction: sloped beams (e.g. over the TV wall) no longer get
#    level grain or fake board seams. Ceiling = beaded T&G, TV wall = flat T&G, enclosure = real lap siding
#    (each board's butt stands 1/2 in proud with a real shadow line).
#  - Removed a stray full-height cedar plane at x=5.309 that stood 6 cm inside the bath + sauna left wall (it hid the
#    vanity mirror, sauna shelf/hooks/backrest and showed exterior knotty cedar inside the sauna).
#  - Bathroom: cedar flat-T&G walls, beaded-T&G ceiling, black vanity top; CAM_07_Bathroom (wide, like the sauna views).
#  - Bath back wall: coplanar triangles now share one board layout (was a diagonal break); vanity bar light added.
