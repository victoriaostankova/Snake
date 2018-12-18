from Snake import Segment, Snake, World, movement_map
from unittest.mock import MagicMock
from tkinter import Canvas


def test_moving_off_the_world():
    canvas_mocked = MagicMock(spec=Canvas)
    segments = [Segment(1, 0, 1, canvas_mocked)]
    snake = Snake(canvas_mocked, segments)
    world = World(canvas_mocked, snake, None, 2, 2)
    assert world.move() is False


def test_self_eating():
    canvas_mocked = MagicMock(spec=Canvas)
    segments = [
        Segment(0, 0, 1, canvas_mocked),
        Segment(1, 0, 1, canvas_mocked),
        Segment(2, 0, 1, canvas_mocked),
        Segment(2, 1, 1, canvas_mocked),
        Segment(1, 1, 1, canvas_mocked),
    ]
    snake = Snake(canvas_mocked, segments)
    world = World(canvas_mocked, snake, None, 10, 10)
    world.current_vector = movement_map['Up']
    assert world.move() is False


def test_normal_movement():
    canvas_mocked = MagicMock(spec=Canvas)
    segments = [
        Segment(1, 0, 1, canvas_mocked),
        Segment(2, 0, 1, canvas_mocked),
    ]
    snake = Snake(canvas_mocked, segments)
    world = World(canvas_mocked, snake, None, 10, 10)
    assert world.move() is True
