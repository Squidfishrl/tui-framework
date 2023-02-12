"""Demo for an application's layout using only containers with fixed size
Last update: v0.10.0
"""

from tui.app import App
from tui.components.division import Division
from tui.styles.border import DefaultBorder

def main():
    app = App(rows=50, columns=72)
    app.root = Division(style="rows=50, columns=72, padding=1, padding_top=0,\
            padding_bottom=0")
    app.root.add_border(DefaultBorder)

    # header
    header = Division(style="rows=5, columns=68, inline=True")
    header.add_border(DefaultBorder)
    app.root.append_child(header)

    # back button
    hdiv1 = Division(style="rows=3, columns=6, padding_left=1,\
            padding_right=1, margin_left=1")
    hdiv1.add_border(DefaultBorder)
    hdiv1.area.add_chars("<")
    header.append_child(hdiv1)

    # take up empty space
    hdiv_space = Division(style="columns=37")
    header.append_child(hdiv_space)

    # login btn
    hdiv2 = Division(style="rows=3, columns=10, padding_left=1,\
            padding_right=1, margin_right=1")
    hdiv2.add_border(DefaultBorder)
    hdiv2.area.add_chars("login")
    header.append_child(hdiv2)

    # register button
    hdiv3 = Division(style="rows=3, columns=12, padding_left=1,\
            padding_right=1")
    hdiv3.add_border(DefaultBorder)
    hdiv3.area.add_chars("register")
    header.append_child(hdiv3)

    
    # body
    body = Division(style="rows=43, columns=68, inline=True")

    # sidebar
    sidebar = Division(style="rows=43, columns=15, padding=1")
    sidebar.add_border(DefaultBorder)

    text1 = Division(style="rows=3, columns=11, padding_left=2")
    text1.add_border(DefaultBorder)
    text1.area.add_chars("About")

    text2 = Division(style="rows=3, columns=11, padding_left=1")
    text2.add_border(DefaultBorder)
    text2.area.add_chars("Content")

    # main
    main = Division(style="rows=43, columns=53, margin=2, padding_left=1,\
            padding_right=1")
    main.add_border(DefaultBorder)
    main.area.add_chars("Hello world!")

    app.root.append_child(body)
    body.append_child(sidebar)
    body.append_child(main)
    sidebar.append_child(text1)
    sidebar.append_child(text2)

    app.run()


if __name__ == "__main__":
    main()
