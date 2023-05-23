"""Tested in 0.18.6"""

from tui.app import App
from tui.components.button import Button
from tui.components.division import Division
from tui.components.input import Input
from tui.components.label import Label
from tui.events.event import Event
from tui.events.event_broker import EventBroker
from tui.events.mouse import MouseEventTypes
from tui.events.mouse_event import MouseEvent
from tui.styles.border import DefaultBorder


def main():
    # Create app instance with preset rows and columns
    app: App = App(fps=60, rows=51, columns=72)
    # app.root = Division(style="rows=51, columns=72, padding=1, padding_top=0, padding_bottom=0, margin_top=1", identifier="root")
    app.root.add_border(DefaultBorder)
    # header
    header = Division(
        Button(
            "x",
            style="rows=3, columns=6, margin_left=1, text_align=center, vertical_align=center",
            identifier="exit-btn"
        ),
        Division(
            Label(
                " [ not logged in ]",
                style="rows=3, columns=37, padding_left=1, padding_right=1, text_align=left, vertical_align=center",
                identifier="login-username"
            ),
            style="rows=3, columns=37",
            identifier="hdr-empty"
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
        style="rows=5, columns=68, display=inline", identifier="header",
    )

    header.add_border(DefaultBorder)

    header.children.get_by_id("exit-btn").add_border(DefaultBorder)
    header.children.get_by_id("register-btn").add_border(DefaultBorder)
    header.children.get_by_id("login-btn").add_border(DefaultBorder)
    app.root.append_child(header)

    # body
    body = Division(style="rows=43, columns=68, display=inline", identifier="body")

    # sidebar
    sidebar = Division(style="rows=43, columns=15, padding=1")
    sidebar.add_border(DefaultBorder)

    home = Button(style="rows=3, columns=11, padding_left=1, vertical_align=center, text_align=center", identifier="home-btn")
    home.add_border(DefaultBorder)
    home.text = "Home "

    about = Button(style="rows=3, columns=11, padding_left=1, vertical_align=center, text_align=center", identifier="about-btn")
    about.add_border(DefaultBorder)
    about.text = "About"  # add text after initialisation

    content = Button(style="rows=3, columns=11, padding_left=1, vertical_align=center, text_align=center", identifier="content-btn")
    content.add_border(DefaultBorder)
    content.text = "Content"

    auth = Division(style="rows=17, columns=64, padding=1, margin=10, margin_left=15, margin_bottom=0")
    username_div = Division(style="rows=1, columns=30, display=inline")
    login = Label("Username: ", style="rows=1, columns=10")
    username_inp = Input(style="rows=1, columns=20")
    deliminer = Division(style="rows=1, columns=30")
    submit = Button(style="rows=3, columns=64, padding_left=1, padding_right=1, margin_left=29, margin_right=25, vertical_align=center, text_align=center")
    submit.add_border(DefaultBorder)
    submit.text = "Submit"

    auth.append_child(username_div)
    username_div.append_child(login)
    username_div.append_child(username_inp)
    auth.append_child(deliminer)

    auth.add_border(DefaultBorder)

    # main
    main = Division(style="rows=43, columns=53, margin=2, padding_left=1,\
            padding_right=1")
    main.add_border(DefaultBorder)
    main_content = Label("", style="rows=36, columns=45, padding=1")
    main.append_child(main_content)

    app.root.append_child(body)
    body.append_child(sidebar)
    sidebar.append_child(home)
    sidebar.append_child(about)
    sidebar.append_child(content)
    body.append_child(main)

    def _home(event: Event):
        main_content.clear()
        main_content.text = "\n \nHome Page - Text User Interface Demo\n \nShowcase some basic functionalities!"

    EventBroker.subscribe(
        event=MouseEventTypes.MOUSE_LEFT_CLICK,
        subscriber=home,
        pre_composition=_home
    )

    def _about(event: Event):
        main_content.clear()
        about_text = "\n \nThis is the about page. Here, the auto-wrap feature will be showcased as per defined in the text style standard. Furthermore, you may click the login or register buttons to see run-time DOM manipulation. Press the exit button on the top left to log out and or quit."
        main_content.text = about_text

    EventBroker.subscribe(
        event=MouseEventTypes.MOUSE_LEFT_CLICK,
        subscriber=about,
        pre_composition=_about
    )

    def _content(event: Event):
        main_content.clear()
        content_text = "\n \nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Proin nibh nisl condimentum id venenatis. Pretium viverra suspendisse potenti nullam ac tortor. Eu facilisis sed odio morbi quis commodo odio aenean sed. Porttitor leo a diam sollicitudin tempor. Neque gravida in fermentum et sollicitudin ac. Mi ipsum faucibus vitae aliquet. Dignissim sodales ut eu sem integer vitae justo. Eleifend quam adipiscing vitae proin sagittis nisl rhoncus mattis rhoncus.\n \n \nNibh sed pulvinar proin gravida hendrerit lectus. Cursus sit amet dictum sit amet justo donec enim. Vitae auctor eu augue ut lectus arcu bibendum at. Facilisis mauris sit amet massa vitae tortor condimentum lacinia. Cursus euismod quis viverra nibh cras pulvinar mattis. Urna duis convallis convallis tellus id interdum velit laoreet id. Morbi tincidunt augue interdum velit euismod. Faucibus interdum posuere lorem ipsum dolor sit amet consectetur adipiscing. Id aliquet lectus proin nibh nisl condimentum. Amet volutpat consequat mauris nunc congue. Interdum consectetur libero id faucibus nisl. Sapien et ligula ullamcorper malesuada proin libero. Cras ornare arcu dui vivamus arcu felis bibendum ut."
        main_content.text = content_text

    EventBroker.subscribe(
        event=MouseEventTypes.MOUSE_LEFT_CLICK,
        subscriber=content,
        pre_composition=_content
    )

    def _login_page(event):
        while len(body.children) > 0:
            body.children.pop(0)

        body.set_style("display", "block")
        body.children.append(auth)
        body.children.append(submit)

    EventBroker.subscribe(
        event=MouseEventTypes.MOUSE_LEFT_CLICK,
        subscriber=header.children.get_by_id("login-btn"),
        pre_composition=_login_page
    )

    def _username(event):
        auth._focus = False
        username_inp._focus = True

    EventBroker.subscribe(
        event=MouseEventTypes.MOUSE_LEFT_CLICK,
        subscriber=auth,
        pre_composition=_username
    )

    def _login_submit(event):
        while len(body.children) > 0:
            body.children.pop(0)

        name = username_inp.text
        body.set_style("display", "inline")
        body.append_child(sidebar)
        body.append_child(main)
        _home(None)

        login_username: Label = header.children.get_by_id("hdr-empty").children.get_by_id("login-username")
        login_username.clear()
        login_username.text = f" [ {name} ] "

    EventBroker.subscribe(
        event=MouseEventTypes.MOUSE_LEFT_CLICK,
        subscriber=submit,
        pre_composition=_login_submit
    )

    def _exit(event):
        print(f"\x1b[{app.root.area.rows-2};{0}f Exiting...")
        exit()

    EventBroker.subscribe(
        event=MouseEventTypes.MOUSE_LEFT_CLICK,
        subscriber=header.children.get_by_id("exit-btn"),
        pre_composition=_exit
    )

    app.run()

if __name__ == "__main__":
    main()
