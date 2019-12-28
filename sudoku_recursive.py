import time

def identifySquare(row, col):
    a = int(row / 3) * 3
    b = int(col / 3) * 3
    return [[a, b], [a, b + 1], [a, b + 2], [a + 1, b], [a + 1, b + 1], [a + 1, b + 2],
            [a + 2, b], [a + 2, b + 1], [a + 2, b + 2]]


def valid(num, row, col, board):
    square = identifySquare(row, col)
    a = True
    for k in range(9):
        if num == board[k][col]:
            a = False
            break
        if num == board[row][k]:
            a = False
            break
        if num == board[square[k][0]][square[k][1]]:
            a = False
            break
    return a


def backTrack(row, col, board):
    if col == len(board[row]):
        col = 0
        row += 1

    if row == len(board):
        return board

    if board[row][col] > 0:
        return backTrack(row, col + 1, board)

    for i in range(1, 10):
        num = i
        if valid(num, row, col, board):
            board[row][col] = num
            if backTrack(row, col + 1, board):
                return board
            board[row][col] = 0
    return False


def printB(board):
    print("Board:")
    print(board[0])
    print(board[1])
    print(board[2])
    print(board[3])
    print(board[4])
    print(board[5])
    print(board[6])
    print(board[7])
    print(board[8])
    print()


if __name__ == '__main__':
    # board = [' ' for x in range(80)]
    start_time = time.time()
    brd = [
        [0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 8, 0, 0, 0, 7, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 5, 0, 0],
        [0, 7, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 4, 0],
        [0, 0, 5, 0, 0, 0, 6, 0, 3],
        [0, 9, 0, 4, 0, 0, 0, 7, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0]]

    printB(backTrack(0, 0, brd))
    print("Program took:", time.time() - start_time, "to run")
