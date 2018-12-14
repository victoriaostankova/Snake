from tkinter import *
import random
# Ширина экрана
WIDTH = 800
# Высота экрана
HEIGHT = 600
# Размер сегмента змейки
SEG_SIZE = 20
# Переменная отвечающая за состояние игры
IN_GAME = True
# Создание вспомогательных функций
def create_block():
    """ Создаёт яблоко в случайной позиции в окне """
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
    # блок это яблоко красного цвета
    BLOCK = c.create_oval(posx, posy,

                          posx+SEG_SIZE, posy+SEG_SIZE,

                          fill="tomato")
def main():
    """ Оснавная функция, которая управляет игровым процессом"""
    global IN_GAME
    if IN_GAME:
        # Двигаем змейку
        s.move()
        # Определяем координаты головы
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Столкновение с границами экрана
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        # Поедание яблок
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()
        # Самоедство
        else:
            # Проходим по всем сегментам змеи
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False
        root.after(100, main)
    # Конец игры, сообщение о проигрыше
    else:
        c.create_text(WIDTH/2, HEIGHT/2,
                      text="Конец игры!",
                      font="Arial 36",
                      fill="black")
class Segment(object):
    """ Класс сегмента змейки, сегмент змейки прямоугольник """
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x+SEG_SIZE, y+SEG_SIZE,
                                           fill="white")
class Snake(object):
    """ Класс змейки, набор сегментов """
    def __init__(self, segments):
        self.segments = segments
        # Список доступных движений змейки
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # Изначально змейка двигается вправо
        self.vector = self.mapping["Right"]
    def move(self):
        """ Двигаем змейку в заданном направлении """
        # Перебираем все сегменты кроме первого
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            # задаем каждому сегменту позицию сегмента стоящего после него
            c.coords(segment, x1, y1, x2, y2)
        # получаем координаты сегмента перед "головой"
        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        # помещаем "голову" в направлении указанном в векторе движения
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)
    def add_segment(self):
        """ Добавляет сегмент змейке """
        # определяем последний сегмент
        last_seg = c.coords(self.segments[0].instance)
        # определяем координаты куда поставить следующий сегмент
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        # добавляем змейке еще один сегмент в заданных координатах
        self.segments.insert(0, Segment(x, y))
    def change_direction(self, event):
        """ Изменяет направление движения змейки """
        # event передаст нам символ нажатой клавиши
        # и если эта клавиша в доступных направлениях
        # изменяем направление
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]
# Создаём окно
root = Tk()
# Устанавливаем название окна
root.title("Змейка")
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="green yellow")
c.grid()
# нажатие клавиш
c.focus_set()
# создаем набор сегментов
segments = [Segment(SEG_SIZE, SEG_SIZE),
            Segment(SEG_SIZE*2, SEG_SIZE),
            Segment(SEG_SIZE*3, SEG_SIZE)]
# Сама змейка
s = Snake(segments)
# Реакция на нажатие
c.bind("<KeyPress>", s.change_direction)
create_block()
main()
# Запуск окна
root.mainloop()