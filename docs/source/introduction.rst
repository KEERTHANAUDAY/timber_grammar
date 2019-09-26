********************************************************************************
Introduction
********************************************************************************

timber_grammar provide functionality for applying a set of Shape Grammar rule transformations 
for timber-timber joinery structures. For example some of the Grammar rule transformations are 
lap, tenon, splice joint and their respective sub rule transformations. The main library
has been developed with the Framework (:mod:`compas`) and the Rhino UI wrapper functions
are developed with (:mod:`RhinoCommon`)

.. image:: https://raw.githubusercontent.com/KEERTHANAUDAY/timber_grammar/master/docs/source/_static/tool_structure.png


Shape Grammars
==============


Shape grammars, defines a set of allowable shape transformations that can be used to generate 
a language of spatial designs(Stiny 1968).

.. image:: https://raw.githubusercontent.com/KEERTHANAUDAY/timber_grammar/master/docs/source/_static/Shape_Grammar_rule.png


Geometry datastructure
======================


The geometry datastructure is built on the BTL format in order to pass each beam element
of the finished structure directly to CNC fabricatable format. This also helps compute 
rule tranformations at desired positions along each Beam. The data structure can be categorised 
3 levels, primarity the geometry of each beam, at a higher level the datastructure of each 
rule transformation and finally the network information of the entire derivation history of 
a timber structure.