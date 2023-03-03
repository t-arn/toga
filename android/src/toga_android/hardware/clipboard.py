from ..libs.android.content import ClipboardManager as A_ClipboardManager
from ..libs.android.content import ClipData as A_ClipData
from ..libs.activity import MainActivity
from rubicon.java import __cast__


class Clipboard():
    clipboard_manager = None
    data_types = ("Text", "URI", "Intent")

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._native_activity = MainActivity.singletonThis
        clipboard = self._native_activity.getSystemService("clipboard")  # returns a java/lang/Object
        # cast the Object to ClipboardManager and assign it to self.clipboard_manager
        self.clipboard_manager = __cast__(A_ClipboardManager, clipboard, globalref=False)

    def clear(self):
        self.clipboard_manager.clearPrimaryClip()

    def get_text(self):
        if self.clipboard_manager.hasPrimaryClip():
            clip_data = self.clipboard_manager.getPrimaryClip()
            item = clip_data.getItemAt(0)
            if item.getText():
                return item.getText()
            else:
                return None
        else:
            return None

    def set_text(self, text):
        if text is None:
            self.clear()
        else:
            clip_data = A_ClipData.newPlainText(self.data_types[0], text)
            self.clipboard_manager.setPrimaryClip(clip_data)