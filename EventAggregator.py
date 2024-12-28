import collections
import contextlib
import logging
from typing import Callable, Any

from pydantic import BaseModel

logger = logging.getLogger('event')
logger.setLevel(logging.DEBUG)


class DamageEvent(BaseModel):
    attacking_unit: Any
    target_unit: Any
    damage: int


class AttackEvent(DamageEvent):
    pass


class DealDamageEvent(DamageEvent):
    pass


class EventAggregator:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._subscribers = collections.defaultdict(list)
        return cls._instance

    def subscribe(self, event_type, subscriber: Callable) -> None:
        self._subscribers[event_type].append(subscriber)  # type: ignore
        logger.debug(f'SUBSCRIBE {str(subscriber)} to {event_type}')

    def event(self, event: BaseModel) -> None:
        for subscriber in self._subscribers[type(event)]:  # type: ignore
            subscriber(event)
        logger.debug(f'NEW EVENT {type(event)}: {event}')

    def unsubscribe(self, event_type, subscriber: Callable) -> None:
        with contextlib.suppress(ValueError):
            self._subscribers[event_type].remove(subscriber)  # type: ignore
        logger.debug(f'UNSUBSCRIBE {str(subscriber)} from {event_type}')

    def unsubscribe_all(self, subscriber) -> None:
        for subscribers in self._subscribers.values():  # type: ignore
            with contextlib.suppress(ValueError):
                subscribers.remove(subscriber)
        logger.debug(f'UNSUBSCRIBE ALL {str(subscriber)} ')
