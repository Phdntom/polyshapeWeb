polyshapeWeb
============

A shape generation algorithm and utilities for use in scientific computation.

interface.py
------------
  Minimal script to make calls to the PolyShape class.

PolyShape.py
------------
  Implements PolyShape class and Cell class for use with cell counting algorithm.
  
  
  A PolyShape object can be declared via
  
    polyshape = PolyShape( < "Shape Type String" >, N, "store shapes option" )
    
      "Shape Type String": currently supports
                              polyominoes
                              polyplets
                              polyhexes
                              polyiamonds
                           for site graphs only. Bond graphs coming soon!
                           
      N:    the number of site cells in a graph.
      
      "store shapes option":
              TRUE:     stores all graphs via x,y coordinates in a list accessible via
                        polyshape.big_list
              FALSE:    only provides a count of the graphs generated accessible via
                        polyshape.get_count()
                        
    
