"""Manages events"""


from typing import Optional
from tui.component import Component
from tui.event_listener import Callback, EventListener
from tui.keys import Keys
from tui.mouse import MouseEvent


class EventBroker:
    """Responsible for managing events"""
    global_listeners: dict[str | tuple[Keys] | MouseEvent, list[EventListener]] = {}
    global_subscribers: dict[Component, list[EventListener]] = {}
    component_listeners: dict[str | tuple[Keys] | MouseEvent, list[EventListener]] = {}
    local_subscribers: dict[Component, list[EventListener]] = {}

    @staticmethod
    def subscribe(
            event: str | tuple[Keys] | MouseEvent,
            subscriber: Component,
            pre_composition: Optional[Callback] = None,
            post_composition: Optional[Callback] = None,
            local: bool = True  # is the event local?
    ) -> EventListener:
        """Create an event listener"""
        listener = EventListener(
                    event_type=event,
                    subscriber=subscriber,
                    pre_composition=pre_composition,
                    post_composition=post_composition
                )

        if local:
            listener_dict = EventBroker.component_listeners
            subscriber_events = EventBroker.local_subscribers
        else:
            listener_dict = EventBroker.global_listeners
            subscriber_events = EventBroker.global_subscribers

        listener_arr = listener_dict.get(event)
        if listener_arr is None:
            listener_dict[event] = [listener]
        else:
            listener_arr.append(listener)

        event_arr = subscriber_events.get(subscriber)
        if event_arr is None:
            subscriber_events[subscriber] = [listener]
        else:
            event_arr.append(listener)

        return listener

    @staticmethod
    def unsubscribe(component: Component, listener: EventListener) -> None:
        """Unsubscribe a listener from a component"""
        if listener in EventBroker.local_subscribers[component]:
            EventBroker.component_listeners[listener.event_type].remove(listener)
            EventBroker.local_subscribers[component].remove(listener)

        if listener in EventBroker.global_subscribers[component]:
            EventBroker.global_listeners[listener.event_type].remove(listener)
            EventBroker.global_subscribers[component].remove(listener)

    @staticmethod
    def unsubscribe_all(component: Component) -> None:
        """Unsubscribe all listeners from a component"""
        try:
            for listener in EventBroker.local_subscribers[component]:
                EventBroker.component_listeners[listener.event_type].remove(listener)
                EventBroker.local_subscribers[component].remove(listener)
            del EventBroker.local_subscribers[component]
        except KeyError:
            pass

        try:
            for listener in EventBroker.global_subscribers[component]:
                EventBroker.global_listeners[listener.event_type].remove(listener)
                EventBroker.global_subscribers[component].remove(listener)
            del EventBroker.global_subscribers[component]
        except KeyError:
            pass

    @staticmethod
    def handle(
            event: str | tuple[Keys] | MouseEvent
    ) -> tuple[list[Callback], list[Callback]]:
        """Find the corresponding listeners and prepare their callbacks"""
        pre_composit_hook = []
        post_composit_hook = []

        try:
            for listener in EventBroker.global_listeners[event]:
                if listener.pre_composition is not None:
                    pre_composit_hook.append(listener.pre_composition)
                if listener.post_composition is not None:
                    post_composit_hook.append(listener.post_composition)
        except KeyError:
            pass

        try:
            for listener in EventBroker.component_listeners[event]:
                # skip subscribers without focus
                if not listener.subscriber.has_focus:
                    continue

                if listener.pre_composition is not None:
                    pre_composit_hook.append(listener.pre_composition)
                if listener.post_composition is not None:
                    post_composit_hook.append(listener.post_composition)
        except KeyError:
            pass

        return pre_composit_hook, post_composit_hook
