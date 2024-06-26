import asyncio
import sys

from textual.app import App as TextualApp
from toga.command import Command
from toga.handlers import simple_handler

from .screens import Screen as ScreenImpl


class TogaApp(TextualApp):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def on_mount(self) -> None:
        self.impl.create()


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.loop = asyncio.new_event_loop()
        self.native = TogaApp(self)

    def create(self):
        self.interface._startup()
        self.set_current_window(self.interface.main_window._impl)

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_app_commands(self):
        self.interface.commands.add(
            Command(
                simple_handler(self.interface.about),
                f"About {self.interface.formal_name}",
                section=sys.maxsize,
                id=Command.ABOUT,
            ),
        )

    def create_menus(self):
        self.interface.factory.not_implemented("App.create_menus()")

    ######################################################################
    # App lifecycle
    ######################################################################

    def exit(self):
        self.native.exit()

    def main_loop(self):
        self.native.run()

    def set_icon(self, icon):
        pass

    def set_main_window(self, window):
        self.native.push_screen(self.interface.main_window.id)

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        return [ScreenImpl(window._impl.native) for window in self.interface.windows]

    ######################################################################
    # App capabilities
    ######################################################################

    def beep(self):
        self.native.bell()

    def show_about_dialog(self):
        pass

    ######################################################################
    # Cursor control
    ######################################################################

    def show_cursor(self):
        pass

    def hide_cursor(self):
        pass

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        pass

    def set_current_window(self, window):
        self.native.switch_screen(window.native)
        self.native.title = window.get_title()

    ######################################################################
    # Full screen control
    ######################################################################

    def enter_full_screen(self, windows):
        pass

    def exit_full_screen(self, windows):
        pass


class DocumentApp(App):
    pass
