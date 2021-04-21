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

class Wumpus_world:
    def __init__(self, c, r, num_w, num_p):
        self.X_max   = c     
        self.Y_max   = r
        num_wumpuses = num_w
        num_pits     = num_p
        self.Map     = []
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
    
    def spread_safe(self, x, y):
        self.Map[y][x].update_state("S")
        neighbours = self.adjacent_cells(x, y)
        for n_x, n_y in neighbours:
            self.Map[n_y][n_x].update_state("S")
            
    def spread_pit(self, x, y):
        self.Map[y][x].update_state("s")
        neighbours = self.adjacent_cells(x, y)
        for n_x, n_y in neighbours:
            self.Map[n_y][n_x].update_possible_state("P")
            
    def spread_wumpus(self, x, y):
        self.Map[y][x].update_state("S")
        neighbours = self.adjacent_cells(x, y)
        for n_x, n_y in neighbours:
            self.Map[n_y][n_x].update_possible_state("W")
    
    def risky_cells(self, perc_cells: set):
        r_cells = []
        for x, y in perc_cells:
            adj_cs = self.adjacent_cells(x, y)
            r_cells.extend([(x1, y1) for x1, y1 in adj_cs if self.Map[y1][x1].get_state() == ""])
        return r_cells
        
    def get_cell_state(self, x, y):
        return self.Map[y][x].get_state()
    
    def get_cell_possible_states(self, x, y):
        return self.Map[y][x].get_possible_states()
    


    
class cell_state:
    def __init__(self, loc_x, loc_y):
        self.x               = loc_x
        self.y               = loc_y
        self.state           = "" 
        self.possible_states = set() # "pit", "wumpus"

        
    def get_location(self):
        return (self.x, self.y)
    
    def get_state(self):
        return self.state
    
    def get_possible_states(self):
        return self.possible_states
    
    def update_state(self, new_state):
        self.state = new_state
        self.possible_states.clear()
        
    def update_possible_state(self, state):
        if self.state != "":
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


def main():
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

    # YOUR CODE HERE
    W_WORLD  = Wumpus_world(n_columns, n_rows, n_wumpuses, n_pits)  
    cur_pos  = observations[-1]["location"] # 图坐标
    is_next_valid, test_pos = W_WORLD.is_in_map(action, cur_pos[0] - 1, cur_pos[1] - 1)
    percepts_cells = set()
    if not is_next_valid:
        print("invalid move")
        return None
    
    for ob in observations:
        obs_x, obs_y = tuple(ob["location"]) # 图坐标
        ob_percepts  = ob["percepts"]
        percepts_cells.add((obs_x - 1, obs_y - 1))
        if len(ob_percepts) == 0:
            W_WORLD.spread_safe(obs_x - 1, obs_y - 1)
        else:
            for pc in ob_percepts:
                if pc == "Breeze":
                    W_WORLD.spread_pit(obs_x - 1, obs_y - 1)
                elif pc == "Stench":
                    W_WORLD.spread_wumpus(obs_x - 1, obs_y - 1)
    
    cell_domains = {}
    for xr, yr in W_WORLD.risky_cells(percepts_cells):
        cell_domains[(xr,yr)] = W_WORLD.get_cell_possible_states(xr, yr)
        if (xr, yr) != test_pos:
            cell_domains[(xr,yr)].add("S")
            
    cell_constraints = []
    for xp, yp in percepts_cells:
        


if __name__ == '__main__':
    main()
