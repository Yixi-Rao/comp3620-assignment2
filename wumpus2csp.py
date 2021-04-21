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
    def __init__(self, c, r, num_w, num_p):
        self.X_max          = c     
        self.Y_max          = r
        self.num_wumpuses   = num_w
        self.num_pits       = num_p
        self.Map            = []
        self.observed_cells = set()
        self.cons_cells     = set()
        self.create_Map(self.X_max, self.Y_max)
        
    def create_Map(self, x_max, y_max):
        """AI is creating summary for create_Map

            Args:
                x_max ([type]): x为图x
                y_max ([type]): y为图y
        """
        for y in range(y_max):
            self.Map.append([])
            for x in range(x_max):
                self.Map[y].append(cell_state(x, y))
    
    def is_in_map(self, action: str, cur_x: int, cur_y: int):
        """is_in_map

            Args:
                action (str): [description]
                cur_x (int): x 为坐标轴x
                cur_y (int): y 为坐标轴x
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
        directions = ["north", "south", "west", "east"]
        return [self.is_in_map(d, x, y)[1] for d in directions if self.is_in_map(d, x, y)[0]]
    
    def adjacent_risky_cells(self, x, y, safe_cells):
        return [c for c in self.adjacent_cells(x, y) if c not in safe_cells]
    
    def spread_safe(self, x, y):
        self.Map[y][x].update_state("S")
        neighbours = self.adjacent_cells(x, y)
        for n_x, n_y in neighbours:
            self.Map[n_y][n_x].update_state("S")
            
    def spread_pit(self, x, y):
        self.Map[y][x].update_state("S")
        self.Map[y][x].update_percept("P")
        neighbours = self.adjacent_cells(x, y)
        for n_x, n_y in neighbours:
            self.Map[n_y][n_x].update_possible_state("P")      
            
    def spread_wumpus(self, x, y):
        self.Map[y][x].update_state("S")
        self.Map[y][x].update_percept("W")
        neighbours = self.adjacent_cells(x, y)
        for n_x, n_y in neighbours:
            self.Map[n_y][n_x].update_possible_state("W")
    
    def get_risky_cells(self, perc_cells: set, observed_cells):
        r_cells = []
        for x, y in perc_cells:
            adj_cs = self.adjacent_cells(x, y)
            r_cells.extend([(x1, y1) for x1, y1 in adj_cs if (x1, y1) not in observed_cells and (x1, y1) not in r_cells]) # 
        return r_cells
        
    def get_cell_state(self, x, y):
        return self.Map[y][x].get_state()
    
    def get_cell_possible_states(self, x, y):
        return self.Map[y][x].get_possible_states()
    
    def get_cell_percepts(self, x, y):
        return self.Map[y][x].get_percepts()
    
class cell_state:
    def __init__(self, loc_x, loc_y):
        self.x               = loc_x
        self.y               = loc_y
        self.state           = "" 
        self.possible_states = set() # "P", "W", "S"
        self.percepts        = set()
    
    def get_location(self):
        return (self.x, self.y)
    
    def get_state(self):
        return self.state
    
    def get_possible_states(self):
        return self.possible_states
    
    def get_percepts(self):
        return self.percepts
    
    def update_percept(self, p):
        self.percepts.add(p)
        
    def update_state(self, new_state):
        self.state = new_state
        self.possible_states = set()
        
    def update_possible_state(self, state):
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
    """AI is creating summary for generate_constraint_domain

        Args:
            domain ([type]): [description]
            n_adj ([type]): [description]

        Raises:
            SystemExit: [description]

        Returns:
            [type]: [description]
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
    input_file              = args.input.split("/")[-1].split(".")[0]
    
    W_WORLD                 = Wumpus_world(n_columns, n_rows, n_wumpuses, n_pits)  
    cur_pos                 = observations[-1]["location"] # 图坐标
    is_next_valid, test_pos = W_WORLD.is_in_map(action, cur_pos[0] - 1, cur_pos[1] - 1)
    observed_cells          = set() # 坐标轴 set（（x，y））
    observed_cons_cells     = set()

#--------------------------------------------- Section 1: update the map ---------------------------------------------
    # if the next move is invalid than just quit
    if not is_next_valid:
        print("invalid move")
        return None

    # update the possible states attribute of all the risky cell and update the state attribute of all the safe cell
    for ob in observations:
        obs_x, obs_y = tuple(ob["location"]) # 图坐标
        ob_percepts  = ob["percepts"]
        observed_cells.add((obs_x - 1, obs_y - 1))
        if len(ob_percepts) == 0:
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
    # this section will generate the cell domain of the involved variables
    cell_domains = {} # { (x,y):set("s","w","p") }
    risky_cells  = W_WORLD.get_risky_cells(observed_cons_cells, observed_cells) # 坐标轴 list（（x，y））
    
    for xr, yr in risky_cells:
        cell_domains[(xr, yr)] = W_WORLD.get_cell_possible_states(xr, yr)
        cell_domains[(xr, yr)].add("S")
        
    if test_pos not in cell_domains:
        cell_domains[test_pos] = {"S"}

#--------------------------------------------- Section 3: constraints part ---------------------------------------------
    # this section will generate all the constraints of this problem 
    cell_constraints = [] 
    for xp, yp in observed_cons_cells:
        adj_risky_cells = W_WORLD.adjacent_risky_cells(xp, yp, observed_cells)
        cons_domain = generate_constraint_domain(list(W_WORLD.get_cell_percepts(xp, yp)), len(adj_risky_cells))
        cell_constraints.append((tuple(adj_risky_cells), cons_domain))

    amount_domain = generate_amount_domain(["P", "W", "S"], len(risky_cells),W_WORLD.num_pits, W_WORLD.num_wumpuses)
    cell_constraints.append((risky_cells, amount_domain))

    # this section will generate a special constsaint for ...a.csp 
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
        print(input_file + "_" + action + "_a.csp " + "using toy binary csp")
        with open(output_path + "/" + input_file + "_" + action + "_a.csp", "w") as file:
            file.write("var a : 0" + "\n")
            file.write("con a : 1" + "\n")
    
    try:
        convert(output_path + "/" + input_file + "_" + action + "_b.csp",  output_path + "/" + input_file + "_" + action + "_b.csp")
    except ValueError:
        print(input_file + "_" + action + "_b.csp " + "using toy binary csp")
        with open(output_path + "/" + input_file + "_" + action + "_b.csp", "w") as file:
            file.write("var a : 0" + "\n")
            file.write("con a : 1" + "\n")
        
if __name__ == '__main__':
    main() 
