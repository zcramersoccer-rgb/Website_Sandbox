import bpy, sys
from bpy_extras.view3d_utils import region_2d_to_vector_3d
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; cam=bpy.data.objects[a[0]]
scn=bpy.data.scenes['Pavilion']; dg=bpy.context.evaluated_depsgraph_get()
W,H=640,360; scn.render.resolution_x,scn.render.resolution_y=W,H
fr=cam.data.view_frame(scene=scn)  # tr, br, bl, tl in camera space
tr,br,bl,tl=fr
for px,py in [(int(p.split(',')[0]),int(p.split(',')[1])) for p in a[1:]]:
    u=px/W; v=py/H
    top=tl.lerp(tr,u); bot=bl.lerp(br,u); pt=top.lerp(bot,v)
    d=(cam.matrix_world.to_3x3()@pt).normalized(); o=cam.matrix_world.translation
    hit,loc,n,idx,ob,_=scn.ray_cast(dg,o,d)
    print('HIT',px,py,ob.name if hit else None, tuple(round(c/0.0254,1) for c in loc) if hit else '')
