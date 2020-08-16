import z3
from util import display_board

def n_queens(N):
    if N >= 100:
        raise ValueError('Please specify a value smaller than 100')

    nq_solver = z3.Solver()

    # Add variables
    # We know each queen must be in a different row.
    # So, we represent each queen by a single integer: the column position
    Q = [z3.Int('Q{}'.format(i)) for i in range(N)]

    # Add constraint
    # Add range constraint
    for i in range(N):
        nq_solver.add(0 <= Q[i], Q[i] < N)
    # Add row constraint
    nq_solver.add(z3.Distinct(Q))
    # Add diagonal constraint
    for i in range(N):
        for j in range(i):
            if i == j: continue
            nq_solver.add(Q[i] - Q[j] != i - j)
            nq_solver.add(Q[i] - Q[j] != j - i)

    return nq_solver

if __name__ == '__main__':
    nq_solver = n_queens(8)
    nq_solver.check()
    s = nq_solver.model()
    display_board([(int(str(v)[1:]), s[v].as_long()) for v in s], len(s))
