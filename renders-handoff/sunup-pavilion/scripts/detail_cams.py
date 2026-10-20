import bpy, sys, math
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; outdir, tag = a[0], a[1]
IN=0.0254; scn=bpy.data.scenes['Pavilion']; scn.cycles.samples=64
cd=bpy.data.cameras.new('det'); cd.type='ORTHO'; cd.ortho_scale=140*IN; cd.clip_end=300
ob=bpy.data.objects.new('det',cd); scn.collection.objects.link(ob); ob.location=Vector((-80,-1500,62))*IN; ob.rotation_euler=(math.radians(90),0,0)
scn.camera=ob; scn.render.resolution_x,scn.render.resolution_y=720,1080; scn.render.filepath=f'{outdir}/{tag}_elev.png'; bpy.ops.render.render(write_still=True)
scn.camera=bpy.data.objects['CAM_07 corner detail - trim + soffit hip']; scn.render.resolution_x,scn.render.resolution_y=960,1080
scn.camera.data.lens=40
scn.render.filepath=f'{outdir}/{tag}_corner.png'; bpy.ops.render.render(write_still=True); print('DONE',tag)
