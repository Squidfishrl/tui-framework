"""The event broker is a middle ground layer between the event producer thread
and the 'consumer' listeners. It handles subscribing listeners to events and
calling them on event trigger."""


from typing import Optional
from tui.component import Component
from tui.components.division import Division
from tui.events.event import Event
from tui.events.event_listener import Callback, EventListener
from tui.events.mouse import MouseEventTypes
from tui.events.mouse_event import MouseEvent


class EventBroker:
    """Responsible for managing event subscription and event callbacks"""

    # a 'subscriber' with id ==  -1 is used to signify a global event
    global_component = Division(identifier='-1')

    def __init__(self):
        self.listeners: dict[Event, list[EventListener]] = {}
        self.subscribers: dict[Component, list[EventListener]] = {}

    def subscribe(
            self,
            event: Event | MouseEventTypes,  # the event we listen for
            # the subscriber component must have focus before the event
            # callbacks
            subscriber: Optional[Component],
            # most callbacks are expected to be called before composition
            pre_composition: Optional[Callback] = None,
            # callback after composition is done
            post_composition: Optional[Callback] = None,
    ) -> EventListener:
        """Create an event listener, given a subscriber component. If the
        subscriber component has focus and the corresponding event is received,
        the pre_composition function is called back, then global composition
        occurs, then post_composition functions are executed.
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
        """Create an event listener, given a subscriber component. If the
        subscriber component has focus and the corresponding event is received,
        the pre_composition function is called back, then global composition
        occurs, then post_composition functions are executed.

        This is an inner function, only to be called by self.subscribe after
        arguments are handled.
        """

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
            listener: EventListener
    ) -> None:
        """Unsubscribe an event listener from a component"""
        component = listener.subscriber

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

    def handle(
            self,
            event: Event,
            pre_composit_hook: list[Callback],
            post_composit_hook: list[Callback]
    ) -> None:
        """Find the corresponding listeners for an event and prepare their
        callbacks. The callbacks are appended to the pre/post composite hooks.
        """

        # Convert MouseEvent to _MouseEvent, since that is what listeners are
        # subscribed to
        if isinstance(event, MouseEvent):
            _event = event.event.value
        else:
            _event = event

        try:
            for listener in self.listeners[_event]:
                if listener.pre_composition is not None:
                    pre_composit_hook.append(
                            lambda: listener.pre_composition(event)
                        )
                if listener.post_composition is not None:
                    post_composit_hook.append(
                            lambda: listener.post_composition(event)
                        )
        except KeyError:
            # Do nothing if event isn't listened to
            return
