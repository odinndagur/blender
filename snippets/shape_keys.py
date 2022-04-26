import bpy

def main():
    obj = bpy.context.active_object
    verts = obj.data.vertices
    
    new_verts = bpy.data.meshes['x5y4_plane_width251_height251_scale1'].vertices
    
    sk_basis = obj.shape_key_add(name='Basis',from_mix=False)
    sk_basis.interpolation = 'KEY_LINEAR'
    obj.data.shape_keys.use_relative = False
    

    for n in range(5):
        sk = obj.shape_key_add(name='Deform')
        sk.interpolation = 'KEY_LINEAR'
        new_verts = bpy.data.meshes[n+4].vertices
        for i in range(len(verts)):
            sk.data[i].co.z = new_verts[i].co.z
main()