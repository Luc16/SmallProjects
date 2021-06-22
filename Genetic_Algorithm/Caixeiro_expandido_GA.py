import random
import itertools
import time


class Brute:
    def __init__(self, num_cities, num_routs):
        self.moves = list(range(1, num_cities))
        self.final_list = list(itertools.permutations(self.moves))
        self.num_routs = num_routs
        self.score = []

    @staticmethod
    def dist(p1, p2):
        return ((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))**0.5

    def fit(self, moves, cities, idx):
        score = 0
        prev = 0
        routs = list(idx) + [len(moves)]
        for rout in routs:
            score += self.dist(cities[0], cities[moves[prev]])
            for index, move in enumerate(moves[prev: rout-1]):
                score += self.dist(cities[move], cities[moves[prev + index + 1]])
            score += self.dist(cities[moves[rout-1]], cities[0])
            prev = rout
        return score, moves, idx

    def run(self, cities):
        best = [float('inf'), 0]
        for option in self.final_list:
            lk = list(option)
            for idx in itertools.combinations(range(1, len(lk)), self.num_routs-1):
                current = self.fit(lk, cities, idx)
                best = min(current, best, key=lambda x: x[0])
        return best


class Chromosome:
    def __init__(self, num_cities, num_routs, moves=None, routs=None):
        self.moves = moves
        self.num_routs = num_routs
        if moves is None:
            self.moves = list(range(1, num_cities))
            random.shuffle(self.moves)
        self.routs = routs
        if routs is None:
            self.routs = [random.randint(1, num_cities - num_routs)]
            [self.routs.append(random.randint(self.routs[i - 1] + 1, num_cities - num_routs + i))for i in range(1, num_routs - 1)]
            self.routs.append(len(self.moves))
        self.score = 0

    @staticmethod
    def dist(p1, p2):
        return ((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])) ** 0.5

    def fit(self, cities, scores):
        if self.score == 0:
            prev = 0
            for rout in self.routs:
                self.score += self.dist(cities[0], cities[self.moves[prev]])
                for index, move in enumerate(self.moves[prev: rout-1]):
                    self.score += self.dist(cities[move], cities[self.moves[prev + index + 1]])
                self.score += self.dist(cities[self.moves[rout-1]], cities[0])
                prev = rout
            scores.append(1 / self.score)


class Solver:
    def __init__(self, cities, num_chromosome, num_routs, tag="both", final=6):
        self.num_chromosome = num_chromosome
        self.current_generation = [Chromosome(len(cities), num_routs) for _ in range(num_chromosome)]
        self.next_generation = []
        self.score_list = []
        self.prev_scores = []
        self.cities = cities
        self.tag = tag
        self.num_cities = len(cities)
        self.final = final
        random.seed()
        self.keep_pct = 0.05
        self.limit = int(self.keep_pct * self.num_chromosome)
        self.num_gens = 0

    def just_mutate_shuffle(self):
        for _ in range(self.limit, self.num_chromosome):
            chosen_chromosome = random.choices(self.current_generation, weights=self.score_list, k=1)
            new_chromosome = Chromosome(self.num_cities, chosen_chromosome[0].moves[1:])
            rands = [random.randint(1, self.num_cities), random.randint(1, self.num_cities)]
            rands.sort()
            random.shuffle(new_chromosome.moves[rands[0]: rands[1]])
            self.next_generation.append(new_chromosome)

    def just_mutate(self):
        for _ in range(self.limit, self.num_chromosome):
            chosen_chromosome = random.choices(self.current_generation, weights=self.score_list, k=1)
            new_chromosome = Chromosome(self.num_cities, chosen_chromosome[0].moves[1:])
            for _ in range(random.randint(1, self.num_cities)):
                mutations = random.sample(range(1, self.num_cities), 2)
                if mutations[0] != mutations[1]:
                    temp = new_chromosome.moves[mutations[0]]
                    new_chromosome.moves[mutations[0]] = new_chromosome.moves[mutations[1]]
                    new_chromosome.moves[mutations[1]] = temp
            self.next_generation.append(new_chromosome)

    def mutate(self):
        for _ in range(random.randint(0, (self.num_chromosome-self.limit)//20)):
            chosen_chromosome = random.choice(self.next_generation[self.limit:])

            for _ in range(random.randint(1, self.num_cities)):
                mutations = random.sample(range(1, self.num_cities), 2)
                if mutations[0] != mutations[1]:
                    temp = chosen_chromosome.moves[mutations[0]]
                    chosen_chromosome.moves[mutations[0]] = chosen_chromosome.moves[mutations[1]]
                    chosen_chromosome.moves[mutations[1]] = temp

    def mutate_shuffle(self):
        for _ in range(random.randint(0, self.num_chromosome-self.limit)):
            chosen_chromosome = random.choice(self.next_generation)
            rands = [random.randint(1, self.num_cities), random.randint(1, self.num_cities)]
            rands.sort()
            random.shuffle(chosen_chromosome.moves[rands[0]: rands[1]])

    def crossover(self):
        for _ in range(self.limit, self.num_chromosome//2 + 1):
            chosen_chromosome = random.choices(self.current_generation, weights=self.score_list, k=2)
            new_chromosome = [Chromosome(self.num_cities, chromosome.moves[1:]) for chromosome in chosen_chromosome]
            for _ in range(random.randint(1, self.num_cities//2)):
                gene = random.randint(1, self.num_cities-1)
                temp = new_chromosome[0].moves[gene]
                indexes = [new_chromosome[0].moves.index(new_chromosome[1].moves[gene]), new_chromosome[1].moves.index(temp)]
                new_chromosome[0].moves[gene] = new_chromosome[1].moves[gene]
                new_chromosome[1].moves[gene] = temp
                temp = new_chromosome[0].moves[indexes[0]]
                new_chromosome[0].moves[indexes[0]] = new_chromosome[1].moves[indexes[1]]
                new_chromosome[1].moves[indexes[1]] = temp
            if len(self.next_generation) == self.num_chromosome - 1:
                self.next_generation.append(new_chromosome[0])
            elif len(self.next_generation) == self.num_chromosome:
                continue
            else:
                [self.next_generation.append(chromosome) for chromosome in new_chromosome]

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
            self.score_list = self.score_list[:self.limit]
            for chromosome in self.current_generation:
                chromosome.fit(self.cities, self.score_list)
            # sort
            self.current_generation.sort(key=lambda x: x.score)
            self.score_list.sort(reverse=True)
            self.prev_scores.append(self.current_generation[0].score)
            self.num_gens += 1
            # check end
            if self.end(self.final):
                break
            # evolve
            self.select()
            if self.tag == "both":
                self.crossover()
                self.mutate()
                # self.mutate_shuffle()  # -------> not Helping
            elif self.tag == "crossover":
                self.crossover()
            elif self.tag == "mutate":
                self.just_mutate()
            elif self.tag == "mut_shuffle":
                self.just_mutate_shuffle()

            self.current_generation = self.next_generation
            self.next_generation = []
        return self.num_gens, self.current_generation[0].score, self.current_generation[0].moves


def main():
    dots = [[random.randint(0, 1000), random.randint(0, 1000)] for _ in range(8)]

    brute = Brute(len(dots))
    time_start = time.time()
    brute_result = brute.run(dots)
    time_end = time.time()

    print("Brute force result:", brute_result)
    print("Brute force time:", time_end-time_start)
    print()

    NUM_CHILDREN = 500
    DIFFERENT_TESTS = 4
    FINAL = 30
    num_attempts = 100

    rounded_brute = round(brute_result[0], 6)
    gens = [0 for _ in range(DIFFERENT_TESTS)]
    accuracy = [0 for _ in range(DIFFERENT_TESTS)]
    reached_best = [0 for _ in range(DIFFERENT_TESTS)]
    times = [0 for _ in range(DIFFERENT_TESTS)]
    worst_miss = [0 for _ in range(DIFFERENT_TESTS)]
    tags = ["both",
            "crossover",
            "mutate",
            "mut_shuffle"]

    for _ in range(num_attempts):
        for i in range(DIFFERENT_TESTS):
            time_start = time.time()
            result = Solver(dots, NUM_CHILDREN, tag=tags[i], final=FINAL).run()
            time_end = time.time()
            times[i] += time_end-time_start
            gens[i] += result[0]
            error = 100*abs((brute_result[0]-result[1])/brute_result[0])
            if error > worst_miss[i]:
                worst_miss[i] = error
            accuracy[i] += 100 - error
            if round(result[1], 6) == rounded_brute:
                reached_best[i] += 100

    for i in range(DIFFERENT_TESTS):
        print("Accuracy (", tags[i], "): ", accuracy[i]/num_attempts, sep='')
        print("Reached best:", reached_best[i] / num_attempts)
        print("Worst miss:", worst_miss[i])
        print("Time per solve (Genetic Algorithm):", times[i]/num_attempts)
        print("Generations per solve (Genetic Algorithm):", gens[i] / num_attempts)
        print()


def split(main_list, split_idxs):
    arr = [main_list[0: split_idxs[0]]]
    for i in range(1, len(split_idxs)):
        arr.append(main_list[split_idxs[i-1]:split_idxs[i]])
    arr.append(main_list[split_idxs[-1]:])
    for i in range(len(arr)):
        if not arr[i]:
            del arr[i]
    return arr


def crossover(num_dots, num_routs, b, c):
    new_chromosome = [Chromosome(num_dots, num_routs, moves=chromosome.moves, routs=chromosome.routs) for chromosome in (b, c)]
    for _ in range(random.randint(1, num_dots // 2)):
        gene = random.randint(0, num_dots - 2)
        temp = new_chromosome[0].moves[gene]
        indexes = [new_chromosome[0].moves.index(new_chromosome[1].moves[gene]), new_chromosome[1].moves.index(temp)]
        new_chromosome[0].moves[gene] = new_chromosome[1].moves[gene]
        new_chromosome[1].moves[gene] = temp
        temp = new_chromosome[0].moves[indexes[0]]
        new_chromosome[0].moves[indexes[0]] = new_chromosome[1].moves[indexes[1]]
        new_chromosome[1].moves[indexes[1]] = temp
    for i in range(c.num_routs):
        old_rout1, old_rout2 = new_chromosome[0].routs[i], new_chromosome[1].routs[i]
        for chromosome in new_chromosome:
            chromosome.routs[i] = random.randint(min(old_rout1, old_rout2), max(old_rout1, old_rout2))
            while chromosome.routs[i] in chromosome.routs[:i]+new_chromosome[0].routs[i+1:]:
                chromosome.routs[i] = random.randint(min(old_rout1, old_rout2), max(old_rout1, old_rout2))
    [chromosome.routs.sort() for chromosome in new_chromosome]
    return new_chromosome


def mutate_rout(routs, num_routs, num_dots):
    idx, sign, amount = random.randint(0, num_routs-2), random.choice([-1, 1]), random.randint(1, num_dots-1)
    routs[idx] += sign*amount
    print(routs)
    if idx == 0 and 0 < routs[idx] < routs[idx+1]:
        return routs
    if not (routs[idx-1] < routs[idx] < routs[idx+1]):
        routs[idx] -= sign * amount
    return routs


def mutate(num_dots, num_routs, cromossomes):
    chosen_chromosome = random.choice(cromossomes)
    for _ in range(random.randint(0, num_dots-1)):
        mutations = random.sample(range(0, num_dots-1), 2)
        if mutations[0] != mutations[1]:
            temp = chosen_chromosome.moves[mutations[0]]
            chosen_chromosome.moves[mutations[0]] = chosen_chromosome.moves[mutations[1]]
            chosen_chromosome.moves[mutations[1]] = temp
    idx, sign, amount = random.randint(0, num_routs - 2), random.choice([-1, 1]), random.randint(1, num_dots//2)
    chosen_chromosome.routs[idx] += sign * amount
    if idx == 0 and 0 < chosen_chromosome.routs[idx] < chosen_chromosome.routs[idx + 1]:
        return
    if not (chosen_chromosome.routs[idx - 1] < chosen_chromosome.routs[idx] < chosen_chromosome.routs[idx + 1]):
        chosen_chromosome.routs[idx] -= sign * amount


def main2():
    dots = [[203, 119], [867, 817], [639, 648], [845, 52], [671, 89], [644, 410], [327, 214], [473, 125], [16, 6]]
    num_routs = 3
    # brute = Brute(len(dots), num_routs)
    # b_result = brute.run(dots)
    # print(b_result, split(b_result[1], b_result[2]))
    # for _ in range(100000):
    c = Chromosome(len(dots), num_routs)
    c.fit(dots, [])
    s = [c.score, [], [], []]
    s[1] = [m for m in c.moves]
    s[2] = [r for r in c.routs]
    s[3] = split(s[1], s[2])
    while s[2] == c.routs or s[0] < c.score:
        mutate(len(dots), num_routs, [c])
        c.score = 0
        c.fit(dots, [])
    print("Original C:", s[0], s[1], s[2], s[3])
    print("Mutated C:", c.score, c.moves, c.routs, split(c.moves, c.routs))
    # cs = crossover(len(dots), num_routs, b, c)
    # [chro.fit(dots, []) for chro in cs]
    # [print("Kid:", chro.score, chro.moves, chro.routs, split(chro.moves, chro.routs)) for chro in cs]


if __name__ == '__main__':
    main2()
