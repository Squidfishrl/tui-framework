from tui.app import App
from tui.components.division import Division
from tui.components.label import Label

app = App()

app.root.set_style("padding", 25)
new_root = Division(style=f"rows={app.root.area.rows}, columns={app.root.area.columns}, padding=25")
new_root.append_child(
        Label("Hello, World!", style="rows=1, columns=13")
)
app.root = new_root

app.run()

