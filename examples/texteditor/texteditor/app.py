import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleTextEditorApp(toga.App):
    # Button callback functions
    def enable_toggle_pressed(self, widget, **kwargs):
        self.texteditor.enabled = not self.texteditor.enabled

    def readonly_toggle_pressed(self, widget, **kwargs):
        self.texteditor.readonly = not self.texteditor.readonly

    def add_content_pressed(self, widget, **kwargs):
        self.texteditor.value = "All work and no play makes Jack a dull boy... " * 100

    def clear_pressed(self, widget, **kwargs):
        self.texteditor.clear()

    def set_label(self, widget):
        if self.texteditor.value == "":
            self.label.text = "Nothing has been written yet"
            return
        number_of_lines = len(self.texteditor.value.split("\n"))
        self.label.text = "{} lines has been written".format(number_of_lines)

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        self.texteditor = toga.TextEditor(
            placeholder='Enter text here...',
            value='Initial value',
            style=Pack(flex=1, font_family='monospace', font_size=14),
            on_change=self.set_label
        )

        button_toggle_enabled = toga.Button(
            'Toggle enabled',
            on_press=self.enable_toggle_pressed,
            style=Pack(flex=1)
        )
        button_toggle_readonly = toga.Button(
            'Toggle readonly',
            on_press=self.readonly_toggle_pressed,
            style=Pack(flex=1)
        )
        button_add_content = toga.Button(
            'Add content',
            on_press=self.add_content_pressed,
            style=Pack(flex=1)
        )
        button_clear = toga.Button(
            'Clear',
            on_press=self.clear_pressed,
            style=Pack(flex=1)
        )
        btn_box = toga.Box(
            children=[
                button_toggle_enabled,
                button_toggle_readonly,
                button_add_content,
                button_clear,
            ],
            style=Pack(
                direction=ROW,
                padding=10
            )
        )
        self.label = toga.Label("Nothing has been written yet")

        outer_box = toga.Box(
            children=[btn_box, self.texteditor, self.label],
            style=Pack(
                direction=COLUMN,
                padding=10
            )
        )

        self.main_window.content = outer_box
        self.main_window.show()


def main():
    return ExampleTextEditorApp('TextEditor', 'org.beeware.widgets.texteditor')


if __name__ == '__main__':
    app = main()
    app.main_loop()
