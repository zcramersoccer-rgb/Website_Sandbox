import bpy, sys, colorsys
a=sys.argv[sys.argv.index('--')+1:]; out, cam = a[0], a[1]
scn=bpy.data.scenes['Pavilion']; scn.camera=bpy.data.objects[cam]
obs=[o for o in scn.objects if o.type=='MESH']
for i,o in enumerate(obs):
    m=bpy.data.materials.new('dbg%d'%i); m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    e=nt.nodes.new('ShaderNodeEmission'); r,g,b=colorsys.hsv_to_rgb((i*0.618)%1,0.8,1.0); e.inputs[0].default_value=(r,g,b,1)
    o2=nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0],o2.inputs[0])
    o.data.materials.clear(); o.data.materials.append(m)
    for p in o.data.polygons: p.material_index=0
    print('ID', i, '%.2f %.2f %.2f'%(r,g,b), o.name)
scn.world=None
scn.render.resolution_x,scn.render.resolution_y=640,360; scn.cycles.samples=4; scn.cycles.use_denoising=False
scn.render.filepath=out; bpy.ops.render.render(write_still=True)
