Examples
================

Plane Orientation
--------------------

**Beam**

x-axis: length, y-axis: width, z-axis: height

**Dowel**

z-axis: length

.. image:: https://raw.githubusercontent.com/ytakzk/Gradual_Assemblies/master/docs/source/_static/plane_orientation.png


How to Use
--------------------

.. code-block :: python

    # import libraries
    import Rhino.Geometry as rg
    from geometry.beam import Beam
    from geometry.dowel import Dowel
    from geometry.hole import Hole

    # dimensions
    beam_dx = 145
    beam_dy = 10
    beam_dz = 4
    dowel_radius = 1.0

    # create beams as planes
    beam_plane_1 = rg.Plane(rg.Plane.WorldXY)
    beam_plane_1.Translate(rg.Vector3d(100, 100, 0))

    beam_plane_2 = rg.Plane(rg.Plane.WorldXY)
    beam_plane_2.Translate(rg.Vector3d(100, 100, 50))

    beam_planes = [beam_plane_1, beam_plane_2]

    # create dowels as planes
    dowel_plane_1 = rg.Plane(rg.Plane.WorldXY)
    dowel_plane_1.Translate(rg.Vector3d(140, 100, 0))
    dowel_plane_2 = rg.Plane(rg.Plane.WorldXY)
    dowel_plane_2.Translate(rg.Vector3d(60, 100, 0))

    # create an instance of dowel class as the connected dowel connected
    dowel_1 = Dowel(base_plane=dowel_plane_1, dowel_radius=dowel_radius)
    dowel_2 = Dowel(base_plane=dowel_plane_2, dowel_radius=dowel_radius)

    dowels = [dowel_1, dowel_2]

    beams = []

    # feed beam planes
    for beam_plane in beam_planes:

        # create an instance of beam class
        beam = Beam(base_plane=beam_plane, dx=beam_dx, dy=beam_dy, dz=beam_dz)

        for dowel in dowels:

            # add a dowel to the beam as its connection
            beam.add_dowel(dowel)

        beams.append(beam)

    original_beam_breps = [b.brep_representation() for b in beams]

    # get planes and brep(s)
    safe_planes, top_planes, bottom_planes, beam_breps = Hole.get_tool_planes_as_tree(beams, target_plane=rg.Plane.WorldXY, safe_buffer=2, safe_plane_diff=100)

.. image:: https://raw.githubusercontent.com/ytakzk/Gradual_Assemblies/master/docs/source/_static/example_grasshopper.PNG


Beam Class
--------------------

A class for beams

.. code-block :: python

    beam_plane = rg.Plane.WorldXY # the plane to define a beam's position and orientation
    beam_dx    = 145 # the length of a beam
    beam_dy    = 10 # the width of a beam
    beam_dz    = 4 # the depth of a beam

    # instanciate
    beam = Beam(base_plane=beam_plane,
                dx=beam_dx,
                dy=beam_dy,
                dz=beam_dz)
    
    # get a brep of the beam (can be used for visualization or debug)
    brep = beam.brep_representation()


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
