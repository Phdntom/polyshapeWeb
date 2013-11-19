import json
import PolyShapeWeb as ps
import sys
#import polyAnimate as pa

if __name__ == '__main__':

    N = 5
    name = "polyplet"

    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    if len(sys.argv) > 2:
        name = sys.argv[2]

    print( "Running with N={0} for {1} tiling.".format(N,name) )

    graph = ps.PolyShape(name, N)
    print( graph )
    print( graph.get_count() )

    fname = "stream{0}{1}.json".format(graph.N,graph.lattice)
    print( "Algorithm log in {0}.".format(fname) )

#    for each in graph.streamJSON():
#        print each
    with open(fname,"w") as fobj:
        fobj.write("var data = [\n")
        fobj.write(",\n".join(graph.streamJSON()))
        fobj.write("\n];")





