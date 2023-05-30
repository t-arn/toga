from ..libs.android.text import InputType
from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        super().create(
            input_type=(
                InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD
            )
        )
