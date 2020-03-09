import time


def identify_square(mult, idx):
    a = int(mult / 3) * 27 + int((idx - 9 * mult) / 3) * 3
    return [a, a + 1, a + 2, a + 9, a + 10, a + 11,
            a + 18, a + 19, a + 20]


def valid(nt, idx, board):
    mult = idx // 9
    square = identify_square(mult, idx)
    if nt == 0:
        nt = 1
    for j in range(nt, 10):
        a = False
        for k in range(9):
            if j == board[idx - (9 * mult) + 9 * k]:
                a = True
                break
            if j == board[k + (9 * mult)]:
                a = True
                break
            if j == board[square[k]]:
                a = True
                break
        if not a:
            return j
    return 0


def backTrack(board):
    fixed = []
    for i in range(len(board)):
        if board[i] != 0:
            fixed.append(i)
    i = 0
    while i < len(board):
        if i not in fixed:
            board[i] = valid(board[i], i, board)
            if board[i] == 0:
                while True:
                    if i == 0:
                        return 'Impossible'
                    if i not in fixed:
                        board[i] = 0
                    if ((i-1) not in fixed) and valid(board[i - 1], i - 1, board) != 0:
                        i -= 2
                        break
                    else:
                        i -= 1
        i += 1
        # print(i)
        # printB(board)
    return board


def printB(board):
    print("Board:")
    print(board[:9])
    print(board[9:18])
    print(board[18:27])
    print(board[27:36])
    print(board[36:45])
    print(board[45:54])
    print(board[54:63])
    print(board[63:72])
    print(board[72:81])
    print()


if __name__ == '__main__':
    start_time = time.time()
    brd_uper_duper_hard = [
        0, 0, 0, 0, 0, 0, 2, 0, 0,
        0, 8, 0, 0, 0, 7, 0, 9, 0,
        6, 0, 2, 0, 0, 0, 5, 0, 0,
        0, 7, 0, 0, 6, 0, 0, 0, 0,
        0, 0, 0, 9, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 2, 0, 0, 4, 0,
        0, 0, 5, 0, 0, 0, 6, 0, 3,
        0, 9, 0, 4, 0, 0, 0, 7, 0,
        0, 0, 6, 0, 0, 0, 0, 0, 0]
    brd_hard = [
        7, 0, 0, 5, 0, 1, 0, 0, 4,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        5, 0, 6, 0, 0, 0, 8, 0, 1,
        0, 0, 0, 2, 0, 7, 0, 0, 0,
        0, 0, 4, 0, 8, 0, 3, 0, 0,
        0, 0, 1, 9, 0, 3, 2, 0, 0,
        4, 2, 0, 0, 0, 0, 0, 6, 9,
        8, 0, 0, 0, 7, 0, 0, 0, 2,
        0, 0, 9, 0, 0, 0, 4, 0, 0]

    brd = [
        2, 3, 0, 0, 5, 0, 6, 0, 9,
        0, 9, 0, 0, 0, 2, 0, 7, 1,
        5, 0, 0, 7, 0, 9, 0, 0, 0,
        0, 6, 5, 0, 0, 0, 9, 0, 0,
        9, 0, 0, 0, 0, 0, 0, 0, 4,
        0, 0, 1, 0, 0, 0, 2, 6, 0,
        0, 0, 0, 8, 0, 6, 0, 0, 5,
        3, 7, 0, 2, 0, 0, 0, 9, 0,
        8, 0, 2, 0, 3, 0, 0, 1, 6]

    # print(backTrack(brd))
    # printB(backTrack(brd))
    # print("Program took:", time.time() - start_time, "to run")



