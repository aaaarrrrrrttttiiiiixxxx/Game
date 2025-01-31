import pygame
import logging.config

WIDTH = 640
HEIGHT = 480
# WIDTH = 2560
# HEIGHT = 1440
CAMERA_MOVE = 0.1
# CAMERA_MOVE = None
FPS = 30
HIT_NEAREST = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

ENEMY_SPAWN_RATE = 50

pygame.font.init()
FONT = pygame.font.SysFont(None, 16)  # type: ignore
UPGRADE_FONT = pygame.font.SysFont(None, 28)  # type: ignore

LVL_UP = pygame.USEREVENT + 1

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        # '': {
        #     'handlers': ['default'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
        'event': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)
