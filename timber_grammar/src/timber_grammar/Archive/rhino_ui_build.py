import rhinoscriptsyntax as rs
import compas
from compas.datastructures import Mesh
from compas.geometry import Frame
from assembly_model import Model
from compas_rhino.artists import MeshArtist
from compas_rhino.helpers import mesh_select_face
from compas_rhino.artists import Artist
from compas_rhino.utilities import select_meshes
from compas_rhino.helpers import mesh_from_guid


#def rule_create_beam():
#    model.load_beams()
#    #Ask for user to input beam location
#    #Ask for beam direction
#    #Ask for width, length , height
#    model.create_beam(Frame.worldXY(),depth, width, height)
#    
#    #Visualize all the beams in Rhino
#    #Clear Rhino preview layer.
#    for beam_mesh in model.mesh:
#        #Paint the mesh
        

#get information for joints
beam_guid = select_meshes()
beam_to_match = mesh_from_guid(Mesh, beam_guid[0])

face_id = mesh_select_face(beam_to_match)