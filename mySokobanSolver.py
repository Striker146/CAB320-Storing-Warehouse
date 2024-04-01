
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban
from collections import deque


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [(10779566, 'Ryan','Hansen'), (10779710,'Cody', 'Overs')]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class TouchingWalls:
    def __init__(self,up = None, right = None, down = None, left = None):
        self.walls = [up, right, down, left]
        self.up = up
        self.right = right
        self.down = down
        self.left = left

    def __repr__(self) -> str:
        return f"[{str(self.wall_1)}, {str(self.wall_2)}]"
    
class Corners:
    def __init__(self, corner_pairs):
        self.corner_pairs = corner_pairs
        self.corners = self.get_corners()

    def get_corners(self):
        corners = []
        for corner_pair in self.corner_pairs:
            corners.append(corner_pair.corner_1)
            corners.append(corner_pair.corner_2)
        return corners
    

class Corner:
    def __init__(self, wall_1, wall_2):
        self.wall_1 = wall_1
        self.wall_2 = wall_2
        diff = (wall_1[0] - wall_2[0], wall_1[1] - wall_2[1])
        self.corner_1 = (wall_1[0] - diff[0], wall_1[1])
        self.corner_2 = (wall_1[0], wall_1[1] - diff[1])

    def __str__(self):
        return f"[{str(self.wall_1)}, {str(self.wall_2)}], [{str(self.corner_1), str(self.corner_2)}]]"
    
    def __repr__(self) -> str:
        return f"[{str(self.wall_1)}, {str(self.wall_2)} | {str(self.corner_1), str(self.corner_2)}]"

def corner_comparator(wall_1, wall_2):
    if 1 == abs(wall_1[0] - wall_2[0]) and 1 == abs(wall_1[1] - wall_2[1]) :
        return True
    return False


def possible_worker_positions(warehouse):
        # Define movement offsets for up, down, left, and right
        movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        visited = set()
        queue = deque([(warehouse.worker[0], warehouse.worker[1])])
        possible_positions = set()

        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            possible_positions.add((x, y))
            for dx, dy in movements:
                new_x, new_y = x + dx, y + dy
                # Check if the new position is within the bounds of the warehouse and not a wall
                if (new_x, new_y) not in warehouse.walls and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y))

        return possible_positions

def get_corner_walls(warehouse):
    corner_pairs = []
    for wall_1 in warehouse.walls:
        for wall_2 in warehouse.walls:
            if corner_comparator(wall_1, wall_2):
                corner_pairs.append(Corner(wall_1, wall_2))
    #print(corner_pairs)
    corners = Corners(corner_pairs=corner_pairs)
    return corners

def display_taboo(warehouse, corners):
    display_string = ''
    for nrow in range(warehouse.nrows):
        for ncol in range(warehouse.ncols):
            if (ncol, nrow) in warehouse.walls:
                display_string = display_string + "#"
            elif (ncol, nrow) in corners.corners:
                display_string = display_string + "X"
            else:
                display_string = display_string + " "
        display_string = display_string + "\n"
    return display_string



def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
       
    '''
    ##         "INSERT YOUR CODE HERE"
    taboo = ''
    corner_walls = get_corner_walls(warehouse)
    taboo = display_taboo(warehouse, corner_walls)
    print(taboo)
    return taboo

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
    def __init__(self, warehouse):
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        raise NotImplementedError

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    
    raise NotImplementedError()


if "__main__" == __name__:
    wh = sokoban.Warehouse()
    wh.load_warehouse("./warehouses/warehouse_03.txt")
    taboo_cells(wh)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

'''
            elif x < 0 or x >= warehouse.ncols or y < 0 or y >= warehouse.nrows:
                taboo += '&'  # Outer cell
            else:
                adjacent_walls = 0  # Reset adjacent walls count for each empty cell
                for dx, dy in adjacent_positions:
                    # Calculate the position of the adjacent cell
                    adjacent_cell = (x + dx, y + dy)
                    # Check if the adjacent cell is a wall by verifying if it's in the warehouse's list of walls
                    if adjacent_cell in warehouse.walls:
                        # If the adjacent cell is a wall, increment the adjacent_walls counter
                        if adjacent_cell[0] >= 0 and adjacent_cell[1] >= 0:
                            adjacent_walls += 1
                        else:
                            print("hello bitch")
                            adjacent_walls -= 100
                        
                taboo += 'X' if adjacent_walls == 2 else ' '
'''