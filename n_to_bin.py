"""N-ary to binary constraint compiler.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: COMP-3620 team
Date:    2021

Student Details
---------------
Student Name:
Student Number:
Date:
"""
import argparse
import os
import sys
from typing import Dict, List, Set, Tuple
from functools import reduce


def process_command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments and return an object with attributes
    containing the parsed arguments or their default values.

    Returns
    -------
    args : an argparse.Namespace object
        This object will have two attributes:
            - input: a string with the path of the input file specified via
            the command line.
            - output: a string with the path of the file where the binarised
            CSP is to be found.

    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", dest="input", metavar="INPUT",
                        type=str, help="Input file with an n-ary CSP (MANDATORY)")
    parser.add_argument("-o", "--output", dest="output", metavar="OUTPUT",
                        default='binarised.csp',
                        help="File to write the binarised CSP (default: %(default)s)")

    args = parser.parse_args()
    if args.input is None:
        raise SystemExit("Error: No input file was specified.")

    if not os.path.exists(args.input):
        raise SystemExit(
            "Error: Input file '{}' does not exist".format(args.input))

    return args

def modify_tuple(ori_tuple: tuple, offsets: list):
    temp = list(ori_tuple)
    
    for index, offset in enumerate(offsets):
        temp[index] = ori_tuple[index + offset]

    return tuple(temp)
    
    
def main():
    args                   = process_command_line_arguments()
    input_path             = args.input
    output_path            = args.output
    variables, constraints = parse_nary_file(input_path)

    # unary_cons = list(filter(lambda x: len(x[0]) == 1, constraints))
    # if len(unary_cons) != 0:
    #     for unary_var, unary_domain in unary_cons:
    #         variables[unary_var] = variables[unary_var].intersection(set(unary_domain))
    
    
    bin_variables   = variables # This is the new binary variables dictionary inclued the union variables -> (x,y,z) : set((1,2,3),(3,4,5)...)
    bin_constraints = []        # This is the new binary constraints list inclued the union variables -> [ ( (x,y,z),[(1,1,2),(2,2,3)...] ), ]
    union_var_dict  = {}        # a dictionry to check whether there is a duplicated union variable constraint -> (x,y,z) : set(x,y,z)
    bin_var_dict    = {}        # a dictionry to check whether there is a duplicated binary variable constraint -> {(x,y) : set((1,1),(2,4)...)}
    
    for cons_vars, cons_valid_list in constraints:
        if len(cons_vars) > 2:
            if set(cons_vars) not in union_var_dict.values():
                bin_variables[cons_vars]  = set(cons_valid_list) 
                union_var_dict[cons_vars] = set(cons_vars)
    
            else:
                if cons_vars in union_var_dict:
                    bin_variables[cons_vars] = bin_variables[cons_vars].intersection(set(cons_valid_list))
                    if len(bin_variables[cons_vars]) == 0:
                        print("Unsatisfiable constraints")
                        return None
                else:
                    var_key                  = list(union_var_dict.keys())[list(union_var_dict.values()).index(set(cons_vars))]
                    var_offsets              = [var_key.index(cons_vars[i]) - i for i in range(len(cons_vars))]
                    
                    revised_valid_list       = set(map(lambda x :modify_tuple(x, var_offsets), cons_valid_list))
                    
                    bin_variables[var_key]   = bin_variables[var_key].intersection(revised_valid_list)
                    if len(bin_variables[var_key]) == 0:
                        print("Unsatisfiable constraints")
                        return None
                            
        else:
            b_x, b_y = cons_vars
            if ((b_x,b_y) in bin_var_dict) or ((b_y,b_x) in bin_var_dict):
                bin_var_dict[cons_vars] = bin_var_dict[cons_vars].intersection(set(cons_valid_list)) if (b_x, b_y) in bin_var_dict else bin_var_dict[cons_vars].intersection(set([(y,x) for x,y in cons_valid_list]))
                if len(bin_var_dict[cons_vars]) == 0:
                    print("Unsatisfiable constraints")
                    return None
            else:
                bin_var_dict[cons_vars] = set(cons_valid_list)
            
    for x_y, bin_domain in bin_var_dict.items():
        bin_constraints.append((x_y, list(bin_var_dict)))
        
    for u_vars in union_var_dict.keys():
        for o_index, o_var in enumerate(u_vars):
            o_domain = bin_variables[o_var]
            bin_constraints.append((
                                    (o_var, "".join(u_vars)),
                                    [(x[o_index], str(x)) for x in bin_variables[u_vars] if x[o_index] in o_domain]
                                   ))
            
    with open(output_path, "w") as file:
        for bin_var, bin_domain in bin_variables.items():
            file.write("var " + "".join(bin_var) + " : " +  " ".join([str(x) for x in bin_domain]) + "\n")
        for cons_vars, cons_valid_list in bin_constraints:
            cons_valid_list[0] = " ".join(cons_valid_list[0])
            if len(cons_valid_list) == 1:
                file.write("con " + " ".join(cons_vars) + " : " + cons_valid_list[0] + "\n")
            else:
                file.write("con " + " ".join(cons_vars) + " : " + reduce(lambda x, y: x + " : " + " ".join(y), cons_valid_list) + "\n")

# -----------------------------------------------------------------------------
# You might like to use the helper functions below. Feel free to modify these
# functions to suit your needs.
# -----------------------------------------------------------------------------


def parse_nary_file(file_name: str):
    """Parse an n-ary CSP file.

        Parameters
        ----------
        file_name : str
            The path to the n-ary CSP file.

        Returns
        -------
        variables : Dict[str, Set[str]]
            A dictionary mapping variable names to their domains. Each domain is
            represented by a set of values.

        constraints : List[Tuple[Tuple[str, ...], List[Tuple[str, ...]]]]
            A list of constraints. Each constraint is a tuple with two elements:
                1) The first element is the tuple of the variables involved in the
                constraint, e.g. ('x', 'y', 'z').

                2) The second element is the list of values those variables are
                allowed to take, e.g. [('0', '0', '0'), ('0', '1', '1')].

    """
    variables: Dict[str, Set[str]] = {}
    constraints: List[Tuple[Tuple[str, ...], List[Tuple[str, ...]]]] = []

    with open(file_name, "r") as file:
        for line in file:
            if line.startswith('var'):
                var_names, domain = line[3:].split(':')
                domain_set = set(domain.split())
                for v in var_names.split():
                    variables[v] = domain_set

            elif line.startswith('con'):
                content = line[3:].split(':')
                vs = tuple(content[0].split())
                values = [tuple(v.split()) for v in content[1:]]
                constraints.append((vs, values))

    return variables, constraints


if __name__ == '__main__':
    main()
