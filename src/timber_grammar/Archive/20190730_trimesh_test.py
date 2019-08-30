
import trimesh as t 

# HERE = os.path.dirname('__file__')
# DATA = os.path.abspath(os.path.join(HERE, '..', 'trimesh_1.obj'))


mesh_1 = t.load_mesh('./test_1.stl',process=False)
mesh_1.is_watertight

mesh_2 = t.load_mesh('./test_2.stl',process=False)
mesh_2.is_watertight

a = mesh_1.difference(mesh_2, 'blender')
a.export('test.stl')
#t.exchange.dae.export_collada(a)

if __name__ == '__main__':

    import trimesh as t 
    mesh_1 = t.load_mesh('./test_1.stl',process=False)
    mesh_1.is_watertight

    mesh_2 = t.load_mesh('./test_2.stl',process=False)
    mesh_2.is_watertight

    a = mesh_1.difference(mesh_2, 'blender')
    f = t.exchange.dae.export_collada(a)
    print(f)

