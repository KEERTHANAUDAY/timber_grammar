import compas
from assembly_model import Model
from Derivation import Derivation

import rhino_UI_utilities

from compas_rhino.artists import MeshArtist

__commandname__ = "derivation_undo"

def RunCommand(is_interactive):

    #load Derivation and delete last step
    derivation = Derivation.from_json(rhino_UI_utilities.get_json_file_location())
    derivation.remove_last_step()
    print("New Derivation step count:" , str(derivation.count))
    #load last model
    model = derivation.get_step(derivation.count-1)


    #Visualization 
    artist = MeshArtist(None, layer ='BEAM::Beams_out')
    artist.clear_layer()
    for beam in model.beams:
        artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')
        artist.draw_faces(join_faces=True)

    #Save Derivation (Model is also saved)
    derivation.to_json(rhino_UI_utilities.get_json_file_location(), pretty = True)
    
if __name__ == '__main__':
    RunCommand(True)