# blender -b sunup-pavilion.blend -P render_review.py -- OUTDIR RESX RESY SPP NAME...
import bpy, sys, math
from mathutils import Vector
a = sys.argv[sys.argv.index('--')+1:]; outdir, rx, ry, spp = a[0], int(a[1]), int(a[2]), int(a[3]); names = a[4:]
IN = 0.0254; scn = bpy.data.scenes['Pavilion']
scn.render.resolution_x, scn.render.resolution_y = rx, ry; scn.cycles.samples = spp
def ortho(name, loc, rot, scale, clip=None):
    cd = bpy.data.cameras.new(name); cd.type = 'ORTHO'; cd.ortho_scale = scale*IN; cd.clip_end = 300
    if clip: cd.clip_start = clip*IN
    ob = bpy.data.objects.new(name, cd); scn.collection.objects.link(ob); ob.location = Vector(loc)*IN
    ob.rotation_euler = [math.radians(r) for r in rot]; return ob
ORTHO = {
 'E1 front elevation (SW)': lambda: ortho('E1', (0, -1500, 78), (90, 0, 0), 300),
 'E2 kitchen end elevation (SE)': lambda: ortho('E2', (1500, 0, 78), (90, 0, 90), 300),
 'E3 back elevation (NE)': lambda: ortho('E3', (0, 1500, 78), (90, 0, 180), 300),
 'E4 open end elevation (NW)': lambda: ortho('E4', (-1500, 0, 78), (90, 0, -90), 300),
 'P1 roof plan': lambda: ortho('P1', (0, 0, 1500), (0, 0, 0), 360),
 'P2 floor plan cut at 4 ft': lambda: ortho('P2', (0, 0, 1500), (0, 0, 0), 360, clip=1500 - 48),
}
for n in names:
    cam = ORTHO[n]() if n in ORTHO else bpy.data.objects[n]
    scn.camera = cam
    scn.render.filepath = f'{outdir}/{n}.png'
    bpy.ops.render.render(write_still=True); print('RENDERED', n, flush=True)
print('ALLDONE', flush=True)
