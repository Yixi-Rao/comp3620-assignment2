"""Wumpus World.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: COMP-3620 team
Date: 2021

Student Details
---------------
Student Name: Yixi Rao
Student Number: u6826541
Date: 18/04/2021
"""
import argparse
import os
import sys
import itertools
from functools import reduce
from reference_n_to_bin import convert

class Wumpus_world:
    """this is the map of the Wumpus world and each cell in the map is represented as a cell_state
    """
    def __init__(self, c, r, num_w, num_p):
        """init function

            Args:
                c (int): the number of columns in the map
                r (int): the number of rows in the map
                num_w (int): the number of Wumpus in the map
                num_p (int): the number of pit in the map
        """
        self.X_max          = c     
        self.Y_max          = r
        self.num_wumpuses   = num_w
        self.num_pits       = num_p
        self.Map            = []
        self.observed_cells = set()
        self.cons_cells     = set()
        self.create_Map(self.X_max, self.Y_max)
        
    def create_Map(self, x_max, y_max):
        """ make the map to be a (c x r) grid map and initial cell state
        """
        for y in range(y_max):
            self.Map.append([])
            for x in range(x_max):
                self.Map[y].append(cell_state(x, y))
    
    def is_in_map(self, action: str, cur_x: int, cur_y: int):
        """to test whether the next action to the current position is a valid move, if it is a valid position
            it will return (true, next position) else (false, ())
            Returns:
                tuple: if it is a valid position it will return (true, next position) else (false, ())
        """
        if action == "north":
            next_x, next_y = cur_x, cur_y + 1
        elif action == "south":
            next_x, next_y = cur_x, cur_y - 1
        elif action == "west":
            next_x, next_y = cur_x - 1, cur_y
        else: 
            next_x, next_y = cur_x + 1, cur_y
        
        if (next_x > self.X_max - 1 or next_x < 0) or (next_y > self.Y_max - 1 or next_y < 0):
            return (False, ())
        else:
            return (True, (next_x, next_y)) 
    
    def adjacent_cells(self, x, y) ->list:
        """return the adjacent cells of the current position
            Returns:
                list: list of tuple of adjacent posiitons
        """
        directions = ["north", "south", "west", "east"]
        return [self.is_in_map(d, x, y)[1] for d in directions if self.is_in_map(d, x, y)[0]]
    
    def adjacent_risky_cells(self, x, y, safe_cells):
        """return the adjacent cells where it may be dangerous of the cells where it perceives something dangerous
        """
        return [c for c in self.adjacent_cells(x, y) if c not in safe_cells]
    
    def spread_safe(self, x, y):
        """if the (x,y) position does not perceive any thing, then we can reason that adjacent cells are also safe so updating the adjacent cells state
        """
        self.Map[y][x].update_state("S")
        neighbours = self.adjacent_cells(x, y)
        for n_x, n_y in neighbours:
            self.Map[n_y][n_x].update_state("S")
            
    def spread_pit(self, x, y):
        """if the (x,y) position perceives pit, then we can reason that adjacent cells may have pit so updating the adjacent cells state
        """
        self.Map[y][x].update_state("S")
        self.Map[y][x].update_percept("P")
        neighbours = self.adjacent_cells(x, y)
        for n_x, n_y in neighbours:
            self.Map[n_y][n_x].update_possible_state("P")      
            
    def spread_wumpus(self, x, y):
        """if the (x,y) position perceives wumpus, then we can reason that adjacent cells may have wumpus so updating the adjacent cells state
        """
        self.Map[y][x].update_state("S")
        self.Map[y][x].update_percept("W")
        neighbours = self.adjacent_cells(x, y)
        for n_x, n_y in neighbours:
            self.Map[n_y][n_x].update_possible_state("W")
    
    def get_risky_cells(self, perc_cells: set, observed_cells):
        """return all the cells where it may have pits or wumpus in it
            Returns:
                list: list of tuple of risky posiitons
        """
        r_cells = []
        for x, y in perc_cells:
            adj_cs = self.adjacent_cells(x, y)
            r_cells.extend([(x1, y1) for x1, y1 in adj_cs if (x1, y1) not in observed_cells and (x1, y1) not in r_cells]) # 
        return r_cells
        
    def get_cell_state(self, x, y):
        """return the (x,y) cell state
        """
        return self.Map[y][x].get_state()
    
    def get_cell_possible_states(self, x, y):
        """return the (x,y) all possible state
        """
        return self.Map[y][x].get_possible_states()
    
    def get_cell_percepts(self, x, y):
        """return the observation of the (x,y)
        """
        return self.Map[y][x].get_percepts()
    
class cell_state:
    """it contains the possible states of the cell, and a certain state. if the certain state is "" then it is unsure and the possible states is not empty
    """
    def __init__(self, loc_x, loc_y):
        """
            Args:
                loc_x (int): the locaiton x of the cell
                loc_y (int): the locaiton x of the cell
            """
        self.x               = loc_x
        self.y               = loc_y
        self.state           = ""    # certain state can only be "" "S" "W" "P"       
        self.possible_states = set() # the domain is {"P", "W", "S"}
        self.percepts        = set() # what the cell perceives
    
    def get_location(self):
        """retrun the location of the cell
        """
        return (self.x, self.y)
    
    def get_state(self):
        """retrun the state of the cell
        """
        return self.state
    
    def get_possible_states(self):
        """retrun the possible_states of the cell
        """
        return self.possible_states
    
    def get_percepts(self):
        """retrun the percepts of the cell
        """
        return self.percepts
    
    def update_percept(self, p):
        """update the percepts of the cell
        """
        self.percepts.add(p)
        
    def update_state(self, new_state):
        """update the certain state of the cell, and it only can be update to safe so clear all the possible states
        """
        self.state = new_state
        self.possible_states = set()
        
    def update_possible_state(self, state):
        """update the possible state of the cell, iff the certain state is unsure
        """
        if self.state == "":
            self.possible_states.add(state)

def process_command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments and return an object with attributes
    containing the parsed arguments or their default values.
    """
    import json

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", dest="input", metavar="INPUT",
                        type=str, help="Input file with the Wumpus World parameters and observations (MANDATORY)")
    parser.add_argument("-a", "--action", dest="action", metavar="ACTION",
                        type=str, choices=["north", "south", "east", "west"],
                        help="Action to be tested for safety (MANDATORY)")
    parser.add_argument("-o", "--output", dest="output", metavar="OUTPUT", default='wumpus_outputs',
                        help="Output folder (default: %(default)s)")

    args = parser.parse_args()
    if args.action is None:
        raise SystemExit("Error: No action was specified.")

    if args.input is None:
        raise SystemExit("Error: No input file was specified.")

    if not os.path.exists(args.input):
        raise SystemExit(
            "Error: Input file '{}' does not exist".format(args.input))

    try:
        with open(args.input) as instream:
            args.domain_and_observations = json.load(instream)
    except IOError:
        raise SystemExit("Error: could not open file {}".format(args.input))

    return args

def generate_constraint_domain(domain, n_adj):
    """using the permutations of the provided domain to generate the constraint domain such as constraint of there is at less one pit in the adjacent cells of the cell that feels breeze

        Args:
            domain (list): the list of value e.g. ["S","P"]
            n_adj (int): the number of variable involved in this constraint

        Raises:
            SystemExit: we don't need to use the permutations to generate the uanry constraint

        Returns:
            set: constraint domain
    """
    result = set()
    if len(domain) == 1:
        result = set(itertools.permutations([domain[0] for _ in range(n_adj)] + ['S' for _ in range(n_adj - 1)], n_adj))
    else:
        if n_adj == 1:
            raise SystemExit("Error: n_adj == 1 for [B,S].")
        if n_adj == 2:
            result = set(itertools.permutations(['W', 'P'], 2))
        elif n_adj == 3:
            result = set(itertools.permutations(['W','W', 'P', 'P'], 3)).union(set(itertools.permutations(['W', 'P', 'S'], 3)))
        else:
            result = set(itertools.permutations(['W','W','W', 'P', 'P','P'], 4)).union(set(itertools.permutations(['W','P','S','S'], 4)),
                                                                                       set(itertools.permutations(['W','P','P','S'], 4)),
                                                                                       set(itertools.permutations(['W','W','P','S'], 4)))
    return result

def generate_amount_domain(domain, n_adj, n_p, n_w):
    """To generate the amount constraint domain e.g. there are at most n_p pits and n_w wumpus in this n_adj cells
    """
    return set(itertools.permutations(["P" for _ in range(n_p)] + ['W' for _ in range(n_w)] + ['S' for _ in range(n_adj)], n_adj))

def main():
#--------------------------------------------- Section 0: definition ---------------------------------------------
    # Processes the arguments passed through the command line
    args = process_command_line_arguments()

    # The name of the action to test
    action = args.action

    # The path of the directory that will contain the generated CSP files
    output_path = args.output

    # The description of the Wumpus World features and sequence of observations
    # resulting from the agent actions.
    dao          = args.domain_and_observations
    n_rows       = dao["rows"]         # y
    n_columns    = dao["columns"]      # x
    n_wumpuses   = dao["wumpuses"]
    n_pits       = dao["pits"]
    observations = dao["observations"] # [ {"location" : [x,y], "percepts" : ["Breeze"]} ... ]

    # definition
    input_file              = args.input.split("/")[-1].split(".")[0]                   # the scenario 
    
    W_WORLD                 = Wumpus_world(n_columns, n_rows, n_wumpuses, n_pits)       # Wumpus_world instance
    cur_pos                 = observations[-1]["location"]                              # note that this is the scenario coordinate
    is_next_valid, test_pos = W_WORLD.is_in_map(action, cur_pos[0] - 1, cur_pos[1] - 1) # test_pos is the next position 
    observed_cells          = set()                                                     # set of all the cell which have observation
    observed_cons_cells     = set()                                                     # set of all the cell which perceive danger

#--------------------------------------------- Section 1: update the map ---------------------------------------------
    # if the next move is invalid than just quit
    if not is_next_valid:
        print("invalid move")
        return None

    # for all the observed cells update the KB and reason the possible states of the adjacent cells
    for ob in observations:
        obs_x, obs_y = tuple(ob["location"]) # note that this is the scenario coordinate 
        ob_percepts  = ob["percepts"]
        observed_cells.add((obs_x - 1, obs_y - 1))
        if len(ob_percepts) == 0: # perceive nothing. it is safe
            W_WORLD.spread_safe(obs_x - 1, obs_y - 1) 
        else:
            for pc in ob_percepts:
                if pc == "Breeze":
                    W_WORLD.spread_pit(obs_x - 1, obs_y - 1)
                    observed_cons_cells.add((obs_x - 1, obs_y - 1))
                elif pc == "Stench":
                    W_WORLD.spread_wumpus(obs_x - 1, obs_y - 1)
                    observed_cons_cells.add((obs_x - 1, obs_y - 1))

#--------------------------------------------- Section 2: doamin part -------------------------------------------------
    # this section will generate the state domain of the risky variables
    cell_domains = {} # variable domain dict e.g.{ (x,y):set("s","w","p") }
    risky_cells  = W_WORLD.get_risky_cells(observed_cons_cells, observed_cells) # all the risky cells that may have pit or wumpus
    
    for xr, yr in risky_cells:
        cell_domains[(xr, yr)] = W_WORLD.get_cell_possible_states(xr, yr)
        cell_domains[(xr, yr)].add("S")
    # the next position is a trivial safe position, so manually add it to domain
    if test_pos not in cell_domains:
        cell_domains[test_pos] = {"S"}

#--------------------------------------------- Section 3: constraints part ---------------------------------------------
    # this section will generate all the constraints of this problem, and its domain
    cell_constraints = [] # structure is same as the Ex5 default constraints structure
    for xp, yp in observed_cons_cells:
        adj_risky_cells = W_WORLD.adjacent_risky_cells(xp, yp, observed_cells)
        cons_domain = generate_constraint_domain(list(W_WORLD.get_cell_percepts(xp, yp)), len(adj_risky_cells))
        cell_constraints.append((tuple(adj_risky_cells), cons_domain))
    # this the amount constraints of the pits and wumpus
    amount_domain = generate_amount_domain(["P", "W", "S"], len(risky_cells),W_WORLD.num_pits, W_WORLD.num_wumpuses)
    cell_constraints.append((risky_cells, amount_domain))

    # this section will generate a special constsaint for ...a.csp which is the next position is not safe
    if W_WORLD.num_wumpuses == 0:
        a_constraint = ((test_pos,), {"P"})
        
    elif W_WORLD.num_pits == 0:
        a_constraint = ((test_pos,), {"W"})
    else:
        a_constraint = ((test_pos,), {"P", "W"})
        
    cell_constraints.append(a_constraint)

#--------------------------------------------- Section 4: file part ---------------------------------------------------
    # this seaction will write the a.csp file
    with open(output_path + "/" + input_file + "_" + action + "_a.csp", "w") as file:
        for pos, domain in cell_domains.items():
            file.write("var " + "".join([str(p) for p in pos]) + " : " +  " ".join(domain) + "\n")
            
        for cons_vars_tuple, cons_valid_set in cell_constraints:
            cons_vars = ["".join([str(x) for x in p]) for p in cons_vars_tuple]
            cons_valid_list = list(cons_valid_set)
            cons_valid_list[0] = " ".join(cons_valid_list[0])
            if len(cons_valid_list) == 1:
                file.write("con " + " ".join(cons_vars) + " : " + cons_valid_list[0] + "\n")
            else:
                file.write("con " + " ".join(cons_vars) + " : " + reduce(lambda x, y: x + " : " + " ".join(y), cons_valid_list) + "\n")

    # this seaction will write the b.csp file
    # this will generate a special constsaint for ...b.csp which is the next position is safe
    cell_constraints.remove(a_constraint)
    cell_constraints.append(((test_pos,), {"S"}))
    with open(output_path + "/" + input_file + "_" + action + "_b.csp", "w") as file:
        for pos, domain in cell_domains.items():
            file.write("var " + "".join([str(p) for p in pos]) + " : " +  " ".join(domain) + "\n")
            
        for cons_vars_tuple, cons_valid_set in cell_constraints:
            cons_vars = ["".join([str(x) for x in p]) for p in cons_vars_tuple]
            cons_valid_list = list(cons_valid_set)
            cons_valid_list[0] = " ".join(cons_valid_list[0])
            if len(cons_valid_list) == 1:
                file.write("con " + " ".join(cons_vars) + " : " + cons_valid_list[0] + "\n")
            else:
                file.write("con " + " ".join(cons_vars) + " : " + reduce(lambda x, y: x + " : " + " ".join(y), cons_valid_list) + "\n")
    
    try:
        convert(output_path + "/" + input_file + "_" + action + "_a.csp",  output_path + "/" + input_file + "_" + action + "_a.csp")
    except ValueError:
        # unsat
        print(input_file + "_" + action + "_a.csp " + "using toy binary csp")
        with open(output_path + "/" + input_file + "_" + action + "_a.csp", "w") as file:
            file.write("var a : 0" + "\n")
            file.write("con a : 1" + "\n")
    
    try:
        convert(output_path + "/" + input_file + "_" + action + "_b.csp",  output_path + "/" + input_file + "_" + action + "_b.csp")
    except ValueError:
        # unsat
        print(input_file + "_" + action + "_b.csp " + "using toy binary csp")
        with open(output_path + "/" + input_file + "_" + action + "_b.csp", "w") as file:
            file.write("var a : 0" + "\n")
            file.write("con a : 1" + "\n")
        
if __name__ == '__main__':
    main() 
