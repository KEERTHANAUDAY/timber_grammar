#imports from compas
import compas
from compas.datastructures import Mesh
from compas.geometry._primitives import Frame
from compas.geometry._primitives.box import Box
from compas.geometry import Translation

import os
#imports from timber_grammar
from id_generator import create_id
from Joint_90lap import Joint_90lap
from Beam import Beam

#exporting file path
HERE = os.path.dirname(__file__)
#DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
FILE_O = os.path.join('rhino.json')

#select mesh 
name = create_id()
beam = Beam(Frame.worldXY(),1000,100,150,name)

joint_frame = beam.frame.transformed(Translation([200,0,0]))
beam.joints.append(Joint_90lap(joint_frame,3,50,100,100))
beam.update_mesh() 

#save file
beam.to_json(FILE_O, pretty=True)