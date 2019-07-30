import compas
from compas.rpc import Proxy
import trimesh as t

mesh_1 = t.load_mesh('./test_1.stl',process=False)
mesh_1.is_watertight

mesh_2 = t.load_mesh('./test_2.stl',process=False)
mesh_2.is_watertight
with Proxy('trimesh') as t:
 
    a = mesh_1.difference(mesh_2, 'blender')
    a.export('test_proxy.stl')    