tested = 0
'''
Aufgabe 1 - Sudoku

Write a Sudoku solver.
Use a generator that takes as argument a partial board, chooses an unfilled position,
and enumerates all valid boards that have this position filled.
Remember to write tests first.
'''

# Example Wikipedia board 9x9 board
# has just one solution
board = [[0, 7, 0, 0, 0, 0, 0, 8, 0],
         [0, 0, 8, 5, 9, 6, 0, 0, 2],
         [3, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 4, 0, 6, 0, 5, 8, 0, 0],
         [7, 0, 0, 0, 2, 0, 0, 0, 3],
         [0, 0, 6, 8, 0, 7, 0, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 8],
         [1, 0, 0, 3, 8, 4, 6, 0, 0],
         [0, 6, 0, 0, 0, 0, 0, 9, 0]]

# has 2 solutions
non_unique = [[9, 0, 6, 0, 7, 0, 4, 0, 3],
              [0, 0, 0, 4, 0, 0, 2, 0, 0],
              [0, 7, 0, 0, 2, 3, 0, 1, 0],
              [5, 0, 0, 0, 0, 0, 1, 0, 0],
              [0, 4, 0, 2, 0, 8, 0, 6, 0],
              [0, 0, 3, 0, 0, 0, 0, 0, 5],
              [0, 3, 0, 7, 0, 0, 0, 5, 0],
              [0, 0, 7, 0, 0, 5, 0, 0, 0],
              [4, 0, 5, 0, 1, 0, 7, 0, 8]]

# easy one where only 1 number is missing
easy = [[6, 7, 9, 2, 1, 3, 5, 8, 4],
        [4, 1, 8, 5, 9, 6, 7, 3, 2],
        [3, 5, 2, 4, 7, 8, 9, 1, 6],
        [2, 4, 1, 6, 3, 5, 8, 7, 9],
        [7, 8, 5, 9, 2, 1, 4, 6, 3],
        [9, 3, 6, 8, 4, 7, 2, 5, 1],
        [5, 2, 3, 7, 6, 9, 1, 4, 8],
        [1, 9, 7, 3, 8, 4, 6, 2, 5],
        [8, 6, 4, 1, 5, 2, 3, 9, 0]]


def get_solutions(board):
    global tested

    '''
    for i in board:
        print(i)
    print()
    '''

    if not has_zeroes(board):
        if valid_board(board):
            # print ("Boards created: \t {}".format(tested))
            yield board

    for row, col in ((y, x) for y in range(0, 9) for x in range(0, 9)):
        # print("CHECKING",(row,col))
        if board[row][col] != 0:
            continue
        for num in range(1, 10):
            tested += 1
            board[row][col] = num
            print ("Boards created: \t {}".format(tested), end="\r")
            if valid_board(board):
                try:
                    for i in get_solutions(board):
                        yield i
                except StopIteration:
                    continue
        board[row][col] = 0
        break


def valid_board(board):
    # check rows
    for row in board:
        if not is_line_valid(row):
            return False

    # check columns
    for i in range(0, 9):
        col = [board[j][i] for j in range(0, 9)]
        if not is_line_valid(col):
            return False

    # check every 9 element block
    for i in range(0, 3):
        blocks = [[], [], []]
        for j in range(0, 3):
            for k in range(0, 3):
                blocks[k].extend(board[(j + 3 * i)][(k * 3):((k + 1) * 3)])
        for b in blocks:
            if not is_line_valid(b):
                return False

    return True


def is_line_valid(line):
    used = list()
    for i in line:
        if i == 0:
            continue
        if i in used:
            return False
        used.append(i)
    return True


def has_zeroes(board):
    for row in board:
        for col in row:
            if col == 0:
                return True
    return False

######################################################

test = non_unique  # <---- SET sudoku board here
a = get_solutions(test)
print("Provided board:")
for i in test:
    print (i)
print()

solutions = 0
while True:
    try:
        s = next(a)
        print()
        for i in s:
            print (i)
        solutions += 1
        print ("Solutions found:\t {}".format(solutions))
        print()
    except StopIteration:
        break
