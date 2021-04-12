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


def main():
    args = process_command_line_arguments()
    input_path = args.input
    output_path = args.output
    variables, constraints = parse_nary_file(input_path)

    # *** YOUR CODE HERE ***


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
