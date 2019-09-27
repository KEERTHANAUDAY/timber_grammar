Examples
================

Create Beam
-----------

**Beam**

compas Frame: frame, x-axis: length, y-axis: width, z-axis: height


.. image:: https://raw.githubusercontent.com/KEERTHANAUDAY/timber_grammar/master/docs/source/_static/data.png


How to Use
----------

.. code-block :: python

    # import libraries
    import compas
    from compas.geometry import Frame
    from timber_grammar.assembly_model import model 
    from timber_grammar.id_generator import create_id
    from timber_grammar import rhino_UI_utilities import utils

    print("Test 1: Create beam and save and load model to JSON")

    #Load Derivation and model
    derivation = Derivation.from_json(rhino_UI_utilities.get_json_file_location())
    model = derivation.get_next_step()

    # dimensions
    frame = Frame.worldXY()
    length = 1000
    width = 100
    height = 100
    name = create_id()

    # create beams as planes
    model.rule_create_beam(frame,length,width,height,name)

    #save Derivation 
    derivation.to_json(rhino_UI_utilities.get_json_file_location(), pretty = True)

    # Visualization
    artist = MeshArtist(None, layer ='BEAM::Beams_out')
    artist.clear_layer()
    for beam in model.beams:
        artist = MeshArtist(beam.mesh, layer ='BEAM::Beams_out')#.mesh is not ideal fix in beam and assemble class
        artist.draw_faces(join_faces=True)

.. image:: https://raw.githubusercontent.com/KEERTHANAUDAY/timber_grammar/master/docs/source/_static/create_beam.png


rule 90 Lap
-----------

A class 90 Lap joint rule 

.. code-block :: python

    #find beam instance by name search from model data
    selected_beam = None
    for beam in model.beams:
        if(beam.name == selected_beam_name):
            selected_beam = beam
            break
    assert (selected_beam != None)

    #values
    face_id = 4
    joint_point = Point(100,0,0)
    ext_start = 500
    ext_end = 1000
    name = create_id() 
    
    #adding joints to selected Beam 
    joint_distance_from_start = selected_beam.Get_distancefromBeamYZFrame(joint_point)
    match_beam_origin =  model.rule_90lap(selected_beam,joint_distance_from_start,face_id,ext_start,ext_end,name) 
     
.. image:: https://raw.githubusercontent.com/KEERTHANAUDAY/timber_grammar/master/docs/source/_static/rule_90Lap.png


Connect beams  
-------------

A class for connecting beams with a 90 Lap joint

.. code-block :: python

    #list of face_ids of coplanar planes 
    coplanar_face_ids = []
    coplanar_face_ids.append(face_id)
    for key,value in face_ids_coplanar_planes.items():
        if key == ""+str(face_id):
            coplanar_face_ids.extend(value)

    #project points
    projected_point_list = []
    new_start_point = project_points_plane([start_point],start_beam_perpendicular_plane)
    projected_point_list.extend(new_start_point)
    for plane in perpendicular_plane:
       new_point = project_points_plane(new_start_point,plane)
       projected_point_list.extend(new_point)

    
    #list of distance to move joints on match beam    
    model.rule_Connect_90lap(selected_beams,projected_point_list,coplanar_face_ids,beam_length,ext_len,create_id())

.. image:: https://raw.githubusercontent.com/KEERTHANAUDAY/timber_grammar/master/docs/source/_static/connect_beam.png



Derivation class
----------------

A class for rule derivation history 

.. code-block :: python

    #load Derivation and delete last step
    derivation = Derivation.from_json(rhino_UI_utilities.get_json_file_location())

    continue_playback = True
    step_id = 0 
    while(continue_playback):
        #ask user for which step they would like to see
        derivation_last_step_index = derivation.count - 1
        
        step_id = rs.GetInteger("Enter which step to visualize (0 - "+ str(derivation_last_step_index) + " step) (Enter -1 for last step)", step_id, -1, derivation_last_step_index)
        if (step_id == -1): step_id = derivation_last_step_index
        if (step_id == None): break # Allow user to quite the command

        #load the selected model
        model = derivation.get_step(step_id)
        step_id = step_id + 1

.. image:: https://raw.githubusercontent.com/KEERTHANAUDAY/timber_grammar/master/docs/source/_static/derive_gif.gif

