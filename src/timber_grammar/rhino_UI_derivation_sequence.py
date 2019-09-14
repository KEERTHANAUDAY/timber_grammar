import compas
from assembly_model import Model
from Derivation import Derivation

import rhino_UI_utilities
import rhinoscriptsyntax as rs
from compas_rhino.artists import MeshArtist

__commandname__ = "derivation_playback"

def RunCommand(is_interactive):

    #load Derivation and delete last step
    derivation = Derivation.from_json(rhino_UI_utilities.get_json_file_location())

    continue_playback = True
    step_id = 0 
    
    #load the selected model
    model = derivation.get_step(derivation.count - 1)

    while(continue_playback):
        #ask user for which step they would like to see
        derivation_last_step_index = derivation.count - 1
        
        step_id = rs.GetInteger("Enter which step to visualize (0 - "+ str(derivation_last_step_index) + " step) (Enter -1 for last step)", step_id, -1, derivation_last_step_index)
        if (step_id == -1): step_id = derivation_last_step_index
        if (step_id == None): break # Allow user to quite the command

        #Visualization 
        artist = MeshArtist(None, layer ='BEAM::Beams_out')
        artist.clear_layer()

        if (step_id>=derivation.count): continue
        
        for i in range(step_id + 1):
            beam = model.beams[i]
            artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')
            artist.draw_faces(join_faces=True)
        artist.redraw()  

        #Iterate step for User Friendiness         
        step_id = step_id + 1


if __name__ == '__main__':
    RunCommand(True)