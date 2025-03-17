import time

from .solver import SolutionSolver

def solve(cube_state, max_moves=25, max_duration=10.0):

    # create instance of solution_solver
    solution_solver = SolutionSolver(cube_state)
    timeout = time.time() + max_duration

    # solve cube
    solution = solution_solver.solve(max_moves, timeout)
    
    # process solution
    if isinstance(solution, str):
        return solution
    
    if solution == -2:
        raise RuntimeError('Timeout exceeded: no solution found!')
    
    if solution == -1:
        raise RuntimeError('No solution found, adjust max_moves')
    
    raise RuntimeError(f'Unexpected return value: {solution}')


if __name__ == "__main__":
    # Example input for testing
    cube_input = 'RFFUUUUUURRDRRBRRBFFFFFDFFDDDBDDBDDLULLLLLLLLRRBUBBUBB'
    try:
        solution = solve(cube_input)
        print(f"Solution: {solution}")
    except RuntimeError as e:
        print(f"Error: {e}")