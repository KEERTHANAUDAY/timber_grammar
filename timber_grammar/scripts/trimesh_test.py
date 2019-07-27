
import trimesh as t 

# HERE = os.path.dirname('__file__')
# DATA = os.path.abspath(os.path.join(HERE, '..', 'trimesh_1.obj'))


mesh_list = t.load_mesh('./scripts/trimesh_2.obj')
mesh_list_2 = t.load_mesh('./scripts/trimesh_1.obj')

a = mesh_list.difference(mesh_list_2, 'blender')

print (a)

#t.boolean.boolean_automatic(mesh,'difference')
#test if everything is okay
