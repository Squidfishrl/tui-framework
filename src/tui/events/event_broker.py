"""Manages events"""


from typing import Optional
from tui.component import Component
from tui.components.division import Division
from tui.events.event import Event
from tui.events.event_listener import Callback, EventListener
from tui.events.mouse import MouseEventTypes
from tui.events.mouse_event import MouseEvent


class EventBroker:
    """Responsible for managing events"""

    # a 'subscriber' with id -1 is used to signify a global event
    global_component = Division(identifier='-1')

    def __init__(self):
        self.listeners: dict[Event, list[EventListener]] = {}
        self.subscribers: dict[Component, list[EventListener]] = {}

    def subscribe(
            self,
            event: Event | MouseEventTypes,
            subscriber: Optional[Component],
            pre_composition: Optional[Callback] = None,
            post_composition: Optional[Callback] = None,
    ) -> EventListener:
        """Create an event listener.
        Converts different event types to Event ones
        """
        if isinstance(event, MouseEventTypes):
            _event = event.value
            print(_event)
        else:
            _event = event

        if subscriber is None:
            subscriber = EventBroker.global_component

        return self._subscribe(event=_event,
                               subscriber=subscriber,
                               pre_composition=pre_composition,
                               post_composition=post_composition)

    def _subscribe(
            self,
            event: Event,
            subscriber: Component,
            pre_composition: Optional[Callback] = None,
            post_composition: Optional[Callback] = None,
    ) -> EventListener:
        """Create an event listener"""

        listener = EventListener(
                    event=event,
                    subscriber=subscriber,
                    pre_composition=pre_composition,
                    post_composition=post_composition
                )

        if self.listeners.get(event) is None:
            # if no event entry exists in the dictionary, create a new one
            self.listeners[event] = [listener]
        else:
            # if one already exists, append the new event listener
            self.listeners[event].append(listener)

        if self.subscribers.get(subscriber) is None:
            # if no event entry exists in the dictionary, create a new one
            self.subscribers[subscriber] = [listener]
        else:
            # if one already exists, append the new event listener
            self.subscribers[subscriber].append(listener)

        return listener

    def unsubscribe(
            self,
            component: Optional[Component],
            listener: EventListener
    ) -> None:
        """Unsubscribe a listener from a component
        If component is None, unsubscribe a global listener.
        """
        if component is None:
            component = EventBroker.global_component

        self._unsubscribe(component=component, listener=listener)


    def _unsubscribe(
            self,
            component: Component,
            listener: EventListener
    ) -> None:
        """Unsubscribe a listener from a component"""
        if listener in self.subscribers[component]:
            self.listeners[listener.event].remove(listener)
            self.subscribers[component].remove(listener)

    def unsubscribe_all(self, component: Component) -> None:
        """Unsubscribe all listeners for a component"""
        try:
            for listener in self.subscribers[component]:
                self.listeners[listener.event].remove(listener)
                self.subscribers[component].remove(listener)
            del self.subscribers[component]
        except KeyError:
            # Do nothing if no events exist for this component
            pass

    def handle(self, event: Event) -> tuple[list[Callback], list[Callback]]:
        """Find the corresponding listeners and prepare their callbacks"""
        pre_composit_hook = []
        post_composit_hook = []

        if isinstance(event, MouseEvent):
            event = event.event.value

        try:
            for listener in self.listeners[event]:
                if listener.pre_composition is not None:
                    pre_composit_hook.append(listener.pre_composition)
                if listener.post_composition is not None:
                    post_composit_hook.append(listener.post_composition)
        except KeyError:
            # Do nothing if event isn't listened to
            pass

        return pre_composit_hook, post_composit_hook
