import bpy, sys, math
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]; eye=[float(x) for x in a[1].split(',')]; tgt=[float(x) for x in a[2].split(',')]; lens=float(a[3])
IN=0.0254; scn=bpy.data.scenes['Pavilion']
cd=bpy.data.cameras.new('tmp'); cd.lens=lens; ob=bpy.data.objects.new('tmp',cd); scn.collection.objects.link(ob)
ob.location=Vector(eye)*IN; d=Vector(tgt)*IN-ob.location; ob.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
scn.camera=ob; scn.render.resolution_x,scn.render.resolution_y=960,540; scn.cycles.samples=48
scn.render.filepath=out; bpy.ops.render.render(write_still=True); print('RENDERED')
