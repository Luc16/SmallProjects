
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.traversable = True
        self.score = 0

    def calculate_score(self, point):
        diff_y = abs(self.x - point[0])
        diff_x = abs(self.y - point[1])
        diagonal = diff_x - diff_y
        if diagonal == 0:
            return diff_x*(2**0.5)
        elif diagonal < 0:
            return diff_x*(2**0.5) - diagonal
        else:
            return diff_y*(2**0.5) + diagonal

    def final_score(self, start, end):
        self.score = self.calculate_score(start)+self.calculate_score(end)


class Solver:

    def __init__(self, grid_size, end_pos, start_pos=(0, 0)):
        self.end_pos = end_pos
        self.grid = [[Node(i, j) for i in range(grid_size[0])] for j in range(grid_size[1])]
        self.near = [self.grid[start_pos[0]][start_pos[1]]]
        self.evaluated = []
        self.grid[start_pos[0]][start_pos[1]].score = 's'
        self.grid[end_pos[0]][end_pos[1]].score = 'e'

    def path_finder(self,):
        best_score = 0
        best_idx = 0
        neighbors = []
        while True:
            current = self.near[best_idx]
            del self.near[best_idx]
            self.evaluated.append(current)

            if current.x == self.end_pos[0] and current.y == self.end_pos[1]:
                return

            self.generate_neighbors(current, neighbors)
            for neighbor in neighbors:
                if neighbor in self.evaluated or not neighbor.traversable:
                    continue
                neighbor.final_score()

    def generate_neighbors(self, node, array):
        for j in range(node.x - 1, node.x + 2):
            for i in range(node.y - 1, node.y + 2):
                if 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0]):
                    array += [self.grid[i][j]]

    def print_grid(self):
        for line in self.grid:
            for element in line:
                print(element.score, end=' ')
            print()


if __name__ == '__main__':
    Solver([10, 10], [9, 9]).print_grid()
    # Solver([10, 10], [9, 9]).path_finder()

