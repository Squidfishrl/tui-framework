"""Demo
Last update: v0.16.0
"""

from tui._coordinates import Coordinates
from tui.app import App
from tui.components.button import Button
from tui.components.division import Division
from tui.components.label import Label
from tui.event_broker import EventBroker
from tui.mouse import MouseAction, MouseButton, MouseEvent
from tui.styles.border import DefaultBorder


def main():
    # Create app instance with preset rows and columns
    app = App(rows=51, columns=72)
    app.root = Division(style="rows=51, columns=72, padding=1, padding_top=0, padding_bottom=0, margin_top=1", identifier="root")
    app.root.add_border(DefaultBorder)

    # header
    header = Division(
        Label(
            "<",
            style="rows=3, columns=6, padding_left=1, padding_right=1, margin_left=1, vertical_align=top",
            identifier="back"
        ),
        Division(
            style="columns=37",
            identifier="empty"
        ),
        Button(
            "Login",
            identifier="login-btn",
            style="rows=3, columns=10, padding_left=1, padding_right=1, margin_right=1, text_align=center, vertical_align=center"
        ),
        Button(
            "Register",
            style="rows=3, columns=12, padding_left=1, padding_right=1, text_align=center, vertical_align=center",
            identifier="register-btn"
        ),

        style="rows=5, columns=68, display=inline",
        identifier="header",
    )

    header.add_border(DefaultBorder)

    header.children.get_by_id("register-btn").add_border(DefaultBorder)
    header.children.get_by_id("login-btn").add_border(DefaultBorder)
    app.root.append_child(header)

    # body
    body = Division(style="rows=43, columns=68, display=inline", identifier="body")

    # sidebar
    sidebar = Division(style="rows=43, columns=15, padding=1")
    sidebar.add_border(DefaultBorder)

    about = Button(style="rows=3, columns=11, padding_left=1, vertical_align=center, text_align=center")
    about.add_border(DefaultBorder)
    about.text = "About"  # add text after initialisation

    content = Button(style="rows=3, columns=11, padding_left=1, vertical_align=center, text_align=center")
    content.add_border(DefaultBorder)
    content.text = "Content"

    # main
    main = Division(style="rows=43, columns=53, margin=2, padding_left=1,\
            padding_right=1")
    main.add_border(DefaultBorder)
    main_content = Label("Hello, world!", style="rows=36, columns=45, padding=1")
    main.append_child(main_content)

    app.root.append_child(body)
    body.append_child(sidebar)
    body.append_child(main)
    sidebar.append_child(about)
    sidebar.append_child(content)

    text1 = "111 text 11111"
    text2 = "2222222 text\n2222"
    text_showcase = "This is the about page. Here, the auto-wrap feature will be showcased as per defined in text style standard.\n Left click should cycle between messages and right click should cycle back"
    texts = [text1, text2, text_showcase]

    def switch_text(event):
        main_content.clear()
        main_content.text = texts[switch_text.text_index % len(texts)]
        switch_text.text_index += 1 if event.action == MouseButton.LEFT else -1

    switch_text.text_index = 0

    EventBroker.subscribe(
        MouseEvent(
            coordinates=Coordinates(0, 0),
            action=MouseAction.MOUSE_UP,
            button=MouseButton.LEFT,
            modifiers=frozenset()
        ),
        subscriber=about,
        pre_composition=lambda event: switch_text(event),
        local=False
    )

    EventBroker.subscribe(
        MouseEvent(
            coordinates=Coordinates(0, 0),
            action=MouseAction.MOUSE_UP,
            button=MouseButton.RIGHT,
            modifiers=frozenset()
        ),
        subscriber=about,
        pre_composition=lambda event: switch_text(event),
        local=False
    )

    app.run()


if __name__ == "__main__":
    main()
