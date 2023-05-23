"""Tested in version 0.18.6"""

from tui.app import App
from tui.components.input import Input
from tui.components.label import Label
from tui.events.event_broker import EventBroker
from tui.events.mouse import MouseEventTypes
from tui.events.mouse_event import MouseEvent
from tui.styles.border import DefaultBorder

app = App(rows=30, columns=100)

# app.root.set_style("padding", 25)
lbl = Label("Hello World!", style="rows=14, columns=98")
lbl.add_border(DefaultBorder)
app.root.append_child(lbl)
app.root.add_border(DefaultBorder)

inp = Input(placeholder="", style="rows=5, columns=98, margin_top=2")
inp.add_border(DefaultBorder)
app.root.append_child(inp)

def change_lbl_text(event: MouseEvent) -> None:
    # lbl.text = f"Mouse row - {event.coordinates.row}    \nMouse column - {event.coordinates.column}    \nComponent has focus - {lbl.has_focus()}     \nLabel rect mapping:\n    Top Left - {lbl._rect_mapping.top_left}\n    Bottom Right - {lbl._rect_mapping.bottom_right}"
    lbl.text = f"Mouse row - {event.coordinates.row}    \nMouse column - {event.coordinates.column}    \nInput has focus - {inp.has_focus()}     \nInput rect mapping:\n    Top Left - {inp._rect_mapping.top_left}\n    Bottom Right - {inp._rect_mapping.bottom_right}\nRoot rect mapping:\n    Top Left - {app.root._rect_mapping.top_left}\n    Bottom Right - {app.root._rect_mapping.bottom_right}\nLabel rect mapping:\n    Top Left - {lbl._rect_mapping.top_left}\n    Bottom Right - {lbl._rect_mapping.bottom_right}"

EventBroker.subscribe(
    event=MouseEventTypes.MOUSE_MOVE,
    subscriber=None,
    pre_composition=change_lbl_text
)

EventBroker.subscribe(
    event=MouseEventTypes.MOUSE_LEFT_CLICK,
    subscriber=None,
    pre_composition=change_lbl_text
)

EventBroker.subscribe(
    event=MouseEventTypes.MOUSE_MOVE,
    subscriber=None,
    pre_composition=change_lbl_text
)

EventBroker.subscribe(
    event=MouseEventTypes.MOUSE_LEFT_CLICK,
    subscriber=None,
    pre_composition=change_lbl_text
)

app.run()
