"""Heuristics for variable selection and value ordering.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: COMP-3620 team
Date:    2021

Student Details
---------------
Student Name: Yixi Rao
Student Number: u6826541
Date: 18/04/2021

This is where you need to write your heuristics for variable selection and
value ordering.
"""
from typing import Callable, Dict, List, Optional

from csp import CSP
from queue import PriorityQueue

Assignment = Dict[str, str]


# -----------------------------------------------------------------------------
# Variable Selection Heuristics
# -----------------------------------------------------------------------------


def next_variable_lex(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Select the next variable by lexicographic order.

    Select the next variable from the remaining variables according to
    lexicographic order. We have implemented this one for you.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # gamma.variables is a list of variable names (as strings). See line 43 in
    # csp.py. We consider them in the order they are added in.
    for var in gamma.variables:
        if var not in assignment:
            return var
    return None


def next_variable_md(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement the most constraining variable (MD) heuristic.

    Choose the variable that that is involved in as many constraints as
    possible. See Lecture 11 for the precise definition. Break ties by
    lexicographic order.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    cur_MD_V = ("", 0)
    first = True
    for var in gamma.variables:
        if var not in assignment:
            num_con = len(list(filter(lambda x: x not in assignment, gamma.neighbours[var]))) 
            if first:
                cur_MD_V = (var, num_con)
                first = False
            else:
                if cur_MD_V[1] < num_con:
                    cur_MD_V = (var, num_con)
                
    if cur_MD_V[0]  != "":
        return cur_MD_V[0]
    else:    
        return None
    

def next_variable_mrv(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement the most constrained variable heuristic (MRV).

    Choose the variable with the smallest consistent domain. See Lecture 11 for
    the precise definition. Break ties by lexicographic order.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    # MRV_dict = {}
    MRV_var = ("", 0)
    first   = True
    for var in gamma.variables:
        if var not in assignment:
            domain_size = len(list(filter(lambda x: gamma.count_conflicts(var, x) == 0, gamma.current_domains[var])))
            if first:
                first   = False
                MRV_var = (var, domain_size)
            else:
                if MRV_var[1] > domain_size:
                    MRV_var = (var, domain_size)
                    # MRV_dict[var] = len(list(filter(lambda x: gamma.count_conflicts(var, x) == 0, gamma.current_domains[var])))
    if MRV_var[0] != "":
        return MRV_var[0]
    else:
        return None

def next_variable_md_mrv(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement MD heuristic, breaking ties with MRV.

    Choose the variable that is involved in as many constraints as possible. If
    there is a tie, choose the variable with the smallest consistent domain.
    See Lecture 11 for the precise definition.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the next variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    cur_MD_V = ("", 0)
    first = True
    for var in gamma.variables:
        if var not in assignment:
            num_con = len(list(filter(lambda x: x not in assignment, gamma.neighbours[var]))) 
            if first:
                cur_MD_V = (var, num_con)
                first = False
            else:
                if cur_MD_V[1] < num_con:
                    cur_MD_V = (var, num_con)
                elif cur_MD_V[1] == num_con:
                    cur_domain_size = len(list(filter(lambda x: gamma.count_conflicts(cur_MD_V[0], x) == 0, gamma.current_domains[cur_MD_V[0]])))
                    var_domain_size = len(list(filter(lambda x: gamma.count_conflicts(var,         x) == 0, gamma.current_domains[var])))
                    if cur_domain_size > var_domain_size:
                        cur_MD_V = (var, num_con)
                
    if cur_MD_V[0]  != "":
        return cur_MD_V[0]
    else:    
        return None


def next_variable_mrv_md(assignment: Assignment, gamma: CSP) -> Optional[str]:
    """Implement MRV heuristic, breaking ties with MD.

    Choose the variable with the smallest consistent domain. If there is a tie,
    choose the variable that is involved in as many constraints as
    possible. See Lecture 11 for the precise definition.

    Parameters
    ----------
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    variable : Optional[str]
        The name of the variable chosen by this heuristic. If there are no
        remaining unassigned variables, we return None.

    """
    MRV_var = ("", 0)
    first   = True
    for var in gamma.variables:
        if var not in assignment:
            domain_size = len(list(filter(lambda x: gamma.count_conflicts(var, x) == 0, gamma.current_domains[var])))
            if first:
                first   = False
                MRV_var = (var, domain_size)
            else:
                if MRV_var[1] > domain_size:
                    MRV_var = (var, domain_size)
                elif MRV_var[1] == domain_size:
                    cur_num_con = len(list(filter(lambda x: x not in assignment, gamma.neighbours[MRV_var[0]]))) 
                    var_num_con = len(list(filter(lambda x: x not in assignment, gamma.neighbours[var]))) 
                    if var_num_con > cur_num_con:
                        MRV_var = (var, domain_size)
    if MRV_var[0] != "":
        return MRV_var[0]
    else:
        return None

# -----------------------------------------------------------------------------
# Value Ordering Heuristics
# -----------------------------------------------------------------------------


def value_ordering_lex(var: str, assignment: Assignment, gamma: CSP) -> List[str]:
    """Order the values based on lexicographic order.

    In this heuristic, variable values are ordered in lexicographic order. We
    have implemented this heuristic for you. We make use of the attribute
    `gamma.current_domains` to be useful. This is a dictionary that maps a
    variable name (a string) to a set of values (a set of strings) in that
    variable's current domain.

    Parameters
    ----------
    var : str
        The name of the variable which we want to assign a value.
    assignment : Dict[str, str]
        A Python dictionary that maps variable names to values.
    gamma : CSP
        An instance of the class CSP, representing the constraint network
        to which we are looking for a solution.

    Returns
    -------
    values : List[str]
        A list the values (represented a strings) in the current domain of the
        variable, sorted according to this heuristic.

    """
    # We need to explicitly convert a set to a list.
    return list(gamma.current_domains[var])


def value_ordering_lcvf(var: str, assignment: Assignment, gamma: CSP) -> List[str]:
    """Order the values based on the Least Constraining Value heuristic.

        This heuristic returns values in order of how constraining they are. It
        prefers the value that rules out the fewest choices for the neighbouring
        variables in the constraint graph. In other words,  it prefers values which
        remove the fewest elements from the current domains of their neighbouring
        variables.

        See Lecture 11 for the precise definition. You might find the attribute
        `gamma.current_domains` to be useful. This is a dictionary that maps a
        variable name (a string) to a set of values (a set of strings) in that
        variable's current domain.

        Parameters
        ----------
        var : str
            The name of the variable which we want to assign a value.
        assignment : Dict[str, str]
            A Python dictionary that maps variable names to values.
        gamma : CSP
            An instance of the class CSP, representing the constraint network
            to which we are looking for a solution.

        Returns
        -------
        values : List[str]
            All the values in  the current domain of the variable, sorted according
            to this heuristic.
    """
    # sorted_values = []
    # for val in gamma.current_domains[var]:
    #     num_invalid = count_conflict_values(var, val, assignment, gamma)
    #     sorted_values.append((num_invalid, val))
    return [y for x,y in sorted([(count_conflict_values(var, x, assignment, gamma), x) for x in gamma.current_domains[var]])]            
        
def count_conflict_values(var: str, val : str, assignment: Assignment, gamma: CSP):
    """AI is creating summary for count_conflict_values

    Args:
        var (str): [description]
        val (str): [description]
        assignment (Assignment): [description]
        gamma (CSP): [description]

    Returns:
        [type]: [description]
    """
    n_conflict_value = 0
    for neighbor, neighbor_conflicts in gamma.conflicts[(var, val)].items():
        if neighbor not in assignment:
            for neighbor_value in gamma.current_domains[neighbor]:
                if neighbor_value in neighbor_conflicts:
                    n_conflict_value += 1
            
    return n_conflict_value


# -------------------------------------------------------------------------------
# Functions used by the system to select from the above heuristics for the search
# You do not need to look any further.
# -------------------------------------------------------------------------------

def get_variable_selection_function(variable_heuristic: str) -> Callable:
    """Return the appropriate variable selection function."""
    if variable_heuristic == "lex":
        return next_variable_lex
    if variable_heuristic == "md":
        return next_variable_md
    if variable_heuristic == "mrv":
        return next_variable_mrv
    if variable_heuristic == "md-mrv":
        return next_variable_md_mrv
    if variable_heuristic == "mrv-md":
        return next_variable_mrv_md

    raise ValueError(f"Error: the variable selection heuristic "
                     f"'{variable_heuristic}' is not supported")


def get_value_ordering_function(value_heuristic: str) -> Callable:
    """Return the appropriate value ordering function."""
    if value_heuristic == "lex":
        return value_ordering_lex
    if value_heuristic == "lcvf":
        return value_ordering_lcvf

    raise ValueError(f"Error: the value selection heuristic "
                     f"'{value_heuristic}' is not supported")
