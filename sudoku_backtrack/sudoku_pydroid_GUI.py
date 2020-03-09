import pygame as pg
from pygame.locals import *
import time

pg.init()
screen = pg.display.set_mode((800, 1000))
FONT_N = pg.font.SysFont('Comic Sans MS', 24)
FONT = pg.font.SysFont('Comic Sans MS', 32)
FONT_C = pg.font.SysFont('Comic Sans MS', 50)
FONT_S = pg.font.SysFont('Comic Sans MS', 64)
FONT_E = pg.font.SysFont('Comic Sans MS', 72)
FONT_F = pg.font.SysFont('Comic Sans MS', 100)


IMAGE_NORMAL = pg.Surface((100, 32))
IMAGE_NORMAL.fill(pg.Color('dodgerblue1'))
IMAGE_HOVER = pg.Surface((100, 32))
IMAGE_HOVER.fill(pg.Color('lightskyblue'))
IMAGE_DOWN = pg.Surface((100, 32))
IMAGE_DOWN.fill(pg.Color('aquamarine1'))


class Button(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,
                         font=FONT, text='', text_color=(0, 0, 0),
                         image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                         image_down=IMAGE_DOWN):
        super().__init__()
        self.image_normal = pg.transform.scale(image_normal, (width, height))
        self.image_hover = pg.transform.scale(image_hover, (width, height))
        self.image_down = pg.transform.scale(image_down, (width, height))

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))

        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)

        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        self.font = font
        self.callback = callback
        self.button_down = False

    def handle_event(self, event, board, fixed):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
                if self.rect.collidepoint(event.pos) and self.button_down:
                    self.callback(board, fixed)
        elif event.type == pg.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal
                self.button_down = False


class BoardPiece(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, callback, callout,
                 font=FONT, text='', text_color=(0, 0, 0),
                 image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                 image_down=IMAGE_DOWN):
        super().__init__()
        # Scale the images to the desired size (doesn't modify the originals).
        self.image_normal = pg.transform.scale(image_normal, (width, height))
        self.image_hover = pg.transform.scale(image_hover, (width, height))
        self.image_down = pg.transform.scale(image_down, (width, height))

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))

        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)

        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        self.font = font
        self.callback = callback
        self.callout = callout
        self.button_down = False
        self.close = False

    def handle_event(self, event, index):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
                if self.rect.collidepoint(event.pos) and self.button_down:
                    self.callback(index)
        elif event.type == pg.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided and not self.close:
                self.image = self.image_normal
                if self.button_down:
                    self.callout(index)
                self.button_down = False

    def rol_col_sqr(self):
        self.close = True
        self.image = self.image_hover

    def away(self):
        self.close = False
        self.image = self.image_normal

    def change_text(self, text, center):
        image_pos = self.image.get_rect().center if center else self.image.get_rect().topright
        if center:
            text_surf = FONT_C.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=image_pos)
        else:
            text_surf = FONT.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(topright=image_pos)
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)


class Game:

    def __init__(self, screen):
        self.entered = False
        self.end = False
        self.error = 0
        self.errorText = ['Errors: '+str(self.error), 'out of 5']
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = screen
        self.all_sprites = pg.sprite.Group()
        self.text = ''
        self.nums = []
        self.board = []
        self.board_pos = []
        self.board_txt = [['', False] for i in range(81)]
        self.board_a = [
            2, 3, 7, 1, 5, 8, 6, 4, 9,
            6, 9, 8, 3, 4, 2, 5, 7, 1,
            5, 1, 4, 7, 6, 9, 8, 3, 2,
            7, 6, 5, 4, 2, 1, 9, 8, 3,
            9, 2, 3, 6, 8, 7, 1, 5, 4,
            4, 8, 1, 5, 9, 3, 2, 6, 7,
            1, 4, 9, 8, 7, 6, 3, 2, 5,
            3, 7, 6, 2, 1, 5, 4, 9, 8,
            8, 5, 2, 9, 3, 4, 7, 1, 6]
        self.board_BT = [
            2, 3, 0, 0, 5, 0, 6, 0, 9,
            0, 9, 0, 0, 0, 2, 0, 7, 1,
            5, 0, 0, 7, 0, 9, 0, 0, 0,
            0, 6, 5, 0, 0, 0, 9, 0, 0,
            9, 0, 0, 0, 0, 0, 0, 0, 4,
            0, 0, 1, 0, 0, 0, 2, 6, 0,
            0, 0, 0, 8, 0, 6, 0, 0, 5,
            3, 7, 0, 2, 0, 0, 0, 9, 0,
            8, 0, 2, 0, 3, 0, 0, 1, 6]
        self.board_BTI = [
            [2, 3, 0, 0, 5, 0, 6, 0, 9],
            [0, 9, 0, 0, 0, 2, 0, 7, 1],
            [5, 0, 0, 7, 0, 9, 0, 0, 0],
            [0, 6, 5, 0, 0, 0, 9, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 1, 0, 0, 0, 2, 6, 0],
            [0, 0, 0, 8, 0, 6, 0, 0, 5],
            [3, 7, 0, 2, 0, 0, 0, 9, 0],
            [8, 0, 2, 0, 3, 0, 0, 1, 6]]
        self.fixed = []
        self.listenToNum = False
        self.index = None
        self.win = False
        self.size = 2

        b = 4
        a = 40
        for x in range(81):
            if (x / 9) % 3 == 0:
                b += 4
            if x % 3 == 0:
                a += 4
            if x % 9 == 0:
                a = 40
            self.board_pos.append([(x % 9) * 50 + a, (x // 9) * 66 + b])
            self.board.append(BoardPiece(self.board_pos[x][0]*self.size, self.board_pos[x][1]*self.size,
                                         48*self.size, 64*self.size, self.press_button,
                                         self.button_out, FONT, self.text, (255, 255, 255),
                                         IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN))
            self.all_sprites.add(self.board[x])
        self.BT_button = Button(250*self.size, 838*self.size, 250*self.size, 100*self.size, self.back_track,
                                FONT, text='Back Track', text_color=(0, 0, 0),
                                image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                                image_down=IMAGE_DOWN)
        self.all_sprites.add(self.BT_button)
        self.BTI_button = Button(250*self.size, 725*self.size, 250*self.size, 100*self.size, self.back_track_w_impl,
                                FONT, text='Back Track w/ impl', text_color=(0, 0, 0),
                                image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                                image_down=IMAGE_DOWN)
        self.all_sprites.add(self.BTI_button)
        self.enter_button = Button(380 * self.size, 615 * self.size, 120 * self.size, 100 * self.size,
                                 self.enter_but,
                                 FONT_N, text='ENTER', text_color=(0, 0, 0),
                                 image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                                 image_down=IMAGE_DOWN)
        self.all_sprites.add(self.enter_button)
        x = 0
        for i in range(9):
            self.nums.append(Button(x * self.size, 625 * self.size, 37 * self.size, 80 * self.size,
                                       self.num_but,
                                       FONT_N, text=str(i+1), text_color=(0, 0, 0),
                                       image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                                       image_down=IMAGE_DOWN))
            self.all_sprites.add(self.nums[i])
            x += 42

    def quit_game(self):
        self.done = True

    @staticmethod
    def identify_square(mult, idx):
        a = int(mult / 3) * 27 + int((idx - 9 * mult) / 3) * 3
        return [a, a + 1, a + 2, a + 9, a + 10, a + 11,
                a + 18, a + 19, a + 20]

    def press_button(self, idx):
        mult = idx//9
        square = self.identify_square(mult, idx)
        for j in range(9):
            if (idx - (9 * mult) + 9 * j) != idx:
                self.board[idx - (9 * mult) + 9 * j].rol_col_sqr()
            if (j + (9 * mult)) != idx:
                self.board[j + (9 * mult)].rol_col_sqr()
            if square[j] != idx:
                self.board[square[j]].rol_col_sqr()

        self.listenToNum = True
        self.index = idx

    def button_out(self, idx):
        mult = idx // 9
        square = self.identify_square(mult, idx)
        for j in range(9):
            if (idx - (9 * mult) + 9 * j) != idx:
                self.board[idx - (9 * mult) + 9 * j].away()
            if (j + (9 * mult)) != idx:
                self.board[j + (9 * mult)].away()
            if square[j] != idx:
                self.board[square[j]].away()
        self.listenToNum = False

    def run(self):
        for i in range(81):
            s = str(self.board_BT[i])
            if s == '0':
                s = ''
            else:
                self.board_txt[i][1] = True
                self.fixed.append(i)
            self.board_txt[i][0] = s
            self.board[i].change_text(self.board_txt[i][0], True)
        while not self.done:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if not self.end:
                self.enter_button.handle_event(event, [], [])
                self.BT_button.handle_event(event, self.board_BT, self.fixed)
                self.BTI_button.handle_event(event, self.board_BTI, [])
                for i in range(len(self.nums)):
                    self.nums[i].handle_event(event, [str(i+1)], [])
                for i in range(len(self.board)):
                    self.board[i].handle_event(event, i)
                if self.listenToNum:
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            self.erase(self.index)
                            self.board[self.index].change_text(self.board_txt[self.index][0], True)
                            self.board_txt[self.index][1] = True
                            self.entered = True
                            if self.board_txt[self.index][0] != str(self.board_a[self.index]):
                                self.error += 1
                                self.errorText[0] = 'Errors: ' + str(self.error)
                                self.erase(self.index)
                            self.button_out(self.index)
                        if not self.board_txt[self.index][1]:
                            self.entered = False
                            self.erase(self.index)
                            if event.key == K_1:
                                self.board_txt[self.index][0] = '1'
                                self.board[self.index].change_text(self.board_txt[self.index][0], False)
                            if event.key == K_2:
                                self.board_txt[self.index][0] = '2'
                                self.board[self.index].change_text(self.board_txt[self.index][0], False)
                            if event.key == K_3:
                                self.board_txt[self.index][0] = '3'
                                self.board[self.index].change_text(self.board_txt[self.index][0], False)
                            if event.key == K_4:
                                self.board_txt[self.index][0] = '4'
                                self.board[self.index].change_text(self.board_txt[self.index][0], False)
                            if event.key == K_5:
                                self.board_txt[self.index][0] = '5'
                                self.board[self.index].change_text(self.board_txt[self.index][0], False)
                            if event.key == K_6:
                                self.board_txt[self.index][0] = '6'
                                self.board[self.index].change_text(self.board_txt[self.index][0], False)
                            if event.key == K_7:
                                self.board_txt[self.index][0] = '7'
                                self.board[self.index].change_text(self.board_txt[self.index][0], False)
                            if event.key == K_8:
                                self.board_txt[self.index][0] = '8'
                                self.board[self.index].change_text(self.board_txt[self.index][0], False)
                            if event.key == K_9:
                                self.board_txt[self.index][0] = '9'
                                self.board[self.index].change_text(self.board_txt[self.index][0], False)
                            self.button_out(self.index)

    def erase(self, idx):
        self.board[idx] = BoardPiece(self.board_pos[idx][0]*self.size, self.board_pos[idx][1]*self.size, 48*self.size, 64*self.size, self.press_button,
                                     self.button_out, FONT, self.text, (255, 255, 255),
                                     IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN)
        self.board_txt[idx][1] = False
        self.all_sprites.add(self.board[idx])

    def enter_but(self, a1, a2):
        self.erase(self.index)
        self.board[self.index].change_text(self.board_txt[self.index][0], True)
        self.board_txt[self.index][1] = True
        self.entered = True
        if self.board_txt[self.index][0] != str(self.board_a[self.index]):
            self.error += 1
            self.errorText[0] = 'Errors: ' + str(self.error)
            self.erase(self.index)
        self.button_out(self.index)

    def num_but(self, a1, a2):
        if not self.board_txt[self.index][1]:
            self.entered = False
            self.erase(self.index)
            self.board_txt[self.index][0] = a1[0]
            self.board[self.index].change_text(self.board_txt[self.index][0], False)
            self.button_out(self.index)

    def error_text(self):
        image_pos_1 = (125*self.size, 775*self.size)
        text_surf_e = FONT_E.render(self.errorText[0], True, (255, 0, 0))
        text_rect_e = text_surf_e.get_rect(center=image_pos_1)
        self.screen.blit(text_surf_e, text_rect_e)
        image_pos_2 = (125*self.size, 811*self.size)
        text_surf_oo5 = FONT_E.render(self.errorText[1], True, (255, 0, 0))
        text_rect_oo5 = text_surf_oo5.get_rect(center=image_pos_2)
        self.screen.blit(text_surf_oo5, text_rect_oo5)

    def run_logic(self):
        self.all_sprites.update(self.dt)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.all_sprites.draw(self.screen)
        self.error_text()
        if self.error == 5:
            self.lose()
        if self.entered:
            for k in range(len(self.board_txt)):
                if self.board_txt[k][0] == '':
                    break
                if k == 80:
                    self.win_f()
        if self.win:
            self.win_f()
        pg.display.flip()

    def lose(self):
        image_pos_1 = (580, 650)
        text_surf_l = FONT_F.render('You Lose', True, (255, 0, 0))
        text_rect_l = text_surf_l.get_rect(center=image_pos_1)
        self.screen.blit(text_surf_l, text_rect_l)
        self.end = True

    def win_f(self):
        image_pos_1 = (580, 650)
        text_surf_f = FONT_F.render('You Win!!', True, (255, 0, 0))
        text_rect_f = text_surf_f.get_rect(center=image_pos_1)
        self.screen.blit(text_surf_f, text_rect_f)
        self.end = True

    def valid_i(self, nt, idx, board):
        mult = int(idx / 9)
        square = self.identify_square(mult, idx)
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

    def back_track(self, board, fixed):
        self.end = True
        i = 0
        while i < len(board):
            if i not in fixed:
                if board[i] != 0:
                    self.erase(i)
                board[i] = self.valid_i(board[i], i, board)
                if board[i] != 0:
                    self.board[i].change_text(str(board[i]), True)
                self.handle_events()
                self.draw()
                time.sleep(0.1)
                if board[i] == 0:
                    while True:
                        if i == 0:
                            self.lose()
                            return 'Impossible'
                        if i not in fixed:
                            board[i] = 0
                            self.erase(i)
                        if ((i - 1) not in fixed) and self.valid_i(board[i - 1], i - 1, board) != 0:
                            i -= 2
                            break
                        else:
                            i -= 1
            i += 1
        self.win = True
        return board

    def identify_square_r(self, row, col):
        a = int(row / 3) * 3
        b = int(col / 3) * 3
        return [[a, b], [a, b + 1], [a, b + 2], [a + 1, b], [a + 1, b + 1], [a + 1, b + 2],
                [a + 2, b], [a + 2, b + 1], [a + 2, b + 2]]

    def valid(self, num, row, col, board):
        square = self.identify_square_r(row, col)
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

    def make_implications(self, board, row, col, implicated):
        can_implicate = True
        while can_implicate:
            prev_board = board
            while row < len(board):
                nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                if board[row][col] == 0:
                    square = self.identify_square_r(row, col)
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
                    self.board[row*9 + col].change_text(str(board[row][col]), True)
                    self.handle_events()
                    self.draw()
                    time.sleep(0.1)
                col += 1
                if col == len(board[row]):
                    col = 0
                    row += 1
            if board == prev_board:
                return implicated

    def delete_implications(self, board, implicated):
        deleted = []
        if len(implicated) > 0:
            for i in implicated:
                deleted.append([i[0], i[1]])
                board[i[0]][i[1]] = 0
                self.erase(i[0]*9 + i[1])
            deleted.sort()
        return deleted

    def next(self, board):
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    return [row, col]

    def back_track_w_impl(self, board, impl, row=0, col=0):
        self.end = True
        nxt = self.next(board)
        if nxt is None:
            self.win = True
            return True
        row = nxt[0]
        col = nxt[1]

        if row == -1:
            return board

        for i in range(1, 10):
            num = i
            if self.valid(num, row, col, board):
                board[row][col] = num
                self.board[row*9 + col].change_text(str(num), True)
                self.handle_events()
                self.draw()
                time.sleep(0.1)
                impl = self.make_implications(board, row, col, impl)
                if self.back_track_w_impl(board, impl, row, col):
                    return board
                self.delete_implications(board, impl)
                impl = []
                board[row][col] = 0
                self.erase((9*row+col))
        return False


if __name__ == '__main__':
    pg.init()
    Game(screen).run()
    pg.quit()
