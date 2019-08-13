import System

def create_id():
    g = System.Guid.NewGuid()
    return g

if __name__ == "__main__":
    a = create_id()
    print(type(a))
    print(a)



# import System

# import compas
# from compas_rhino.artists import MeshArtist
# from compas_rhino.artists import Artist

# class Paint_mesh(object):
#     """This class paints a mesh
#         and assigns an id
#     """
#     def __init__(self,self.mesh, self.str, self.join_face=True):

#         self.layer = layer
#         self.str = str
#         self.mesh = mesh
#         pass

#     def mesh_artist(self):
#         artist = MeshArtist(self.mesh, layer='self.str')
#         artist.draw_faces(join_faces=self.join_face)
        

#     def create_id(self):
#         g = System.Guid.NewGuid()
#         return g


