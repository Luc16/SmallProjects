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


def make_implications(board, row, col, implicated):
    can_implicate = True
    while can_implicate:
        prev_board = board
        while row < len(board):
            nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            if board[row][col] == 0:
                square = identifySquare(row, col)
                for k in range(9):
                    _col = board[k][col]
                    _row = board[row][k]
                    sqr = board[square[k][0]][square[k][1]]
                    if 0 != _col and _col in nums:
                        nums.remove(_col)
                    if 0 != _row and _row in nums:
                        nums.remove(_row)
                    if 0 != sqr and sqr in nums:
                        nums.remove(sqr)
            if len(nums) == 1:
                implicated.append([row, col])
                board[row][col] = nums[0]
            col += 1
            if col == len(board[row]):
                col = 0
                row += 1
        if board == prev_board:
            return implicated


def delete_implications(board, implicated):
    deleted = []
    if len(implicated) > 0:
        for i in implicated:
            deleted.append([i[0], i[1]])
            board[i[0]][i[1]] = 0
        deleted.sort()
    return deleted


def next(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                return [row, col]


def back_track_w_impl(board, impl, row=0, col=0):
    nxt = next(board)
    if nxt is None:
        return True
    row = nxt[0]
    col = nxt[1]

    if row == -1:
        # print('hi')
        return board

    for i in range(1, 10):
        num = i
        if valid(num, row, col, board):
            board[row][col] = num
            impl = make_implications(board, row, col, impl)
            if back_track_w_impl(board, impl, row, col):
                print('hi')
                return board
            delete_implications(board, impl)
            impl = []
            board[row][col] = 0
    return False


if __name__ == '__main__':
    # board = [' ' for x in range(80)]
    start_time = time.time()
    brd_uper_duper_hard = [
        [0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 8, 0, 0, 0, 7, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 5, 0, 0],
        [0, 7, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 4, 0],
        [0, 0, 5, 0, 0, 0, 6, 0, 3],
        [0, 9, 0, 4, 0, 0, 0, 7, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0]]
    brd_hard = [
        [7, 0, 0, 5, 0, 1, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 6, 0, 0, 0, 8, 0, 1],
        [0, 0, 0, 2, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 8, 0, 3, 0, 0],
        [0, 0, 1, 9, 0, 3, 2, 0, 0],
        [4, 2, 0, 0, 0, 0, 0, 6, 9],
        [8, 0, 0, 0, 7, 0, 0, 0, 2],
        [0, 0, 9, 0, 0, 0, 4, 0, 0]]

    brd = [
        [2, 3, 0, 0, 5, 0, 6, 0, 9],
        [0, 9, 0, 0, 0, 2, 0, 7, 1],
        [5, 0, 0, 7, 0, 9, 0, 0, 0],
        [0, 6, 5, 0, 0, 0, 9, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 1, 0, 0, 0, 2, 6, 0],
        [0, 0, 0, 8, 0, 6, 0, 0, 5],
        [3, 7, 0, 2, 0, 0, 0, 9, 0],
        [8, 0, 2, 0, 3, 0, 0, 1, 6]]

    # printB(backTrack(0, 0, brd_hard))
    # print("Program took:", time.time() - start_time, "to run")
    #
    # start_time = time.time()
    printB(back_track_w_impl(brd_hard, []))
    print("Program took:", time.time() - start_time, "to run")

