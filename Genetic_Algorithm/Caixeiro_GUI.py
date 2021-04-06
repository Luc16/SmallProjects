import pygame as pg
import random
import itertools
import time


class Brute:
    def __init__(self):
        self.moves = []
        self.final_list = []
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
        self.moves = [x for x in range(1, len(cities))]
        self.final_list = list(itertools.permutations(self.moves))
        lk = list(self.final_list[0])
        lk.insert(0, 0)
        best = self.fit(lk, cities)
        for option in self.final_list[1:]:
            lk = list(option)
            lk.insert(0, 0)
            current = self.fit(lk, cities)
            if current[0] < best[0]:
                best = current
        return best


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
    def __init__(self, cities, num_children, tag="both", final=6):
        self.num_children = num_children
        self.current_generation = [Child(len(cities)) for _ in range(num_children)]
        self.next_generation = []
        self.score_list = []
        self.prev_scores = []
        self.cities = cities
        self.tag = tag
        self.num_cities = len(cities)
        self.final = final
        random.seed()
        self.keep_pct = 0.1
        self.limit = int(self.keep_pct * self.num_children)
        self.num_gens = 0
        # self.best_in_gen = []

    def just_mutate_shuffle(self):
        for _ in range(self.limit, self.num_children):
            chosen_child = random.choices(self.current_generation, weights=self.score_list, k=1)
            new_child = Child(self.num_cities, chosen_child[0].moves[1:])
            rands = [random.randint(1, self.num_cities), random.randint(1, self.num_cities)]
            rands.sort()
            random.shuffle(new_child.moves[rands[0]: rands[1]])
            self.next_generation.append(new_child)

    def just_mutate(self):
        for _ in range(self.limit, self.num_children):
            chosen_child = random.choices(self.current_generation, weights=self.score_list, k=1)
            new_child = Child(self.num_cities, chosen_child[0].moves[1:])
            for _ in range(random.randint(1, self.num_cities)):
                mutations = random.sample(range(1, self.num_cities), 2)
                if mutations[0] != mutations[1]:
                    temp = new_child.moves[mutations[0]]
                    new_child.moves[mutations[0]] = new_child.moves[mutations[1]]
                    new_child.moves[mutations[1]] = temp
            self.next_generation.append(new_child)

    def mutate(self):
        for _ in range(random.randint(0, (self.num_children-self.limit)//20)):
            chosen_child = random.choice(self.next_generation)
            for _ in range(random.randint(1, self.num_cities)):
                mutations = random.sample(range(1, self.num_cities), 2)
                if mutations[0] != mutations[1]:
                    temp = chosen_child.moves[mutations[0]]
                    chosen_child.moves[mutations[0]] = chosen_child.moves[mutations[1]]
                    chosen_child.moves[mutations[1]] = temp

    def mutate_shuffle(self):
        for _ in range(random.randint(0, self.num_children-self.limit)):
            chosen_child = random.choice(self.next_generation)
            rands = [random.randint(1, self.num_cities), random.randint(1, self.num_cities)]
            rands.sort()
            random.shuffle(chosen_child.moves[rands[0]: rands[1]])

    def crossover(self):
        for _ in range(self.limit, self.num_children//2 + 1):
            chosen_children = random.choices(self.current_generation, weights=self.score_list, k=2)
            new_children = [Child(self.num_cities, child.moves[1:]) for child in chosen_children]
            for _ in range(random.randint(1, self.num_cities//2)):
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
            # self.best_in_gen.append(self.current_generation[0])
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
        return self.num_gens, self.current_generation[0].score, self.current_generation[0].moves  # , self.best_in_gen


class GUI:
    def __init__(self):
        pg.init()
        self.dots = []
        self.font = pg.font.SysFont('Arial', 32)
        self.num_children = 150
        self.final = 20
        self.num_attempts = 1
        self.texts = []
        self.rectangles = []
        self.colors = []
        self.activated = []
        for x in range(3):
            self.texts.append("")
            self.rectangles.append(pg.Rect(270, 400 + 100*x, 140, 32))
            self.colors.append(pg.Color('gray15'))
            self.activated.append(False)
        self.screen_width = 1000
        self.screen_height = 1000
        self.screen = pg.display.set_mode([self.screen_width, self.screen_height])
        self.text_box = pg.Surface((500, 300))
        self.running = True
        self.run_text_box = False
        self.ran_brute = False
        self.brute = Brute()
        self.brute_result = []
        self.result = []
        self.time = ""

    def draw_path_brute(self, cities):
        if len(cities) < len(self.dots) + 1:
            cities.append(0)
        for idx, num in enumerate(cities[:-1]):
            pg.draw.line(self.screen, (0, 0, 255),
                         (self.dots[num][0] + 5, self.dots[num][1] + 5),
                         (self.dots[cities[idx+1]][0] + 5, self.dots[cities[idx+1]][1] + 5), 2)

    def draw_path(self, cities):
        if len(cities) < len(self.dots) + 1:
            cities.append(0)
        for idx, num in enumerate(cities[:-1]):
            pg.draw.line(self.screen, (255, 0, 0), self.dots[num], self.dots[cities[idx + 1]], 2)

    def draw_text_box(self):
        self.text_box.fill((20, 20, 20))
        self.screen.blit(self.text_box, (250, 350))
        self.screen.blit(self.font.render("Numero de crianças:", True, (255, 255, 255)), (260, 360))
        self.screen.blit(self.font.render("Geraçoes para o fim:", True, (255, 255, 255)), (260, 460))
        self.screen.blit(self.font.render("Tentativas por resolução:", True, (255, 255, 255)), (260, 560))
        for i in range(3):
            text = self.font.render(self.texts[i], True, (255, 255, 255))
            self.rectangles[i].w = max(text.get_width(), 140)
            pg.draw.rect(self.screen, self.colors[i], self.rectangles[i], 2)
            self.screen.blit(text,
                             (self.rectangles[i].x + 2, self.rectangles[i].y + 2))

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
        pg.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.run_text_box:
                    for i in range(3):
                        if self.rectangles[i].collidepoint(event.pos):
                            self.colors[i] = pg.Color('lightskyblue3')
                            self.activated[i] = True
                        else:
                            self.activated[i] = False
                            self.colors[i] = pg.Color('gray15')
                else:
                    self.dots.append(event.pos)
                    self.ran_brute = False
                    self.result = []
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if self.run_text_box:
                        try:
                            self.num_children = int(self.texts[0])
                            self.final = int(self.texts[1])
                            self.num_attempts = int(self.texts[2])
                        except ValueError:
                            pass
                        self.run_text_box = False
                        if not self.ran_brute:
                            self.ran_brute = True
                            self.brute_result = self.brute.run(self.dots)
                        s_time = time.time()
                        self.result = Solver(self.dots, self.num_children, final=self.final).run()
                        best = self.result[1]
                        for _ in range(self.num_attempts-1):
                            result = Solver(self.dots, self.num_children, final=self.final).run()
                            if result[1] < best:
                                best = result[1]
                                self.result = result
                        e_time = time.time()
                        self.time = str(round(1000000*((e_time-s_time)/self.num_attempts), 1))
                    else:
                        self.result = []
                        for idx, _ in enumerate(self.texts):
                            self.texts[idx] = ""
                            self.colors[idx] = pg.Color('gray15')
                            self.activated[idx] = False
                        self.run_text_box = True

                elif self.run_text_box:
                    for idx, is_activated in enumerate(self.activated):
                        if is_activated:
                            if event.key == pg.K_BACKSPACE:
                                self.texts[idx] = self.texts[idx][:-1]
                            else:
                                self.texts[idx] += event.unicode

    def draw(self):
        self.screen.fill((200, 200, 200))
        if self.dots:
            pg.draw.circle(self.screen, (0, 150, 0), self.dots[0], 10)
            for dot in self.dots[1:]:
                pg.draw.circle(self.screen, (0, 0, 0), dot, 10)
        if self.ran_brute:
            self.screen.blit(self.font.render("Força bruta: " + str(self.brute_result[0]), True, (0, 0, 255)), (20, 10))
            self.draw_path_brute(self.brute_result[1])
        if self.result:
            self.screen.blit(self.font.render("Algoritmo: " + str(self.result[1]), True, (255, 0, 0)), (20, 50))
            self.draw_path(self.result[2])
            self.screen.blit(self.font.render("Acerto: " +
                                              str(round(100 - 100 *
                                                        abs((self.brute_result[0] - self.result[1]) / self.brute_result[0]),
                                                        2)) + " %", True, (0, 0, 0)), (750, 950))
        if self.run_text_box:
            self.draw_text_box()
        self.screen.blit(self.font.render("Tempo por resolução: "+self.time+" us", True, (0, 0, 0)), (20, 950))
        pg.display.flip()


if __name__ == '__main__':
    GUI().run()
