import compas
from compas.rpc import Proxy
import trimesh as t
#compas_mesh = Box(frameXY,)100,100,100)
mesh_1 = t.load_mesh('./test_a.stl',process=False)
mesh_2 = t.load_mesh('./test_b.stl',process=False)

with Proxy('trimesh') as t:

    a = mesh_1.difference(mesh_2, 'blender')
    a.export('test_proxy_2.stl')    