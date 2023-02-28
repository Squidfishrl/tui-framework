"""Compnoents that listen to events"""

from __future__ import annotations

from typing import Any, Awaitable, Optional, Protocol

from tui.component import Component
from tui.events.event import Event


class EventListener:
    """Responsible for defining the component's behaviour for events"""
    def __init__(
            self,
            event: Event,
            # when no component is passed the evenet is considered global
            subscriber: Optional[Component],
            pre_composition: Optional[Callback] = None,
            post_composition: Optional[Callback] = None
    ) -> None:
        self.event = event
        self.subscriber = subscriber
        self.pre_composition = pre_composition
        self.post_composition = post_composition


class Callback(Protocol):
    """Type annotation for a callable that can take any arguments"""
    def __call__(self, *args: Any, **kwargs: Any) -> Awaitable[None]: ...
