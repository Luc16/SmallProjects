import random
import itertools
import time


class Brute:
    def __init__(self, num_cities):
        self.moves = [0]
        [self.moves.append(x) for x in range(1, num_cities)]
        self.final_list = list(itertools.permutations(self.moves[1:]))
        self.score = []

    @staticmethod
    def dist(p1, p2):
        return ((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))**0.5

    def fit(self, moves, cities):
        score = 0
        for index, move in enumerate(moves):
            if index < len(moves)-1:
                score += self.dist(cities[move], cities[moves[index+1]])
            else:
                score += self.dist(cities[move], cities[0])
        return score, moves

    def run(self, cities):
        for option in self.final_list:
            lk = list(option)
            lk.insert(0, 0)
            self.score.append(self.fit(lk, cities))
        self.score.sort()
        return self.score[0]


class Child:
    def __init__(self, num_cities, moves=None):
        if moves is None:
            moves = []
        self.moves = moves
        if not moves:
            [self.moves.append(x) for x in range(1, num_cities)]
            random.shuffle(self.moves)
        self.moves.insert(0, 0)
        self.score = 0

    @staticmethod
    def dist(p1, p2):
        return ((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))**0.5

    def fit(self, cities, scores):
        self.score = 0
        for index, move in enumerate(self.moves):
            if index < len(self.moves)-1:
                self.score += self.dist(cities[move], cities[self.moves[index+1]])
            else:
                self.score += self.dist(cities[move], cities[0])
        scores.append(1/self.score)
        # return self.score, self.moves


class Solver:
    def __init__(self, cities, num_children, tag="both"):
        self.num_children = num_children
        self.current_generation = [Child(len(cities)) for _ in range(num_children)]
        self.next_generation = []
        self.score_list = []
        self.prev_scores = []
        self.cities = cities
        self.tag = tag
        self.num_cities = len(cities)
        random.seed()
        self.keep_pct = 0.25
        self.limit = int(self.keep_pct * self.num_children)
        self.num_gens = 0

    def just_mutate(self):
        for _ in range(self.limit, self.num_children):
            chosen_child = random.choices(self.current_generation, weights=self.score_list, k=1)
            new_child = Child(self.num_cities, chosen_child[0].moves[1:])
            for i in range(random.randint(1, self.num_cities)):
                mutations = random.sample(range(1, self.num_cities), 2)
                if mutations[0] != mutations[1]:
                    temp = new_child.moves[mutations[0]]
                    new_child.moves[mutations[0]] = new_child.moves[mutations[1]]
                    new_child.moves[mutations[1]] = temp
            self.next_generation.append(new_child)

    def mutate(self):
        for _ in range(random.randint(0, self.num_children-self.limit)):
            chosen_child = random.choice(self.next_generation)
            for i in range(random.randint(1, self.num_cities)):
                mutations = random.sample(range(1, self.num_cities), 2)
                if mutations[0] != mutations[1]:
                    temp = chosen_child.moves[mutations[0]]
                    chosen_child.moves[mutations[0]] = chosen_child.moves[mutations[1]]
                    chosen_child.moves[mutations[1]] = temp

    def crossover(self):
        for _ in range(self.limit, self.num_children//2 + 1):
            chosen_children = random.choices(self.current_generation, weights=self.score_list, k=2)
            new_children = [Child(self.num_cities, child.moves[1:]) for child in chosen_children]
            for i in range(random.randint(1, self.num_cities//2)):
                gene = random.randint(1, self.num_cities-1)
                temp = new_children[0].moves[gene]
                indexes = [new_children[0].moves.index(new_children[1].moves[gene]), new_children[1].moves.index(temp)]
                new_children[0].moves[gene] = new_children[1].moves[gene]
                new_children[1].moves[gene] = temp
                temp = new_children[0].moves[indexes[0]]
                new_children[0].moves[indexes[0]] = new_children[1].moves[indexes[1]]
                new_children[1].moves[indexes[1]] = temp
            if len(self.next_generation) == self.num_children - 1:
                self.next_generation.append(new_children[0])
            elif len(self.next_generation) == self.num_children:
                continue
            else:
                [self.next_generation.append(child) for child in new_children]

    def select(self):
        self.next_generation[:self.limit] += self.current_generation[:self.limit]

    def end(self, final):
        size_scores = len(self.prev_scores)
        if size_scores > final:
            self.prev_scores = self.prev_scores[1:]
            grouped_scores = itertools.groupby(self.prev_scores)
            return next(grouped_scores, True) and not next(grouped_scores, False)
        else:
            return False

    def run(self):
        while True:
            # fit
            self.score_list = []
            for child in self.current_generation:
                child.fit(self.cities, self.score_list)
            # sort
            self.current_generation.sort(key=lambda x: x.score)
            self.score_list.sort(reverse=True)
            self.prev_scores.append(self.current_generation[0].score)
            self.num_gens += 1
            # check end
            if self.end(6):
                break
            # evolve
            self.select()
            if self.tag == "both":
                self.crossover()
                self.mutate()
            elif self.tag == "crossover":
                self.crossover()
            elif self.tag == "mutate":
                self.just_mutate()

            self.current_generation = self.next_generation
            self.next_generation = []
        return self.num_gens, self.current_generation[0].score, self.current_generation[0].moves


if __name__ == '__main__':
    dots = [[1, 2], [4, 1], [3, 5], [2, 4], [6, 2], [9, 5], [16, 11], [34, 29]]
    brute = Brute(len(dots))
    time_start = time.time()
    brute_result = brute.run(dots)
    time_end = time.time()
    print("Brute force result:", brute_result)
    print("Brute force time:", time_end-time_start)
    print()
    accuracy = 0
    time_sum = 0
    for _ in range(1000):
        time_start = time.time()
        result = Solver(dots, 6).run()
        time_end = time.time()
        time_sum += time_end-time_start
        # print(result)
        accuracy += 100 - 100*abs((brute_result[0]-result[1])/brute_result[0])
        # print("Percentage:", 100 - 100*abs((brute_result[0]-result[1])/brute_result[0]), "%")
    print("Accuracy:", accuracy/1000)
    print("Time per solve (Genetic Algorithm):", time_sum/1000)
