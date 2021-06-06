import pygame
import random

"""
10 x 20 размер игровой сетки
Фигуры: S, Z, I, O, J, L, T
Представленны по порядку 0 - 6
"""

pygame.font.init()
pygame.init()

# Общие настройки
s_width = 800
s_height = 700
play_width = 300  # 300 // 10 = 30 ширина на блок
play_height = 600  # 600 // 20 = 20 высота на блок
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
background = pygame.image.load('back.jpg').convert()
# Возможные повороты фигур

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
pygame.mixer.music.load('music.mp3')
sound_fall = pygame.mixer.Sound('fall.mp3')
sound_swipe = pygame.mixer.Sound('swipe.mp3')
sound_fall.set_volume(0.3)
sound_swipe.set_volume(0.3)

# Номер 0 - 6 представления фигур

# Описание кнопки


class Button:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.inact_color = (90, 90, 90)
        self.act_color = (160, 160, 160)

    def draw_b(self, x, y, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(win, self.act_color, (x, y, self.w, self.h))

            if click[0] == 1:
                action()
                if action is None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(win, self.inact_color, (x, y, self.w, self.h))


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # Номер поворота 0-3


def print_text(text, size, color, x, y):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    win.blit(label, (x, y))


# Игровая сетка


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30),
                         (sx + play_width, sy + i * 30))  # Горизонтальные линии
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))  # Вертикальные линии


def clear_rows(grid, locked):
    # Нужно посмотреть, очищена ли строка, сдвиньте каждую вторую строку выше вниз на одну
    global score
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # Добавление позиций для удаления из заблокированных
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        score = score + 1
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:  # Тут съедает нижнюю линию
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


# Описание появления новой фигуры


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - 30))


def fs_reset():
    global fs
    fs = 0.27


def fs_minus():
    global fs
    fs = 0.40


def fs_plus():
    global fs
    fs = 0.15


def sound_off():
    pygame.mixer.music.set_volume(0)


def sound_on():
    pygame.mixer.music.set_volume(0.5)


def draw_window(surface):
    surface.blit(background, (0, 0))
    # Название Тетрис
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    # Рисование сетки и окна
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    sound_button = Button(80, 20)
    sound_button.draw_b(8, 510, action=fs_plus)
    print_text('FS +', 20, (255, 255, 255), 35, 515)

    sound_button = Button(80, 20)
    sound_button.draw_b(8, 540, action=fs_reset)
    print_text('FS res', 20, (255, 255, 255), 25, 545)

    sound_button = Button(80, 20)
    sound_button.draw_b(8, 570, action=fs_minus)
    print_text('FS -', 20, (255, 255, 255), 35, 575)

    sound_button = Button(80, 20)
    sound_button.draw_b(8, 636, action=sound_on)
    print_text('Music on', 20, (255, 255, 255), 12, 640)

    sound_button = Button(80, 20)
    sound_button.draw_b(8, 666, action=sound_off)
    print_text('Music off', 20, (255, 255, 255), 12, 670)


def main():
    global grid
    global score
    global fs
    score = 0

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    fs = 0.27

    while run:

        fall_speed = fs

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Падение фигуры
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                sound_swipe.play()
                if event.key == pygame.K_LEFT:
                    sound_swipe.play()
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    sound_swipe.play()
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    sound_swipe.play()
                    # Поворот фигуры
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    sound_swipe.play()
                    # Перемещение фигуры вниз
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        # Добавление фигуры в сетку для отрисовки
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # Если фигура коснулась нижнего края
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            sound_fall.play()

            # Вызов проверки надо ли очистить линию
            clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        print_text('Yore score:' + str(score), 30, (255, 255, 255), 5, 5)
        pygame.display.update()

        # Проверка проигрыша
        if check_lost(locked_positions):
            run = False

    pygame.mixer.music.stop()
    draw_text("You Lost", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2500)


def main_menu():
    run = True
    while run:
        win.blit(background, (0, 0))
        start_button = Button(500, 50)
        start_button.draw_b(150, 300, action=main)
        print_text('Play', 50, (255, 255, 255), 355, 305)
        start_button = Button(500, 50)
        start_button.draw_b(150, 400, action=quit)
        print_text('Quit', 50, (255, 255, 255), 355, 405)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            else:
                None


main_menu()  # Выход в главное меню -> начало новой игры
