import math
from typing import Union, Tuple


def calc_diffs(direction_x: Union[int, float], direction_y: Union[int, float],
               dist: Union[int, float]) -> Tuple[Union[int, float], Union[int, float]]:
    if direction_y == 0:
        move_x = dist
        move_y = 0.0
    else:
        ratio = abs(direction_x / direction_y)
        move_y = dist / math.sqrt(ratio * ratio + 1)
        move_x = move_y * ratio
    diff_x = move_x if direction_x > 0 else -move_x
    diff_y = move_y if direction_y > 0 else -move_y
    return diff_x, diff_y


def calc_movement_step(x_1: Union[int, float], y_1: Union[int, float],
                       x_2: Union[int, float], y_2: Union[int, float],
                       dist: Union[int, float]) -> Tuple[Union[int, float], Union[int, float]]:
    direction_x = x_1 - x_2
    direction_y = y_1 - y_2

    if math.sqrt(direction_x ** 2 + direction_y ** 2) < dist:
        return direction_x, direction_y
    else:
        return calc_diffs(direction_x, direction_y, dist)
