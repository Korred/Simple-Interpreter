def test_sudoku():
    board = [[0,3,0,0,0,0,0,0,9],
             [0,0,0,1,9,5,0,0,0],
             [0,0,8,0,0,0,0,6,0],
             [3,0,0,0,6,0,0,0,0],
             [4,0,0,0,0,0,0,0,1],
             [0,0,0,0,0,0,0,0,0],
             [0,6,0,0,0,0,0,0,0],
             [0,0,0,4,1,9,0,0,5],
             [0,0,0,0,0,0,0,7,0]]
    gen = solve_sudoku(board,(0,0))
    sol = next(gen)
    assert sol == [[1,3,0,0,0,0,0,0,9],
                   [0,0,0,1,9,5,0,0,0],
                   [0,0,8,0,0,0,0,6,0],
                   [3,0,0,0,6,0,0,0,0],
                   [4,0,0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,0,0,0],
                   [0,6,0,0,0,0,0,0,0],
                   [0,0,0,4,1,9,0,0,5],
                   [0,0,0,0,0,0,0,7,0]]
    sol = next(gen)
    assert sol == [[2,3,0,0,0,0,0,0,9],
                   [0,0,0,1,9,5,0,0,0],
                   [0,0,8,0,0,0,0,6,0],
                   [3,0,0,0,6,0,0,0,0],
                   [4,0,0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,0,0,0],
                   [0,6,0,0,0,0,0,0,0],
                   [0,0,0,4,1,9,0,0,5],
                   [0,0,0,0,0,0,0,7,0]]
    sol = next(gen)
    assert sol == [[5,3,0,0,0,0,0,0,9],
                   [0,0,0,1,9,5,0,0,0],
                   [0,0,8,0,0,0,0,6,0],
                   [3,0,0,0,6,0,0,0,0],
                   [4,0,0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,0,0,0],
                   [0,6,0,0,0,0,0,0,0],
                   [0,0,0,4,1,9,0,0,5],
                   [0,0,0,0,0,0,0,7,0]]
    sol = next(gen)
    assert sol == [[6,3,0,0,0,0,0,0,9],
                   [0,0,0,1,9,5,0,0,0],
                   [0,0,8,0,0,0,0,6,0],
                   [3,0,0,0,6,0,0,0,0],
                   [4,0,0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,0,0,0],
                   [0,6,0,0,0,0,0,0,0],
                   [0,0,0,4,1,9,0,0,5],
                   [0,0,0,0,0,0,0,7,0]]
    sol = next(gen)
    assert sol == [[7,3,0,0,0,0,0,0,9],
                   [0,0,0,1,9,5,0,0,0],
                   [0,0,8,0,0,0,0,6,0],
                   [3,0,0,0,6,0,0,0,0],
                   [4,0,0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,0,0,0],
                   [0,6,0,0,0,0,0,0,0],
                   [0,0,0,4,1,9,0,0,5],
                   [0,0,0,0,0,0,0,7,0]]

def solve_sudoku(board,pos):
    """sudoku solver using generators, board is a string,
       pos is an unfilled position that we want to find a valid value for"""
    if sudoku_is_valid(board):
        for i in range(1,9):
            board[pos[0]][pos[1]] = i
            if (sudoku_is_valid(board)):
                yield board
            else:
                board[pos[0]][pos[1]] = 0

def sudoku_is_valid(board):
    "check if a sudoku board is valid, i.e. rows, cols and squares have all different values"
    # rows
    for row in board:
        for i in range(1,10):
            if (len(list_intersection(row,[i])) > 1):
                return False
    # columns
    for i in range(0,9):
        for j in range(1,10):
            if (len(list_intersection([r[i] for r in board],[j])) > 1):
                    return False
    # squares
    for i in [0,3,6]:
        row1 = board[i]
        row2 = board[i+1]
        row3 = board[i+2]
        for j in [0,3,6]:
            square = []
            square.append(row1[j:j+3])
            square.append(row2[j:j+3])
            square.append(row3[j:j+3])
            square = sum(square,[])
            for k in range(1,10):
                if (len(list_intersection(square,[k])) > 1):
                        return False
    return True

def list_intersection(a,b):
    "intersection of two lists"
    return [e for e in a if e in b]