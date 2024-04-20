
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
import time

class WarehouseProblem(search.Problem):
    def __init__(self, warehouse, initial):
        self.warehouse = warehouse
        self.initial = initial
        self.explored = []
        self.corners = []
        self.worker = initial

    def result(self, state, action):
        """
        Creates a new state from an applied action to a given state

        @param:
            state: The current state.
            action: The action to be applied.

        @return:
            tuple: The new state after applying the action.
        """
        assert action in self.actions(state)
        new_state = tuple(map(sum, zip(state, action)))
        if new_state not in self.explored: # If the cell is previously explored do nothing
            self.explored.append(new_state) 

            if self.is_corner(new_state) and new_state not in self.warehouse.targets:
                self.corners.append(new_state)
            
        return new_state

    def actions(self, state):
        """
        Generates all possible actions from the current state.

        @param:
            state: The current state.

        @return:
            list: A list of possible actions.
        """
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        possible_actions = []
        for move in moves:
            new_pos = tuple(map(sum, zip(state, move)))  # Calculate new position
            if self.is_valid_move(new_pos):
                possible_actions.append(move)
        return possible_actions

    def goal_test(self, state): # NO GOAL THEREFORE ALWAYS FALSE
        """
        Checks if the current state results in the goal condition.

        @param:
            state: The current state.

        @return:
            bool: True if the goal is satisfied, False otherwise.
        """
        return False

    def is_valid_move(self, pos):
        """
        Checks if a given position is a valid move.

        @param:
            pos: The position to check.

        @return:
            bool: True if the move is valid, False otherwise.
        """
        col, row = pos
        return (1 <= row < self.warehouse.nrows and
                1 <= col < self.warehouse.ncols and
                (col, row) not in self.warehouse.walls)
    
    def is_corner(self, state):
        col, row = state
        walls = self.warehouse.walls
        return ((col, row - 1) in walls and (col - 1, row) in walls or
                (col, row - 1) in walls and (col + 1, row) in walls or
                (col, row + 1) in walls and (col - 1, row) in walls or
                (col, row + 1) in walls and (col + 1, row) in walls)

    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [(10779566, 'Ryan','Uchino-Hansen'), (10779710,'Cody', 'Overs')]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_taboo_cord(warehouse):
    """
    Parent function to return a list of all cells that meet the taboo rules

    @param:
        warehouse: An object representing the warehouse layout.

    @returns:
        list: A list of taboo cells, including corners and taboo walls.
    """
    def find_corner_pairs(corners, warehouse):
        """
        Finds pairs of corners that satisfy certain conditions (col, row).

        @param:
            corners (list): A list of corner coordinates.
            warehouse: Intial warehouse layout.

        @return:
            list: A list of pairs of corner coordinates that satisfy the conditions.
        """
        return [(corners[row], corners[col]) 
                for row in range(len(corners)) 
                for col in range(row + 1, len(corners)) 
                if meets_taboo_conditions(corners[row], corners[col], warehouse) 
                and ((abs(corners[row][0] - corners[col][0]) > 1) or (abs(corners[row][1] - corners[col][1]) > 1)) 
                and (corners[row][0] == corners[col][0] or corners[row][1] == corners[col][1])]

    def meets_taboo_conditions(corner1, corner2, warehouse):
        """
        Checks if there are any taboo cells between two corners in a warehouse.

        @param:
            corner1: The first corner coordinate.
            corner2: The second corner coordinate.
            warehouse: Intial warehouse layout.

        @return:
            bool: True if there are no taboo conditions between the corners, False otherwise.
        """
        return all([
            all([
                ((corner1[0], row) in warehouse.walls or (corner1[0], row) in warehouse.targets) or not ((corner1[0] - 1, row) in warehouse.walls or (corner1[0] + 1, row) in warehouse.walls)
                for row in range(min(corner1[1], corner2[1]) + 1, max(corner1[1], corner2[1]))
            ]) if corner1[0] == corner2[0] else
            all([
                ((col, corner1[1]) in warehouse.walls or (col, corner1[1]) in warehouse.targets) or not ((col, corner1[1] - 1) in warehouse.walls or (col, corner1[1] + 1) in warehouse.walls)
                for col in range(min(corner1[0], corner2[0]) + 1, max(corner1[0], corner2[0]))
            ]) if corner1[1] == corner2[1] else
            True
        ])
    
    def coordinates_between_corners(corner1, corner2):
        """
        Generates coordinates between two corners along a row or column.

        @param:
            corner1: The first corner coordinate.
            corner2: The second corner coordinate.

        @return:
            list: A list of coordinates between the corners, forming a straight line along a row or column.
        """
        return [(corner1[0], row) for row in range(min(corner1[1], corner2[1]) + 1, max(corner1[1], corner2[1]))] if corner1[0] == corner2[0] else \
            [(col, corner1[1]) for col in range(min(corner1[0], corner2[0]) + 1, max(corner1[0], corner2[0]))] if corner1[1] == corner2[1] else \
            []
    
    def return_taboo_walls(corner_pairs):
        """
        Generates a list of taboo walls based on pairs of corners.

        @param:
            corner_pairs: A list of pairs of corner coordinates.

        @returns:
            list: A list of coordinates representing taboo walls between the given corner pairs.
        """
        return [cell for pair in corner_pairs for cell in coordinates_between_corners(pair[0], pair[1])]

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
        if warehouse.nrows - 1 != row:
            taboo += "\n"

    return taboo

def calculate_manhattan_distance(pos1, pos2):
    """
    Calcualte the manhattan distance between two points

    @param:
    pos1: first point
    pos2: second point

    @return:
    int: returns the manhattan distance
    """
    pos1 = list(pos1)
    pos2 = list(pos2)
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def is_aligned(pos1, pos2):
    """
    Gets if two poistions are aligned horizontally or vertically

    @param:
    pos1: first point
    pos2: second point

    @return:
    bool: true if aligned, else false
    """
    if pos1[0] == pos2[0]:
        return True
    if pos1[1] == pos2[1]:
        return True
    return False


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
        self.checked_moves = 0
        self.goal = tuple(warehouse.targets)
        self.taboo_cells = get_taboo_cord(self.wh)

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        @param:
        state: the current state

        @return:
        list: All of the valid moves with the given state
        """
        L = []
        #Up
        all_moves = ["Up", "Right", "Down", "Left"]
        for move in all_moves:
            is_possible, possible_state = check_move_validity(self.wh, move, state)

            if is_possible and not any(item in possible_state[1] for item in self.taboo_cells):
                L.append(move)
        return L
    

    def result(self, state, action):
        """
        Gets the next state from a given action

        @param:
        state: current state
        action: the action of the worker

        @return:
        tuple: the next state of the given state with the action
        """
        next_state = list(state)
        assert action in self.actions(state)
        is_possible, next_state = check_move_validity(self.wh,action, state)
        self.checked_moves += 1
        return next_state
     

    def goal_test(self, state):
        """
        checks if the boxes are on the targets
        
        @param:
        state: The state of the warehouse.

        @return:
        bool: true if all boxes are on top of goals, else returns false.
        """
        return set(state[1]) == set(self.goal)
    

    def h(self, node):
        """
        Returns the heuristic of the SokobanProblem. This heuristic calculates
        all of the distances between a box to a target and takes the most minimum
        distance per box. This considers only the closest box to a target so that
        the heuristic remains admissable. The cost of all of the box distances are 
        added together and returned

        @param:
        node: the current node in the frontier

        @return:
        int: The heuristic value
        """
        _, box_positions = node.state
        total_heuristic = 0

        for (box_pos, box_weight) in zip(box_positions, self.wh.weights):
            min_distance = float('inf')
            
            for target_pos in self.goal:
                
                distance = calculate_manhattan_distance(box_pos, target_pos) * (box_weight + 1)
                min_distance = min(min_distance, distance)
            
            if is_aligned(box_pos, target_pos):
                min_distance -= 1
            
            total_heuristic += min_distance
        
        return total_heuristic
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        box_state1 = state1[1]
        box_costs = self.wh.weights

        box_state2 = state2[1]
        push_cost = 0
        for index, (first, second) in enumerate(zip(box_state1, box_state2)):
            if first != second:
                push_cost = box_costs[index]
        return c + 1 + push_cost

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def apply_state_to_warehouse(warehouse,state):
    """
    applies the state to the warehouse code.
    Used mostly for when printing to terminal.

    @param:
    warehouse: a warehouse to have the state applied to
    state: a state which will be applied to the warehouse
    
    @return:
    None

    """
    warehouse.worker = list(state[0])
    warehouse.boxes = list(state[1])



def check_move_validity(warehouse, action, state=None):
        """
        Checks if the move is available

        @param:
        action: the action being taken
        state=None: the state being checked

        @return:
        bool: true if the move is valid, else false
        tuple: the next state that results from the action, None if not possible.
        """
        if state == None:
            state = (tuple(warehouse.worker), tuple(warehouse.boxes))
        #warehouse_clone = warehouse.copy()
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
        if worker in warehouse.walls:
            return False, None
        if worker in boxes:
            new_box = (worker[0] + diff[0], worker[1] + diff[1])
            if new_box in boxes or new_box in warehouse.walls:
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
        
        if not is_possible:
            return 'Impossible'
        apply_state_to_warehouse(wh,state)
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
    #f = search.breadth_first_graph_search(sokoban_puzzle)
    f = search.astar_graph_search(sokoban_puzzle)
    print(sokoban_puzzle.checked_moves)
    if f == None:
        return 'Impossible', None
    else:
        return f.solution(), f.path_cost


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if "__main__" == __name__:
    wh = sokoban.Warehouse()
    wh.load_warehouse("./warehouses/warehouse_00custom4.txt")
    print(taboo_cells(wh))
    time_start = time.time()
    print(solve_weighted_sokoban(wh))

    time_end = time.time()
    print('runtime: ' + str(time_end - time_start))



    #search.breadth_first_graph_search(sokoban_puzzle)


