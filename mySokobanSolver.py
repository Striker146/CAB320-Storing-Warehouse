
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

class WarehouseProblem(search.Problem):
    def __init__(self, warehouse, initial):
        self.warehouse = warehouse
        self.initial = initial
        self.explored = []
        self.corners = []
        self.worker = initial

    def result(self, state, action):
        assert action in self.actions(state)
        new_state = tuple(map(sum, zip(state, action)))
        if new_state not in self.explored: # If the cell is previously explored do nothing
            self.explored.append(new_state) 

            if self.is_corner(new_state) and new_state not in self.warehouse.targets:
                self.corners.append(new_state)
            
        return new_state

    def actions(self, state):
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        possible_actions = []
        for move in moves:
            new_pos = tuple(map(sum, zip(state, move)))  # Calculate new position
            if self.is_valid_move(new_pos):
                possible_actions.append(move)
        return possible_actions

    def goal_test(self, state): # NO GOAL ONLY TRAVEL
        return False

    def is_valid_move(self, pos):
        col, row = pos
        return (1 <= row < self.warehouse.nrows and
                1 <= col < self.warehouse.ncols and
                (col, row) not in self.warehouse.walls)
    
    def is_corner(self, state):
        col, row = state
        return ((col, row - 1) in self.warehouse.walls and (col - 1, row) in self.warehouse.walls or 
            (col, row - 1) in self.warehouse.walls and (col + 1, row) in self.warehouse.walls or
            (col, row + 1) in self.warehouse.walls and (col - 1, row) in self.warehouse.walls or
            (col, row + 1) in self.warehouse.walls and (col + 1, row) in self.warehouse.walls)
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [(10779566, 'Ryan','Hansen'), (10779710,'Cody', 'Overs')]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_taboo_cord(warehouse):
    def find_corner_pairs(corners, warehouse):
        corner_pairs = []

        for row in range(len(corners)):
            for col in range(row + 1, len(corners)):
                corner1 = corners[row]
                corner2 = corners[col]

                # Check if there is a wall between the corners
                if meets_taboo_conditions(corner1, corner2, warehouse):
                    if (abs(corner1[0] - corner2[0]) > 1) or (abs(corner1[1] - corner2[1]) > 1):
                        if corner1[0] == corner2[0]:
                            corner_pairs.append((corner1, corner2))
                        elif corner1[1] == corner2[1]:
                            corner_pairs.append((corner1, corner2))

        return corner_pairs

    def meets_taboo_conditions(corner1, corner2, warehouse):
        if corner1[0] == corner2[0]:  # Same column, check rows
            min_row = min(corner1[1], corner2[1])
            max_row = max(corner1[1], corner2[1])
            for row in range(min_row + 1, max_row):
                if ((corner1[0], row) in warehouse.walls or (corner1[0], row) in warehouse.targets) or not ((corner1[0] - 1, row) in warehouse.walls or (corner1[0] + 1, row) in warehouse.walls):
                    return False
        elif corner1[1] == corner2[1]:  # Same row, check columns
            min_col = min(corner1[0], corner2[0])
            max_col = max(corner1[0], corner2[0])
            for col in range(min_col + 1, max_col):
                if ((col, corner1[1]) in warehouse.walls or (col, corner1[1]) in warehouse.targets) or not ((col, corner1[1] - 1) in warehouse.walls or (col, corner1[1] + 1) in warehouse.walls):
                    return False
        return True
    
    def coordinates_between_corners(corner1, corner2):
        coordinates = []
        
        if corner1[0] == corner2[0]:  # Same column
            min_row = min(corner1[1], corner2[1])
            max_row = max(corner1[1], corner2[1])
            for row in range(min_row + 1, max_row):
                coordinates.append((corner1[0], row))
        elif corner1[1] == corner2[1]:  # Same row
            min_col = min(corner1[0], corner2[0])
            max_col = max(corner1[0], corner2[0])
            for col in range(min_col + 1, max_col):
                coordinates.append((col, corner1[1]))
        
        return coordinates
    
    def return_taboo_walls(corner_pairs):
        cells = []
        for pair in corner_pairs:
            cells += (coordinates_between_corners(pair[0], pair[1]))

        return cells

    wh_problem = WarehouseProblem(warehouse, warehouse.worker)
    search.breadth_first_graph_search(wh_problem)

    corner_pairs = find_corner_pairs(wh_problem.corners, warehouse)

    taboo_walls = return_taboo_walls(corner_pairs)

    taboo_cells = wh_problem.corners + taboo_walls
    return taboo_cells

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
    for row in range(warehouse.nrows):
        for col in range(warehouse.ncols):
            if (col, row) in warehouse.walls:
                taboo += '#'
            elif (col, row) in get_taboo_cord(warehouse): 
                taboo += "X"
            else:
                taboo += " "
        taboo += "\n"

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
        self.wh = warehouse.copy()
        self.initial = tuple([tuple(warehouse.worker), tuple(warehouse.boxes)])

        self.goal = tuple(warehouse.targets)

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        L = []
        #Up
        all_moves = ["Up", "Right", "Down", "Left"]
        for move in all_moves:
            is_possible, new_wh = check_move_validity(self.wh, move, state)
            if is_possible:
                L.append(move)
        return L
    
    def result(self, state, action):
        next_state = list(state)
        assert action in self.actions(state)
        is_possible, next_state = check_move_validity(self.wh,action, state)
        return next_state
    
    
    def goal_test(self, state):
        """Return True if the state is a goal."""
        return set(state[1]) == set(self.goal)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def apply_state_to_warehouse(warehouse,state):
    warehouse.worker = list(state[0])
    warehouse.boxes = list(state[1])

def check_move_validity(warehouse, action, state=None):
        if state == None:
            state = (tuple(warehouse.worker), tuple(warehouse.boxes))
        warehouse_clone = warehouse.copy()
        worker = list(state[0])
        boxes = list(state[1])
        new_box = None
        match action:
            case "Up":
                diff = (0, -1)
            case "Right":
                diff = (1, 0)
            case "Down":
                diff = (0, 1)
            case "Left":
                diff = (-1, 0)
            case _:
                raise Exception(f"'{action}' does not match the available moves.")
        worker = (worker[0] + diff[0], worker[1] + diff[1])
        if worker in warehouse_clone.walls:
            return False, None
        if worker in boxes:
            new_box = (worker[0] + diff[0], worker[1] + diff[1])
            if new_box in boxes or new_box in warehouse_clone.walls:
                return False, None
            else:
                moved_box_index = boxes.index(worker)
                boxes[moved_box_index] = new_box

        next_state = (tuple(worker), tuple(boxes))
        return True, next_state

            
    

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
    worker = warehouse.worker
    wh = warehouse.copy()
    for action in action_seq:
        is_possible, state = check_move_validity(wh,action)
        apply_state_to_warehouse(wh,state)
        if not is_possible:
            return 'Impossible'
        
    return str(wh)


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
    sokoban_puzzle = SokobanPuzzle(warehouse=warehouse)
    f = search.breadth_first_graph_search(sokoban_puzzle)
    return f.solution(), f.path_cost


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if "__main__" == __name__:
    wh = sokoban.Warehouse()
    wh.load_warehouse("./warehouses/warehouse_03.txt")
#    test = solve_weighted_sokoban(wh)
    print(taboo_cells(wh))


    #search.breadth_first_graph_search(sokoban_puzzle)


