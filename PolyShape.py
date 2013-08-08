import numpy


class Cell():
    '''
        Cells embed onto a geometrical lattice.

        Members
        -------
        (i,j):      coordinates in two-dimensional space
        lattice:    defines the neighbor/coordination type via lattice name
        c:          color for checkerboard neighbor restrictions
        Methods
        -------

    '''

    def __init__(self, i, j, lattice, c = None):
        '''
        '''
        self.i = i
        self.j = j
        self.lattice = lattice
        self.c = c

    def __str__(self):
        return "(" + str(self.i) + "," + str(self.j) + ")"

    def get_type(self):
        return self.lattice

    def neighbors(self, grid):
        '''
        '''
        valid_neighbors = []
        vectors = self.neighbor_vectors()

        for v in vectors:
            i = self.i + v[0]
            j = self.j + v[1]
            if self.validate_grid(i, j, grid):
                valid_neighbors.append( Cell(i, j, self.lattice, not self.c) )
                grid[i][j] = False
        return valid_neighbors
    #private members below here 
    def validate_grid(self, i, j, grid):
        '''
        '''

        return grid[i][j] and \
               ( j < len( grid[i]) ) and \
               ( j >= 0 ) and \
               ( i < len(grid) ) and \
               ( i >= 0 )

    def neighbor_vectors(self):
        '''
        '''
        if self.lattice == "polyomino":
            return [ ( 0,+1), (+1, 0), (-1, 0), ( 0,-1) ]

        if self.lattice == "polyplet":
            return [ ( 0,+1), (+1,+1), (+1, 0), (+1,-1),\
                     ( 0,-1), (-1,-1), (-1, 0), (-1,+1) ]

        if self.lattice == "polyhex":
            '''
            The lattice is mapped to a square lattice as follows...

             . . . . .              . . . . .
            . . 4 5 r .             . 4 5 r .
             . 3 v 0 .      -->     . 3 v 0 .
            . q 2 1 . .             . q 2 1 .
             . . . . .              . . . . .

            cell v: (i,j) does not neigbhor r: (i-1,j+1) or q: (i+1,j-1).
            ''' 
            return [ ( 0,+1), (+1,+1), (+1, 0),\
                     ( 0,-1), (-1,-1), (-1, 0) ]

        if self.lattice == "polyiamond":
            if self.c:          #red
                return [ ( 0,+1), (+1, 0), ( 0,-1) ]
            else:               #white
                return [ ( 0,+1), (-1, 0), ( 0,-1) ]
 
def cell_template( cell, N):
    '''
    '''
    grid = []

    template = cell.get_type()

    simple_square = ["polyomino", "polyplet", "polyhex"]

    if template in simple_square:
        for i in range(N):
            grid.append([True for j in range(2*N-1)])
        for j in range(N-1):
            grid[0][j] = False                

        return grid
    elif template == "polyiamond":                     #different than square?
        for i in range(N):
            grid.append([True for j in range(2*N-1)])
        for j in range(N-2):
            grid[0][j] = False
        cell.c = True
        return grid
    else:
        print("ERROR: no valid shape\n")
        return None

class PolyShape():
    """A collection of cells on a lattice"""


    def __init__(self, lattice, N):
        '''
        '''
        self.N = N
        self.lattice = lattice
        self.count = 0

        path = []
        stack = []

        self.big_list = []


        start = Cell(0, N-1, lattice)

        grid = cell_template(start, N)


        stack.append(start)
        self.mark_grid(False, start, grid)

        depth = 0

        self.explore(stack, grid, path, depth)

        #print stack

    def __str__(self):
        return "{0} lattice of size {1}".format(self.lattice,str(self.N))

    def get_count(self):
        return self.count


    def explore(self, stack, grid, path, depth):
        '''
        '''
        v = stack.pop()
        path.append(v)
        depth += 1

        if depth == self.N:
            self.count += 1
            #self.big_list + path
            #self.show_path(path)
            path.pop()
            #self.visualize(grid)

            
        else:
            new_neighbors = v.neighbors(grid)
            low_stack = stack + new_neighbors

            while low_stack:
               self.explore(low_stack, grid, path, depth)
            path.pop()
            
            for each in new_neighbors:
                self.mark_grid(True, each, grid)


    def visualize(self, grid):
        for each in grid:
            for ele in each:
                if ele == True: print "1",
                else: print "0",
            print
        print
    def show_path(self,path):
        print "path",
        for each in path:
            print each,
        print


    def mark_grid(self, switch, n, grid):
        '''
        Parameters
        ----------
        cell:      Node
        grid:      list of list of bool

        DETAILS
            Cell contains a pair of coordinates in a two dimensional grid.
            Does not bound check.
        '''        
        grid[ n.i ][ n.j ] = switch


