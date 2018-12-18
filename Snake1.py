import random
from tkinter import *

# Ширина экрана
WIDTH = 800
# Высота экрана
HEIGHT = 600
# Размер сегмента змейки
SEG_SIZE = 20


def create_apple(canvas):
    """ Создаёт яблоко красного цвета в случайной позиции в окне """
    posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)

    return canvas.create_oval(posx, posy, posx+SEG_SIZE, posy+SEG_SIZE, fill="tomato")


movement_map = {
    'Down': (0, 1),
    'Right': (1, 0),
    'Up': (0, -1),
    'Left': (-1, 0)
}


class Segment:
    """ Класс сегмента змейки, сегмент змейки прямоугольник """
    def __init__(self, x, y, size, canvas):
        self.x = x
        self.y = y
        self.size = size
        self.canvas = canvas
        self.shape = canvas.create_rectangle(x, y, x + size, y + size, fill='white')

    @property
    def coords(self):
        """ Координаты сегмента """
        return self.x, self.y

    @property
    def rect(self):
        """ Координаты прямоугольника, описывающего сегмент """
        return self.x, self.y, self.x + self.size, self.y + self.size

    def move_to(self, x, y):
        """ Передвинуть сегмент в указанные координаты """
        self.canvas.coords(self.shape, x, y, x + self.size, y + self.size)
        self.x, self.y = x, y


class Snake:
    """ Класс змейки, набор сегментов """
    def __init__(self, canvas, segments):
        self.canvas = canvas
        self.segments = segments
        self._last_tail_position = self.tail.coords

    @property
    def head(self):
        return self.segments[-1]

    @property
    def tail(self):
        return self.segments[0]

    def move(self, vector):
        """ Двигаем змейку в заданном направлении """
        self._last_tail_position = self.tail.coords
        for first, second in zip(self.segments[:-1], self.segments[1:]):
            first.move_to(*second.coords)

        x, y = self.head.coords
        size = self.head.size
        self.head.move_to(x + vector[0] * size, y + vector[1] * size)

    def add_segment(self):
        """ Добавляет сегмент змейке """
        self.segments.insert(0,
                             Segment(self._last_tail_position[0],
                                     self._last_tail_position[1],
                                     self.tail.size,
                                     self.canvas))


class World:
    def __init__(self, canvas, snake, apple, width, height):
        self.canvas = canvas
        self.snake = snake
        self.apple = apple
        self.width = width
        self.height = height
        self.current_vector = movement_map['Right']

    def move(self):
        self.snake.move(self.current_vector)
        x1, y1, x2, y2 = self.snake.head.rect
        if x2 > self.width or x1 < 0 or y1 < 0 or y2 > self.height:
            return False

        if any(seg.rect == self.snake.head.rect for seg in self.snake.segments[:-1]):
            return False

        if self.snake.head.rect == tuple(int(c) for c in self.canvas.coords(self.apple)):
            self.snake.add_segment()
            self.canvas.delete(self.apple)
            self.apple = create_apple(self.canvas)

        return True


def change_direction(world, event):
    if event.keysym in movement_map:
        world.current_vector = movement_map[event.keysym]


def main_loop(world, root):
    result = world.move()
    if result:
        root.after(100, main_loop, world, root)
    else:
        world.canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Конец игры!", font="Arial 36", fill="black")


def main():
    # Создаём окно
    root = Tk()
    # Устанавливаем название окна
    root.title("Змейка")
    c = Canvas(root, width=WIDTH, height=HEIGHT, bg="green yellow")
    c.grid()
    # нажатие клавиш
    c.focus_set()
    # создаем набор сегментов
    segments = [Segment(SEG_SIZE, SEG_SIZE, SEG_SIZE, c),
                Segment(SEG_SIZE*2, SEG_SIZE, SEG_SIZE, c),
                Segment(SEG_SIZE*3, SEG_SIZE, SEG_SIZE, c)]
    # Сама змейка
    s = Snake(c, segments)
    apple = create_apple(c)

    world = World(c, s, apple, WIDTH, HEIGHT)
    # Реакция на нажатие
    c.bind("<KeyPress>", lambda e: change_direction(world, e))

    main_loop(world, root)
    # Запуск окна
    root.mainloop()


if __name__ == '__main__':
    main()
