import json
import PolyShape as ps
import sys
#import polyAnimate as pa

def encode(graph):
    x = 0
    y = 0
    for n,cell in enumerate(graph):
        x += cell.i * 10 ** n
        y += cell.j * 10 ** n
    return x,y

if __name__ == '__main__':

    N = 5
    name = "polyplet"

    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    if len(sys.argv) > 2:
        name = sys.argv[2]

    print( "Running with N={0} for {1} tiling.".format(N,name) )

    graph = ps.PolyShape(name, N, True)
    print( graph )
    print( graph.get_count() )

    fname = "graph_log{0}{1}.txt".format(graph.N,graph.lattice)
    print( "Algorithm log in {0}.".format(fname) )

#    for each in graph.streamJSON():
#        print each

    #for each in graph.big_list:
    #    print [ (cell.i,cell.j) for cell in each], encode(each)
    '''
    with open(fname,"w") as fobj:
        fobj.write(graph.get_count())
        fobj.write("\n".join(graph.getKeyCode()))
    '''




