# usage: blender -b vanhove-hood.blend -P render_vh.py -- OUT SCENE CAMERA RESX RESY SPP
import bpy, sys
a=sys.argv[sys.argv.index('--')+1:]; out,scn_name,cam,rx,ry,spp=a[0],a[1],a[2],int(a[3]),int(a[4]),int(a[5])
scn=bpy.data.scenes[scn_name]; scn.camera=bpy.data.objects[cam]
scn.render.resolution_x,scn.render.resolution_y=rx,ry; scn.cycles.samples=spp; scn.cycles.device='CPU'
scn.render.filepath=out; bpy.ops.render.render(write_still=True,scene=scn_name); print('RENDERED',out,flush=True)
