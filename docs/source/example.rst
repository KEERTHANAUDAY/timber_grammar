Examples
================

Create Beam
-----------

**Beam**

compas Frame: frame, x-axis: length, y-axis: width, z-axis: height


.. image:: https://raw.githubusercontent.com/ytakzk/Gradual_Assemblies/master/docs/source/_static/plane_orientation.png


How to Use
--------------------

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

.. image:: https://raw.githubusercontent.com/KEERTHANAUDAY/timber_grammar/master/docs/source/_static/create beam.png


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
     
.. image:: https://raw.githubusercontent.com/KEERTHANAUDAY/timber_grammar/master/docs/source/_static/create beam.png


Dowel Class
--------------------

A class for dowels

.. code-block :: python

    dowel_plane  = rg.Plane.WorldXY # the plane to define a dowel's position and orientation
    dowel_radius = 1.0 # the radius of a dowel

    # instanciate from plane
    dowel_plane = rg.Plane.WorldXY
    dowel = Dowel(base_plane=dowel_plane, dowel_radius=1.0)

    # OR

    # instanciate from line
    dowel_line = rg.Line(rg.Point3d(0, 0, -30), rg.Point3d(0, 0, 30))
    dowel = Dowel(line=dowel_line, dowel_radius=1.0)

    # add a dowel to the beam (possible if the beam has been declared before)
    beam.add_dowel(dowel)


Hole Class
--------------------

A class for making planes to open holes in beams

.. code-block :: python

    # contain beams as array
    beams = [beam_1, beam_2]

    # returns four kinds of data trees
    #
    # 1st: safe planes to drill
    # 2nd: planes to start drilling
    # 3rd: planes to end drilling
    # 4th: breps of beams in each state of drilling

    safe_planes, top_planes, bottom_planes, beam_breps = Hole.get_tool_planes_as_tree(beams,
        safe_plane_diff=100)


Evaluation Functions
-----------------------

Beam and Dowel class have some useful functions to identify the problematic dowel connection.


**Beam Class**	

.. code-block :: python

    # get angles in radian between the beam and its connected dowels as list.
    angles = beam.get_angle_between_beam_and_dowel()

    # get distances between the beam's edge and its connected dowels as list.
    # if the dowel locates totally outside of the beam, it returns a negative value.
    distances = beam.get_distance_from_edges()

**Dowel Class**	

.. code-block :: python

    # get an maximum angle in radian between the dowel and its connected beams.
    angle = dowel.get_angle_between_beam_and_dowel()

    # get minimum distance between the dowel and its connected beams' edge.
    # if the dowel locates totally outside of the beam, it returns a negative value.
    distance = dowel.get_distance_from_edges()
