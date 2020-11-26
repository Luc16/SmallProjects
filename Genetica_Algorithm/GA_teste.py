import random
import time


def print_board(bd):
    for k in bd:
        print(k)
    print()


class Child:
    def __init__(self, bd):
        self.moves = [random.randint(1, 3) for x in range(20)]
        self.pos = [9, 6]
        self.mv_count = 0
        self.score = 0
        self.live = True
        self.board = bd
        self.win = False

    @staticmethod
    def fitness(self):
        self.score = 1000/(((self.pos[1]-5)**2 + (self.pos[0])**2)**.5)

    def move(self):
        if self.live:
            self.board[self.pos[0]][self.pos[1]] = 8
            for direction in self.moves:
                self.board[self.pos[0]][self.pos[1]] = 0
                if direction == 1:
                    self.mv_count += 1
                    if self.pos[0]-1 < 0 or self.board[self.pos[0]-1][self.pos[1]] == 1:
                        self.live = False
                        break
                    else:
                        self.pos[0] -= 1
                elif direction == 2:
                    self.mv_count += 1
                    if self.pos[1] - 1 < 0 or self.board[self.pos[0]][self.pos[1]-1] == 1:
                        self.live = False
                        break
                    else:
                        self.pos[1] -= 1
                elif direction == 3:
                    self.mv_count += 1
                    if self.pos[1] + 1 >= len(self.board[0]) or self.board[self.pos[0]][self.pos[1]+1] == 1:
                        self.live = False
                        break
                    else:
                        self.pos[1] += 1
                elif self.mv_count >= 20:
                    self.live = False
                elif self.pos[0] == 0 and self.pos[1] == 5:
                    self.live = False
                    self.win = True
                self.board[self.pos[0]][self.pos[1]] = 8
                # print("Moved", direction)
                # print_board(self.board)
            self.board[self.pos[0]][self.pos[1]] = 8
            self.fitness(self)


class Game:
    def __init__(self):
        self.size = 10
        self.population = 10
        self.children = []
        self.board = [[0 for y in range(self.size)] for x in range(self.size)]
        self.board[0][5] = 2
        for i in range(6):
            self.board[3][i] = 1
            self.board[7][self.size - i - 1] = 1

    def mutate(self):
        return 0

    def crossover(self):
        return 0

    def select(self):
        return 0

    def play(self):
        for i in range(self.population):
            self.children.append(Child(self.board))
            # print("CHILD NUMBER:", i)
            self.children[i].move()
            # print(children[i].score)
        print_board(self.board)
        self.children.sort(key=lambda x: x.score, reverse=True)
        for i in range(self.population):
            print(self.children[i].score)
            print_board(self.children[i].board)


if __name__ == '__main__':
    gm = Game()
    gm.play()
