"""The event broker is a middle ground layer between the event producer thread
and the 'consumer' listeners. It handles subscribing listeners to events and
calling them on event trigger."""


from typing import Optional
from tui.component import Component
from tui.components.division import Division
from tui.events.event import Event
from tui.events.event_listener import Callback, EventListener
from tui.events.key_event import HotkeyEvent
from tui.events.keys import Keys
from tui.events.mouse import MouseEventTypes
from tui.events.mouse_event import MouseEvent


class EventBroker:
    """Responsible for managing event subscription and event callbacks"""

    # a 'subscriber' with id == -1 is used to signify a global event
    __global_component = Division(identifier='-1')

    listeners: dict[Event, list[EventListener]] = {}
    subscribers: dict[Component, list[EventListener]] = {}

    @staticmethod
    def subscribe(
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
        else:
            _event = event

        if subscriber is None:
            subscriber = EventBroker.__global_component

        return EventBroker._subscribe(event=_event,
                                      subscriber=subscriber,
                                      pre_composition=pre_composition,
                                      post_composition=post_composition)

    @staticmethod
    def _subscribe(
            event: Event,
            subscriber: Component,
            pre_composition: Optional[Callback] = None,
            post_composition: Optional[Callback] = None,
    ) -> EventListener:
        """Create an event listener, given a subscriber component. If the
        subscriber component has focus and the corresponding event is received,
        the pre_composition function is called back, then global composition
        occurs, then post_composition functions are executed.

        This is an inner function, only to be called by EventBroker.subscribe
        after arguments are handled.
        """

        listener = EventListener(
                    event=event,
                    subscriber=subscriber,
                    pre_composition=pre_composition,
                    post_composition=post_composition
                )

        if EventBroker.listeners.get(event) is None:
            # if no event entry exists in the dictionary, create a new one
            EventBroker.listeners[event] = [listener]
        else:
            # if one already exists, append the new event listener
            EventBroker.listeners[event].append(listener)

        if EventBroker.subscribers.get(subscriber) is None:
            # if no event entry exists in the dictionary, create a new one
            EventBroker.subscribers[subscriber] = [listener]
        else:
            # if one already exists, append the new event listener
            EventBroker.subscribers[subscriber].append(listener)

        return listener

    @staticmethod
    def unsubscribe(listener: EventListener) -> None:
        """Unsubscribe an event listener from a component"""
        component = listener.subscriber

        if listener in EventBroker.subscribers[component]:
            EventBroker.listeners[listener.event].remove(listener)
            EventBroker.subscribers[component].remove(listener)

    @staticmethod
    def unsubscribe_all(component: Component) -> None:
        """Unsubscribe all listeners for a component"""
        try:
            for listener in EventBroker.subscribers[component]:
                EventBroker.listeners[listener.event].remove(listener)
                EventBroker.subscribers[component].remove(listener)
            del EventBroker.subscribers[component]
        except KeyError:
            # Do nothing if no events exist for this component
            pass

    @staticmethod
    def handle(
            event: Event,
            pre_composit_hook: list[Callback],
            post_composit_hook: list[Callback]
    ) -> None:
        """Find the corresponding listeners for an event and prepare their
        callbacks. The callbacks are appended to the pre/post composite hooks.
        """

        def handle_listener(listener: EventListener, event: Event) -> None:
            # don't handle events when the subscriber isn't in focus
            if (not listener.subscriber.has_focus()
                    and listener.subscriber.id != '-1'):
                return

            if listener.pre_composition is not None:
                pre_composit_hook.append(
                        lambda: listener.pre_composition(event)
                    )
            if listener.post_composition is not None:
                post_composit_hook.append(
                        lambda: listener.post_composition(event)
                    )

        # Convert MouseEvent to _MouseEvent, since that is what listeners are
        # subscribed to
        if isinstance(event, MouseEvent):
            _event = event.event.value
        else:
            _event = event

        try:
            for listener in EventBroker.listeners[_event]:
                handle_listener(listener, event)

        except KeyError:
            # Do nothing if event isn't listened to
            pass

        if isinstance(_event, HotkeyEvent):
            try:
                for listener in EventBroker.listeners[HotkeyEvent(Keys.Any)]:
                    handle_listener(listener, _event)
            except KeyError:
                # Do nothing if event isn't listened to
                pass
