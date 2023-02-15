"""A button is a widget which can be pressed. Once clicked, it will
asynchronously execute a user defined function. The button inherits all the
functionalities that the label widget has."""

from __future__ import annotations

import functools
from typing import Any, Awaitable, Callable, Optional, Protocol

from tui.components.label import Label
from tui.style import Style


class Callback(Protocol):
    """Type annotation for a callable that can take any arguments"""
    def __call__(self, *args: Any, **kwargs: Any) -> None: ...


class Button(Label):
    """A widget which executes a function when it's signaled"""
    def __init__(
            self,
            identifier: Optional[str] = None,  # Unique identifier
            style: str | Style = Style(),  # Style properties for the component
            text: str = "",  # The text that's displayed on the button
    ) -> None:
        super().__init__(identifier=identifier, style=style, label_text=text)
        # functions subscribed to the onclick event
        self._on_click: list[Callable[[], Awaitable[None]]] = []

    def on_click(self, *_args: Any, **_kwargs: Any):
        """Pass arguments to the on_click decorator"""
        def decorator_onclick(func: Callback) -> Callable[[], Awaitable[None]]:
            """Subscribe a function to the on_click event and make it async"""
            @functools.wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> None:
                """Async wrapper that passes parameters to func"""
                args = _args
                kwargs = _kwargs
                return func(*args, **kwargs)
            # add the function to the subscriber list
            self._on_click.append(wrapper)
            return wrapper
        return decorator_onclick

    async def click_signal(self) -> None:
        """Execute all functions subscribed to the on_click event"""
        for func in self._on_click:
            await func()
