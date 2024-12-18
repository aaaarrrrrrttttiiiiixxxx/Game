import math
from typing import Optional, Tuple, Union

from pygame import Surface

from camera import Camera
from units.base_units import BaseDrawable
from units.image_stores import InfinityImageStore
from utils import calc_diffs


class MovingToPointUnit(BaseDrawable):
    image_path: str
    image_store_type = InfinityImageStore
    move_speed: Union[int, float]

    def __init__(self, camera: Camera, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0) -> None:
        super().__init__(camera, unit_layer, screen, initial_x, initial_y)
        self.target: Optional[Tuple[Union[int, float], Union[int, float]]] = None

    def set_target(self, x: Union[int | float], y: Union[int, float]) -> None:
        self.target = (x, y)

    def _on_reach_target(self) -> None:
        pass

    def process_next_frame(self):
        super().process_next_frame()
        if self.target:
            direction_x = self.target[0] - self.rect.centerx
            direction_y = self.target[1] - self.rect.centery
            if math.sqrt(direction_x ** 2 + direction_y ** 2) < self.move_speed:
                self._on_reach_target()
                return
            diff_x, diff_y = calc_diffs(direction_x, direction_y, self.move_speed)
            self.move(diff_x, diff_y)

    def move(self, diff_x: Union[int, float], diff_y: Union[int, float], screen: bool = False) -> None:
        super().move(diff_x, diff_y, screen)
        if screen and self.target:
            self.target = (self.target[0] + diff_x, self.target[1] + diff_y)
