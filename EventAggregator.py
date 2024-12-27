import collections
import contextlib
import logging
from typing import Callable, Dict, List, Type, Any

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
        return cls._instance

    def __init__(self) -> None:
        self._subscribers: Dict[Type, List[Callable]] = collections.defaultdict(list)

    def subscribe(self, event_type, subscriber: Callable) -> None:
        self._subscribers[event_type].append(subscriber)
        logger.debug(f'SUBSCRIBE {str(subscriber)} to {event_type}')

    def event(self, event: BaseModel) -> None:
        for subscriber in self._subscribers[type(event)]:
            subscriber(event)
        logger.debug(f'NEW EVENT: {event}')

    def unsubscribe(self, event_type, subscriber: Callable) -> None:
        with contextlib.suppress(ValueError):
            self._subscribers[event_type].remove(subscriber)
        logger.debug(f'UNSUBSCRIBE {str(subscriber)} from {event_type}')

    def unsubscribe_all(self, subscriber) -> None:
        for subscribers in self._subscribers.values():
            with contextlib.suppress(ValueError):
                subscribers.remove(subscriber)
        logger.debug(f'UNSUBSCRIBE ALL {str(subscriber)} ')
