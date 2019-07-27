
import trimesh as t 

# HERE = os.path.dirname('__file__')
# DATA = os.path.abspath(os.path.join(HERE, '..', 'trimesh_1.obj'))


mesh_1 = t.load_mesh('./scripts/trimesh_2.obj')
mesh_2 = t.load_mesh('./scripts/trimesh_1.obj')

a = mesh_1.difference(mesh_2, 'blender')

mesh_list.difference()
print (a)

#t.boolean.boolean_automatic(mesh,'difference')
#test if everything is okay
