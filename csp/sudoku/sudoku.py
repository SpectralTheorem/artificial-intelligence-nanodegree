from timeit import default_timer as timer
import z3


def sudoku(board):
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = [[z3.Int('{}{}'.format(r, c)) for c in cols] for r in rows]

    s_solver = z3.Solver()

    for row in boxes:
        for box in row:
            s_solver.add(1 <= box, box <= 9)
    for row in boxes:
        s_solver.add(z3.Distinct(row))
    for col in zip(*boxes):
        s_solver.add(z3.Distinct(col))
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            s_solver.add(
                z3.Distinct([
                    boxes[i + ii][j + jj]
                    for ii in range(3) for jj in range(3)
                ])
            )
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                s_solver.add(boxes[i][j] == board[i][j])

    return s_solver, boxes

def print_board(board):
    for i in range(9):
        if i > 0 and i % 3 == 0:
            print('---------|---------|---------')
        for j in range(9):
            if j > 0 and j % 3 == 0:
                print('|', end='')
            print(' {} '.format(board[i][j]), end='')
        print()
    print()

def print_solution(s_solver, boxes):
    for i in range(9):
        if i > 0 and i % 3 == 0:
            print('---------|---------|---------')
        for j in range(9):
            if j > 0 and j % 3 == 0:
                print('|', end='')
            print(' {} '.format(s_solver.model()[boxes[i][j]]), end='')
        print()
    print()

if __name__ == '__main__':
    # World's hardest sudoku
    board = ((8, 0, 0, 0, 0, 0, 0, 0, 0),
             (0, 0, 3, 6, 0, 0, 0, 0, 0),
             (0, 7, 0, 0, 9, 0, 2, 0, 0),
             (0, 5, 0, 0, 0, 7, 0, 0, 0),
             (0, 0, 0, 0, 4, 5, 7, 0, 0),
             (0, 0, 0, 1, 0, 0, 0, 3, 0),
             (0, 0, 1, 0, 0, 0, 0, 6, 8),
             (0, 0, 8, 5, 0, 0, 0, 1, 0),
             (0, 9, 0, 0, 0, 0, 4, 0, 0))
    print('World hardest sudoku')
    print_board(board)
    input("Press Enter to continue...")

    start = timer()
    s_solver, boxes = sudoku(board)
    if s_solver.check() == z3.sat:
        print_solution(s_solver, boxes)
        end = timer()
        print("Solution found in: {:.2f} ms".format((end - start)*1000))
    else:
        print('Uh oh. The solver did not find a solution.')
