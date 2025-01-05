import pygame


class Clock:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.tics = 0
            cls.__instance.pygame_clock = pygame.time.Clock()
        return cls.__instance

    def tick(self, fps):
        self.tics += 1
        self.pygame_clock.tick(fps)

    def reset(self):
        self.tics = 0

    def get_time_minutes(self, fps) -> float:
        return self.tics / fps / 60  # type: ignore
