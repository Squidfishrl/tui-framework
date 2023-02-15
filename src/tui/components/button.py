"""A button is a widget which can be pressed. Once clicked, it will
asynchronously execute a user defined function. The button inherits all the
functionalities that the label widget has."""

from __future__ import annotations

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
        def decorator_onclick(func: Callback) -> Callable[[], None]:
            """Subscribe a function with set parameters to the on_click event
            while making sure it's async"""
            def wrapper(*args: Any, **kwargs: Any) -> None:
                """Regular wrapper - makes chaining multiple decorators not
                interfere with eachother"""
                return func(*args, **kwargs)

            async def async_param_wrapper() -> None:
                """Async wrapper with fixed function parameters"""
                return func(*_args, **_kwargs)

            # add the function with pre-set parameters
            self._on_click.append(async_param_wrapper)
            # return the basic non-modified function wrapper
            return wrapper
        return decorator_onclick

    async def click_signal(self) -> None:
        """Execute all functions subscribed to the on_click event"""
        for func in self._on_click:
            await func()
