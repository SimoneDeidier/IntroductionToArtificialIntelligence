from typing import Any
from queue import Queue


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.
        
        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """
        def revise(xi: str, xj: str) -> bool:
            """Revises the domain of xi to ensure consistency with xj.
            
            Parameters
            ----------
            xi : str
                The variable whose domain is to be revised
            xj : str
                The variable with which xi must be consistent

            Returns
            -------
            bool
                True if the domain of xi was revised, False otherwise
            """
            revised = False
            # Iterate over a copy of the domain of xi to avoid modifying the domain while iterating
            for x in set(self.domains[xi]):
                # If there is no value y in the domain of xj such that (x, y) is allowed by the constraint
                if not any((x, y) in self.binary_constraints[(xi, xj)] for y in self.domains[xj]):
                    # Remove x from the domain of xi
                    self.domains[xi].remove(x)
                    revised = True
            return revised

        # Initialize the queue with all arcs in the CSP
        queue = Queue()
        for (xi, xj) in self.binary_constraints:
            queue.put((xi, xj))

        # Process the queue until it is empty
        while not queue.empty():
            (xi, xj) = queue.get()
            # If the domain of xi is revised
            if revise(xi, xj):
                # If the domain of xi is empty, the CSP is unsolvable
                if not self.domains[xi]:
                    return False
                # Add all arcs (xk, xi) to the queue to ensure consistency
                for xk in (set(self.variables) - {xj}):
                    if (xk, xi) in self.binary_constraints:
                        queue.put((xk, xi))
                    elif (xi, xk) in self.binary_constraints:
                        queue.put((xi, xk))

        return True

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        self.backtrack_calls = 0
        self.backtrack_failures = 0

        def backtrack(assignment: dict[str, Any]) -> None | dict[str, Any]:
            self.backtrack_calls += 1

            # Check if the assignment is complete
            if len(assignment) == len(self.variables):
                return assignment

            # Select an unassigned variable
            unassigned_vars = [v for v in self.variables if v not in assignment]
            var = unassigned_vars[0]

            # Try assigning each value in the domain of the variable
            for value in self.domains[var]:
                # Check if the value is consistent with the assignment
                if self.is_consistent(var, value, assignment):
                    # Assign the value
                    assignment[var] = value

                    # Recursively call backtrack with the new assignment
                    result = backtrack(assignment)
                    if result is not None:
                        return result

                    # If the result is None, remove the assignment (backtrack)
                    del assignment[var]

            self.backtrack_failures += 1
            return None

        result = backtrack({})
        print(f"\n\nBacktrack calls: {self.backtrack_calls}")
        print(f"Backtrack failures: {self.backtrack_failures}\n\n")
        return result

    def is_consistent(self, var: str, value: Any, assignment: dict[str, Any]) -> bool:
        """Checks if the value assignment is consistent with the current assignment.
        
        Parameters
        ----------
        var : str
            The variable to check
        value : Any
            The value to check
        assignment : dict[str, Any]
            The current assignment of variables

        Returns
        -------
        bool
            True if the assignment is consistent, False otherwise
        """
        for (var1, var2) in self.binary_constraints:
            # If var1 is the current variable and var2 is already assigned
            if var1 == var and var2 in assignment:
                # Check if the value pair (value, assignment[var2]) violates the constraint
                if (value, assignment[var2]) not in self.binary_constraints[(var1, var2)]:
                    return False
            # If var2 is the current variable and var1 is already assigned
            if var2 == var and var1 in assignment:
                # Check if the value pair (assignment[var1], value) violates the constraint
                if (assignment[var1], value) not in self.binary_constraints[(var1, var2)]:
                    return False
        return True


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables
    
    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]
