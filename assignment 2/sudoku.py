# Sudoku problems.
# The CSP.ac_3() and CSP.backtrack() methods need to be implemented

from csp import CSP, alldiff
import copy
import time


def print_solution(solution):
    """
    Convert the representation of a Sudoku solution, as returned from
    the method CSP.backtracking_search(), into a Sudoku board.
    """
    for row in range(width):
        for col in range(width):
            print(solution[f'X{row+1}{col+1}'], end=" ")
            if col == 2 or col == 5:
                print('|', end=" ")
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')


# Choose Sudoku problem
grid = open('sudoku_very_hard.txt').read().split()

width = 9
box_width = 3

domains = {}
for row in range(width):
    for col in range(width):
        if grid[row][col] == '0':
            domains[f'X{row+1}{col+1}'] = set(range(1, 10))
        else:
            domains[f'X{row+1}{col+1}'] = {int(grid[row][col])}

edges = []
for row in range(width):
    edges += alldiff([f'X{row+1}{col+1}' for col in range(width)])
for col in range(width):
    edges += alldiff([f'X{row+1}{col+1}' for row in range(width)])
for box_row in range(box_width):
    for box_col in range(box_width):
        cells = []
        edges += alldiff(
            [
                f'X{row+1}{col+1}' for row in range(box_row * box_width, (box_row + 1) * box_width)
                for col in range(box_col * box_width, (box_col + 1) * box_width)
            ]
        )

csp = CSP(
    variables=[f'X{row+1}{col+1}' for row in range(width) for col in range(width)],
    domains=domains,
    edges=edges,
)

# Function to print the domains of unknown variables
def print_domains(domains):
    for var, domain in domains.items():
        if len(domain) > 1:  # Only print domains of unknown variables
            print(f"{var}: {domain}")

# Function to calculate the reduction percentage
def calculate_reduction_percentage(original_domains, reduced_domains):
    original_count = sum(len(domain) for domain in original_domains.values() if len(domain) > 1)
    reduced_count = sum(len(domain) for domain in reduced_domains.values() if len(domain) > 1)
    reduction_percentage = ((original_count - reduced_count) / original_count) * 100
    return reduction_percentage

# Make a copy of the original domains to calculate reduction percentage later
original_domains = copy.deepcopy(csp.domains)

# Print domains before and after ac_3 for each unknown variable
print("Domains before and after ac_3:")

# Measure the runtime of the AC-3 algorithm
start_time_ac3 = time.time()  # Start the timer for AC-3
ac3_result = csp.ac_3()  # Run the AC-3 algorithm
end_time_ac3 = time.time()  # Stop the timer for AC-3

print(ac3_result)  # Print the result of AC-3 (True if successful, False otherwise)
for var in original_domains:
    if len(original_domains[var]) > 1:  # Only consider unknown variables
        print(f"{var}: before -> {original_domains[var]}, after -> {csp.domains[var]}")

# Calculate and print the reduction percentage
reduction_percentage = calculate_reduction_percentage(original_domains, csp.domains)
print(f"\n\nReduction in domains: {reduction_percentage:.2f}%\n\n")

# Measure the runtime of the backtracking search algorithm
start_time_backtrack = time.time()  # Start the timer for backtracking search
solution = csp.backtracking_search()  # Run the backtracking search algorithm
end_time_backtrack = time.time()  # Stop the timer for backtracking search

# Print the solution
print_solution(solution)

# Calculate and print the runtimes
runtime_ac3 = end_time_ac3 - start_time_ac3  # Calculate the runtime of AC-3
runtime_backtrack = end_time_backtrack - start_time_backtrack  # Calculate the runtime of backtracking search
total_runtime = runtime_ac3 + runtime_backtrack  # Calculate the total runtime

print(f"\n\nRuntime of AC-3 algorithm: {runtime_ac3:.4f} seconds")
print(f"Runtime of backtracking search algorithm: {runtime_backtrack:.4f} seconds")
print(f"Total runtime of AC-3 and backtracking search algorithms: {total_runtime:.4f} seconds\n\n")

# Expected output after implementing csp.ac_3() and csp.backtracking_search():
# True
# 7 8 4 | 9 3 2 | 1 5 6
# 6 1 9 | 4 8 5 | 3 2 7
# 2 3 5 | 1 7 6 | 4 8 9
# ------+-------+------
# 5 7 8 | 2 6 1 | 9 3 4
# 3 4 1 | 8 9 7 | 5 6 2
# 9 2 6 | 5 4 3 | 8 7 1
# ------+-------+------
# 4 5 3 | 7 2 9 | 6 1 8
# 8 6 2 | 3 1 4 | 7 9 5
# 1 9 7 | 6 5 8 | 2 4 3
