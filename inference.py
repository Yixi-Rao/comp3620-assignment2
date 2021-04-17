"""Inference functions used with backtracking search.

COMP3620/6320 Artificial Intelligence
The Australian National University
Authors: COMP-3620 team
Date:    2021

Student Details
---------------
Student Name: Yixi Rao
Student Number: u6826541
Date: 18/04/2021
"""

import collections
from typing import Callable, Dict, List, Optional, Tuple
import copy

from csp import CSP

Assignment = Dict[str, str]
Pruned = List[Tuple[str, str]]


def forward_checking(var: str, assignment: Assignment, gamma: CSP) -> Optional[Pruned]:
    """Implement the forward checking inference procedure.

        Parameters
        ----------
        var : str
            The name of the variable which has just been assigned.
        assignment : Dict[str, str]
            A Python dictionary of the current assignment. The dictionary maps
            variable names to values. The function cannot change anything in
            `assignment`.
        gamma : CSP
            An instance of the class CSP, representing the constraint network
            to which we are looking for a solution. The function cannot change
            anything in `gamma`.

        Returns
        -------
        pruned_list : Optional[Pruned]
            In the case that the algorithm detects a conflict, the assignment and
            CSP should remain unchanged and the function should return None.

            Otherwise, the algorithm should return a pruned_list, which is a list
            of (variable, value) pairs that will be pruned out of the domains of
            the variables in the problem. Think of this as the "edits" that are
            required to be done on the variable domains.
    """
    
    val          = assignment[var]
    Pruned_list  = []
    temp_domains = dict([(x, len(y)) for x,y in gamma.current_domains.items() if x in gamma.neighbours[var]])
    for neighbor, neighbor_conflicts_set in gamma.conflicts[(var, val)].items():
        for domain_val in gamma.current_domains[neighbor]:
            if domain_val in neighbor_conflicts_set:
                if temp_domains[neighbor] == 1:
                    return None
                else:
                    temp_domains[neighbor] = temp_domains[neighbor] - 1
                    Pruned_list.append((neighbor, domain_val))
    return Pruned_list
    
    
def arc_consistency(var: Optional[str], assignment: Assignment, gamma: CSP) -> Optional[Pruned]:
    """Implement the AC-3 inference procedure.

        Parameters
        ----------
        var : Optional[str]
            The name of the variable which has just been assigned. In the case that
            AC-3 is used for preprocessing, `var` will be `None`.
        assignment : Dict[str, str]
            A Python dictionary of the current assignment. The dictionary maps
            variable names to values. The function cannot change anything in
            `assignment`.
        gamma : CSP
            An instance of the class CSP, representing the constraint network
            to which we are looking for a solution. The function cannot change
            anything in `gamma`.

        Returns
        -------
        pruned_list : Optional[Pruned]
            In the case that the algorithm detects a conflict, the assignment and
            CSP should remain unchanged and the function should return None.

            Otherwise, the algorithm should return a pruned_list, which is a list
            of (variable, value) pairs that will be pruned out of the domains of
            the variables in the problem. Think of this as the "edits" that are
            required to be done on the variable domains.
    """
    
    pruned_list  = []
    temp_domains = dict([(x, list(y)) for x, y in gamma.current_domains.items()])
    
    if var == None:
        M = set([(x,y) for x in gamma.variables for y in gamma.neighbours[x]])
        while len(M) != 0:
            X_i, X_j = M.pop()
            no_conflict, Xi_pruned_list = Revise(gamma, temp_domains, X_i, X_j)
            if not no_conflict:
                return None
            if len(Xi_pruned_list) != 0:
                pruned_list.extend(Xi_pruned_list)
                for X_k in gamma.neighbours[X_i]:
                    if X_k != X_j:
                        M.add((X_k, X_i))
    else:
        M = set([(y, var) for y in gamma.neighbours[var]])
        while len(M) != 0:
            X_i, X_j = M.pop()
            no_conflict, Xi_pruned_list = Revise(gamma, temp_domains, X_i, X_j)
            if not no_conflict:
                return None
            if len(Xi_pruned_list) != 0:
                pruned_list.extend(Xi_pruned_list)
                for X_k in gamma.neighbours[X_i]:
                    if X_k != X_j:
                        M.add((X_k, X_i))
    return pruned_list

def Revise(gamma: CSP, temp_domains: list, X_i: str, X_j: str):
    """AI is creating summary for Revise

        Args:
            gamma (CSP): [description]
            X_i (str): [description]
            X_j (str): [description]

        Returns:
            [type]: [description]
    """  
    Xi_pruned_list = []
    Xi_domain_size = len(temp_domains[X_i])
    
    for Xi_val in temp_domains[X_i]:
        any_valid = False
        for Xj_domain_val in temp_domains[X_j]:
            if Xj_domain_val not in gamma.conflicts[(X_i, Xi_val)][X_j]:
                any_valid = True
                break
        if not any_valid:
            if Xi_domain_size == 1:
                return (False, [])
            else:
                Xi_domain_size = Xi_domain_size - 1
                Xi_pruned_list.append((X_i, Xi_val))
                temp_domains[X_i].remove(Xi_val)
                
    return (True, Xi_pruned_list)

# ------------- 1--------------------
    # def arc_consistency2(var: Optional[str], assignment: Assignment, gamma: CSP) -> Optional[Pruned]:
    #     """Implement the AC-3 inference procedure.

    #         Parameters
    #         ----------
    #         var : Optional[str]
    #             The name of the variable which has just been assigned. In the case that
    #             AC-3 is used for preprocessing, `var` will be `None`.
    #         assignment : Dict[str, str]
    #             A Python dictionary of the current assignment. The dictionary maps
    #             variable names to values. The function cannot change anything in
    #             `assignment`.
    #         gamma : CSP
    #             An instance of the class CSP, representing the constraint network
    #             to which we are looking for a solution. The function cannot change
    #             anything in `gamma`.

    #         Returns
    #         -------
    #         pruned_list : Optional[Pruned]
    #             In the case that the algorithm detects a conflict, the assignment and
    #             CSP should remain unchanged and the function should return None.

    #             Otherwise, the algorithm should return a pruned_list, which is a list
    #             of (variable, value) pairs that will be pruned out of the domains of
    #             the variables in the problem. Think of this as the "edits" that are
    #             required to be done on the variable domains.
    #     """
    #     M            = set([(x,y) for x in gamma.variables for y in gamma.neighbours[x]])
    #     pruned_list  = []
    #     temp_domains = dict([(x, list(y)) for x, y in gamma.current_domains.items()])
        
    #     while len(M) != 0:
    #         X_i, X_j = M.pop()
    #         no_conflict, is_revised = Revise2(gamma, temp_domains, pruned_list, X_i, X_j)
    #         if not no_conflict:
    #             return None
    #         if is_revised:
    #             for X_k in gamma.neighbours[X_i]:
    #                 if X_k != X_j:
    #                     M.add((X_k, X_i))
    #     return pruned_list

    # def Revise2(gamma: CSP, temp_domains: list, pruned_list: list, X_i: str, X_j: str):
    #     """AI is creating summary for Revise

    #         Args:
    #             gamma (CSP): [description]
    #             X_i (str): [description]
    #             X_j (str): [description]

    #         Returns:
    #             [type]: [description]
    #     """  
    #     is_revised     = False
    #     Xi_domain_size = len(temp_domains[X_i])
        
    #     for Xi_val in temp_domains[X_i]:
    #         any_valid = False
    #         for Xj_domain_val in temp_domains[X_j]:
    #             if Xj_domain_val not in gamma.conflicts[(X_i, Xi_val)][X_j]:
    #                 any_valid = True
    #                 break
    #         if not any_valid:
    #             if Xi_domain_size == 1:
    #                 return (False, [])
    #             else:
    #                 Xi_domain_size = Xi_domain_size - 1
    #                 is_revised     = True
    #                 pruned_list.append((X_i, Xi_val))
    #                 temp_domains[X_i].remove(Xi_val)
                    
    #     return (True, is_revised)

# ------------- 2--------------------
    # def arc_consistency0(var: Optional[str], assignment: Assignment, gamma: CSP) -> Optional[Pruned]:
    #     """Implement the AC-3 inference procedure.

    #         Parameters
    #         ----------
    #         var : Optional[str]
    #             The name of the variable which has just been assigned. In the case that
    #             AC-3 is used for preprocessing, `var` will be `None`.
    #         assignment : Dict[str, str]
    #             A Python dictionary of the current assignment. The dictionary maps
    #             variable names to values. The function cannot change anything in
    #             `assignment`.
    #         gamma : CSP
    #             An instance of the class CSP, representing the constraint network
    #             to which we are looking for a solution. The function cannot change
    #             anything in `gamma`.

    #         Returns
    #         -------
    #         pruned_list : Optional[Pruned]
    #             In the case that the algorithm detects a conflict, the assignment and
    #             CSP should remain unchanged and the function should return None.

    #             Otherwise, the algorithm should return a pruned_list, which is a list
    #             of (variable, value) pairs that will be pruned out of the domains of
    #             the variables in the problem. Think of this as the "edits" that are
    #             required to be done on the variable domains.
    #     """
    #     M            = set([(x,y) for x in gamma.variables for y in gamma.neighbours[x]])
    #     pruned_list  = []
    #     temp_domains = dict([(x, list(y)) for x, y in gamma.current_domains.items()])
        
    #     while len(M) != 0:
    #         X_i, X_j = M.pop()
    #         no_conflict, Xi_pruned_list = Revise(gamma, temp_domains, X_i, X_j)
    #         if not no_conflict:
    #             return None
    #         if len(Xi_pruned_list) != 0:
    #             pruned_list.extend(Xi_pruned_list)
    #             for X_k in gamma.neighbours[X_i]:
    #                 if X_k != X_j:
    #                     M.add((X_k, X_i))
    #     return pruned_list

# ------------- 3--------------------
    # def arc_consistency2(var: Optional[str], assignment: Assignment, gamma: CSP) -> Optional[Pruned]:
    #     """Implement the AC-3 inference procedure.

    #         Parameters
    #         ----------
    #         var : Optional[str]
    #             The name of the variable which has just been assigned. In the case that
    #             AC-3 is used for preprocessing, `var` will be `None`.
    #         assignment : Dict[str, str]
    #             A Python dictionary of the current assignment. The dictionary maps
    #             variable names to values. The function cannot change anything in
    #             `assignment`.
    #         gamma : CSP
    #             An instance of the class CSP, representing the constraint network
    #             to which we are looking for a solution. The function cannot change
    #             anything in `gamma`.

    #         Returns
    #         -------
    #         pruned_list : Optional[Pruned]
    #             In the case that the algorithm detects a conflict, the assignment and
    #             CSP should remain unchanged and the function should return None.

    #             Otherwise, the algorithm should return a pruned_list, which is a list
    #             of (variable, value) pairs that will be pruned out of the domains of
    #             the variables in the problem. Think of this as the "edits" that are
    #             required to be done on the variable domains.
    #     """
    #     M            = set([(x,y) for x in gamma.variables for y in gamma.neighbours[x] if x not in assignment and y not in assignment])
    #     pruned_list  = []
    #     temp_domains = dict([(x, list(y)) for x, y in gamma.current_domains.items()])
        
    #     while len(M) != 0:
    #         X_i, X_j = M.pop()
    #         no_conflict, Xi_pruned_list = Revise(gamma, temp_domains, X_i, X_j)
    #         if not no_conflict:
    #             return None
    #         if len(Xi_pruned_list) != 0:
    #             pruned_list.extend(Xi_pruned_list)
    #             for X_k in gamma.neighbours[X_i]:
    #                 if X_k != X_j and X_k not in assignment:
    #                     M.add((X_k, X_i))
    #     return pruned_list

# -------------------------------------------------------------------------------
# A function use to get the correct inference method for the search
# You do not need to touch this.
# -------------------------------------------------------------------------------

def get_inference_function(inference_type: str) -> Callable:
    """Return the function that does the specified inference."""
    if inference_type == "forward":
        return forward_checking
    if inference_type == "arc":
        return arc_consistency

    # If no inference is specified, we simply do nothing.
    def no_inference(var, assignment, csp):
        return []

    return no_inference
