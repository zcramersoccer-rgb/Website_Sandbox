import bpy, sys, math
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]
IN=0.0254; scn=bpy.data.scenes['Pavilion']; scn.cycles.samples=96
cd=bpy.data.cameras.new('cc'); cd.lens=55; ob=bpy.data.objects.new('cc',cd); scn.collection.objects.link(ob)
ob.location=Vector((-150,-170,64))*IN; d=Vector((-100,-80,100))*IN-ob.location; ob.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
scn.camera=ob; scn.render.resolution_x,scn.render.resolution_y=900,1000; scn.render.filepath=out; bpy.ops.render.render(write_still=True); print('DONE')
