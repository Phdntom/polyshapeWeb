
class Cell():
    '''
        Cells embed onto a geometrical lattice.

        Members
        -------
        (i,j):      cell coordinates in two-dimensional plane
        lattice:    defines the neighbor/coordination type via lattice name
        c:          color for checkerboard neighbor restrictions

        Methods
        -------

    '''

    def __init__(self, i, j, lattice=None, c=None):
        '''
        '''
        self.i = i
        self.j = j
        self.lattice = lattice
        self.c = c

    def __iter__(self):
        yield self.i
        yield self.j

    def __str__(self):
        return "(" + str(self.i) + ":" + str(self.j) + ")"

    def __repr__(self):
        return "{" + str(self.i) + ":" + str(self.j) + "}"

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

        return valid_neighbors

    #private members below here 
    def validate_grid(self, i, j, grid):
        '''
        Returns bool
        '''
        row_max = len(grid)
        col_max = len(grid[0])
        return grid[i][j] and \
               ( j < col_max ) and \
               ( j >= 0 ) and \
               ( i < row_max ) and \
               ( i >= 0 )

    def neighbor_vectors(self):
        '''
        '''
        if self.lattice == "polyomino":
            # simple square
            return [ ( 0,+1), (+1, 0), (-1, 0), ( 0,-1) ]

        if self.lattice == "polyplet":
            # square with diagonal neighbors
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
            '''
            '''
            if self.c:          #red
                return [ ( 0,+1), (+1, 0), ( 0,-1) ]
            else:               #white
                return [ ( 0,+1), (-1, 0), ( 0,-1) ]

    def template(self, N):
        '''
        '''
        grid = []

        simple_square = ["polyomino", "polyplet", "polyhex"]

        if self.lattice in simple_square:
            for i in range(N):
                grid.append([True for j in range(2*N-1)])
            for j in range(N-1):
                grid[0][j] = False                
            return grid
        elif self.lattice == "polyiamond":                     #different than square?
            for i in range(N):
                grid.append([True for j in range(2*N-1)])
            for j in range(N-2):
                grid[0][j] = False
            self.c = True
            return grid
        else:
            print("ERROR: This cell has no valid template\n")
            return None

### class Cell

class PolyShape():
    """A collection of cells on a lattice"""

    def __init__(self, lattice, N = 5, store = False):
        '''
        '''
        self.N = N
        self.lattice = lattice
        self.count = 0
        self.store = store
        if store:
            self.big_list = []

        self.actions = []         # for animation only
        self.sim_time = 0

        path = []
        stack = []

        start = Cell(0, N-1, lattice)
        grid = start.template(N)
        list_grid = []
        for row in enumerate(grid,start=0):
            for col in enumerate(row[1],start=0):
                list_grid.append( (row[0],col[0],col[1]))

        self.actions.append( (self.sim_time, "grid", "make", [l for l in list_grid]) )
        self.sim_time += 1

        stack.append(start)
        self.mark_grid(False, start, grid)
        self.actions.append( (self.sim_time, "stack", "push", [start]) )
        self.actions.append( (self.sim_time, "grid", "mark", (start,False) ) )
        self.sim_time += 1

        depth = 0
        self.explore(stack, grid, path, depth)

    def __str__(self):
        return "{0} lattice of size {1}".format(self.lattice,str(self.N))

    def action_stream(self):
        for each in self.actions:
            yield each

    def stream_name(self):
        return "{0}_{1}_stream".format(self.lattice,str(self.N))

    def streamJSON(self):
        '''
        time,

        grid, make, list of (i,j,bool)
        grid, mark, (Cell, bool)
        grid, neighbors, list of Cell
 
        stack, push, list of Cell
        stack, copy, list of Cell
        stack, pop, Cell

        path, push, Cell
        path, show, list of Cell
        path, pop, Cell
        '''
        for action in self.actions:
            yield self.encodeJSONs(action)

    def encodeJSONs(self,action):
        time = action[0]
        obj  = action[1]
        name = action[2]
        data = action[3]
        json_dict = {}
        json_dict["time"] = time
        json_dict["object"] = obj
        json_dict["command"] = name         

        if obj == "grid":
            if name == "make":
                json_dict["data"] = data
            elif name == "mark":
                json_dict["data"] = tuple(data[0]), data[1]
            elif name == "neighbors":
                json_dict["data"] = [ tuple(c) for c in data ]

        elif obj == "stack":
            if name == "push" or name == "copy":
                json_dict["data"] = [tuple(c) for c in data]
            elif name == "pop":
                json_dict["data"] = tuple(data)
                
        elif obj == "path":
            if name == "push" or name == "pop":
                json_dict["data"] = tuple(data)
            elif name == "show":
                json_dict["data"] = [tuple(c) for c in data]

        else:
            print action

        import json
        return json.dumps(json_dict)

    def get_count(self):
        return self.count

    def explore(self, stack, grid, path, depth):
        '''
        '''
        v = stack.pop()                         # follow the top cell
        path.append(v)
        depth += 1

        self.actions.append( (self.sim_time, "stack", "pop", v) )
        self.actions.append( (self.sim_time, "path", "push", v) )
        self.sim_time += 1

        if depth == self.N:                     # stop if depth is N
            self.count += 1
            if self.store:
                self.big_list + path
            #self.show_path(path)

            self.actions.append( (self.sim_time, "path", "show", [c for c in path]) )
            self.sim_time += 1
            p = path.pop()
            self.actions.append( (self.sim_time, "path", "pop", p) )
            self.sim_time += 1
            #self.visualize(grid)
        else:
            new_neighbors = v.neighbors(grid)
            self.actions.append( (self.sim_time, "grid", "neighbors", [n for n in new_neighbors]) )
            self.sim_time += 1

            for each in new_neighbors:
                self.mark_grid(False, each, grid)
                self.actions.append( (self.sim_time, "grid", "mark", (each,False) ) )
                self.sim_time += 1

            new_stack = stack + new_neighbors  # preserve stack for future
            self.actions.append( (self.sim_time, "stack", "copy", [s for s in stack]) )
            self.sim_time += 1
            self.actions.append( (self.sim_time, "stack", "push", [n for n in new_neighbors]) )
            self.sim_time += 1

            while new_stack:
               self.explore(new_stack, grid, path, depth)

            # the top cell in path is used up, remove it 
            p = path.pop()
            self.actions.append( (self.sim_time, "path", "pop", p) )
            self.sim_time += 1
            # Mark neighbors used in this recursion available for future.
            for each in new_neighbors:
                self.mark_grid(True, each, grid)
                self.actions.append( (self.sim_time, "grid", "mark", (each, True) ) )
                self.sim_time += 1

    def mark_grid(self, switch, cell, grid):
        '''
        Parameters
        ----------
        cell:      Node
        grid:      list of list of bool

        DETAILS
            Cell contains a pair of coordinates in a two dimensional grid.
            Does not bound check.
        '''        
        grid[ cell.i ][ cell.j ] = switch

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

