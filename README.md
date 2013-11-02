polyshapeWeb
============

A shape generation algorithm and utilities for use in scientific computation.

interface.py
------------
  Minimal script to make calls to the PolyShape class.

PolyShape[Web].py
-----------------
  Implements PolyShape class and Cell class for use with counting algorithm.
  
  
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
/animate/polyWeb.js
-------------------
  Sets up a function wrapper for a polyShapeWeb animation using D3 (d3js.org)
  
/animate/polyWeb.html
---------------------
  Builds a basic page and pulls in a stream<N><Shape>.json file from PolyShapeWeb.py.
  
References
----------
D.Hugh Redelmeier, Counting polyominoes: Yet another attack, Discrete Mathematics, Volume 36, Issue 2, 1981, Pages 191-203, ISSN 0012-365X, http://dx.doi.org/10.1016/0012-365X(81)90237-5.
(http://www.sciencedirect.com/science/article/pii/0012365X81902375)
