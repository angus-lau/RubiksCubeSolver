import time
from .solve import SolutionSolver

def solve(cube_state, max_moves=25, max_duration=10):

    # create instance of solution_solver
    ss = SolutionSolver(cube_state)

    # solve cube
    solution = ss.solve(max_moves, time.time() + max_duration)
    
    # process solution
    if isinstance(solution, str):
        return solution
    if solution == -2:
        raise RuntimeError('Timeout exceeded: no solution found!')
    if solution == -1:
        raise RuntimeError('No solution found, adjust max_moves')
    raise RuntimeError(f'Unexpected return value: {solution}')