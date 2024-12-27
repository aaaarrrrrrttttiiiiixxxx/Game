import collections
import contextlib
from typing import Callable, Dict, List, Type, Any

from pydantic import BaseModel


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

    def event(self, event: BaseModel) -> None:
        for subscriber in self._subscribers[type(event)]:
            subscriber(event)

    def unsubscribe(self, event_type, subscriber: Callable) -> None:
        with contextlib.suppress(ValueError):
            self._subscribers[event_type].remove(subscriber)

    def unsubscribe_all(self, subscriber) -> None:
        for subscribers in self._subscribers.values():
            with contextlib.suppress(ValueError):
                subscribers.remove(subscriber)
