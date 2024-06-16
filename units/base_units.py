import contextlib
import logging
import math
from typing import final, Optional, Union, Type

from pygame import Surface, Rect
from pygame.sprite import Sprite

from camera import Camera
from config import FONT, RED, FPS
from units.image_stores import BaseImageStore
from utils import calc_movement_step, calc_diffs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BaseDrawable(Sprite):
    image_path: str
    image_store_type: Type[BaseImageStore] = BaseImageStore
    reloaded_store = True
    height = 50
    width = 50

    def __init__(self, camera: Camera, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0) -> None:
        super(BaseDrawable, self).__init__()
        self.image_store = self.image_store_type(self.image_path, self.reloaded_store)
        self.screen = screen
        self.camera = camera
        self.rect = Rect(initial_x, initial_y, self.width, self.height)
        self.rect.center = (initial_x, initial_y)
        self.unit_layer = unit_layer

    def draw(self) -> None:
        self.screen.blit(self.image_store.get_image(), self.camera.map(*self.rect.topleft))

    def move(self, diff_x: Union[int, float], diff_y: Union[int, float], screen: bool = False) -> None:
        self.rect.x += diff_x  # type: ignore
        self.rect.y += diff_y  # type: ignore

    def move_to(self, res_x: int, res_y: int) -> None:
        self.rect.x = res_x
        self.rect.y = res_y

    def dist_from(self, x: int, y: int) -> float:
        return math.sqrt((self.rect.x - x) * (self.rect.x - x) + (self.rect.y - y) * (self.rect.y - y))

    def process_next_frame(self):
        self.image_store.next_frame()

    def draw_interface(self) -> None:
        pass


class BaseUnit(BaseDrawable):
    max_hp: Optional[int] = None
    base_hp_regen = 0.0
    attack_speed: Optional[Union[int, float]] = None

    def __init__(self, camera: Camera, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0) -> None:
        super().__init__(camera, unit_layer, screen, initial_x, initial_y)
        if self.max_hp is not None:
            self.hp = float(self.max_hp)
            self.hp_regen = self.base_hp_regen
        if self.attack_speed:
            self.attack_freeze = 0.0

    @final
    def update(self, action: str, **kwargs) -> None:
        with contextlib.suppress(AttributeError, TypeError):
            self.__getattribute__(action)(**kwargs)

    @property
    def radius(self) -> int:
        return int(math.sqrt(self.rect.w ** 2 + self.rect.h ** 2) / 2)

    def draw(self) -> None:
        super().draw()
        self.draw_text()

    def attack(self) -> None:
        if self.attack_speed and self.attack_freeze <= 0:
            self._attack()
            self.attack_freeze = FPS / self.attack_speed

    def _attack(self) -> None:
        pass

    def draw_text(self) -> None:
        if self.max_hp and self.hp:
            img2 = FONT.render(f'{int(self.hp)} / {self.max_hp}', True, RED)
            x, y = self.rect.topleft
            y -= 10
            self.screen.blit(img2, self.camera.map(x, y))

    def got_attack(self, incoming_damage: int) -> None:
        self.hp -= incoming_damage
        if self.hp <= 0:
            self._dead()

    def _dead(self) -> None:
        self.kill()

    def process_next_frame(self) -> None:
        super().process_next_frame()
        if self.max_hp and self.hp and self.hp_regen:
            self.hp += self.hp_regen / FPS
            if self.hp > self.max_hp:
                self.hp = self.max_hp
        if self.attack_speed:
            self.attack_freeze -= 1


class MovingToTargetUnit(BaseUnit):
    move_speed: Union[int, float]

    def __init__(self, camera: Camera, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0) -> None:
        super().__init__(camera, unit_layer, screen, initial_x, initial_y)
        self.target = None  # type: Optional[BaseUnit]
        self.rect.center = initial_x, initial_y

    def set_target(self, target: BaseUnit) -> None:
        self.target = target

    def _on_reach_target(self) -> None:
        pass

    def reach_target(self, distance_x: int, distance_y: int) -> bool:
        return math.sqrt(distance_x ** 2 + distance_y ** 2) < self.move_speed

    def make_movement_step(self, use_collide: bool = False) -> None:
        if self.target:
            calc_movement_step(*self.target.rect.center, *self.rect.center, self.move_speed)
            direction_x = self.target.rect.centerx - self.rect.centerx
            direction_y = self.target.rect.centery - self.rect.centery
            if self.reach_target(direction_x, direction_y):
                self._on_reach_target()
                return
            diff_x, diff_y = calc_diffs(direction_x, direction_y, self.move_speed)
            if use_collide:
                self.unit_layer.move(self, 0, diff_y)
                self.unit_layer.move(self, diff_x, 0)
            else:
                self.move(int(diff_x), int(diff_y))
