import warnings

from toga.handlers import wrapped_handler

from .base import Widget


class TextEditor(Widget):
    """ A text editor widget

    Args:
        id (str): An identifier for this widget.
        style(:obj:`Style`):  An optional style object.
            If no style is provided then a new one will be created for the widget.
        factory: Optional factory that must be able to return a implementation
            of a TextEditor Widget.
        value (str): The initial text of the widget.
        readonly (bool): Whether a user can write into the text input,
            defaults to `False`.
        placeholder (str): The placeholder text for the widget.
        on_change (``callable``): The handler to invoke when the text changes.
        linenumbers (bool): Whether line numbers should be shown,
            defaults to `True`
    """
    MIN_HEIGHT = 100
    MIN_WIDTH = 100

    def __init__(
        self,
        id=None,
        style=None,
        factory=None,
        value=None,
        readonly=False,
        placeholder=None,
        on_change=None,
        linenumbers=True
    ):
        super().__init__(id=id, style=style, factory=factory)
        self.linenumbers = linenumbers  # this must be set before calling the factory

        # Create a platform specific implementation of a TextEditor
        self._impl = self.factory.TextEditor(interface=self)

        # Set all the properties
        # Set the initial value before on_change because we do not want it
        # to trigger on_change
        self.value = value
        self.readonly = readonly
        self.placeholder = placeholder
        self.on_change = on_change

    @property
    def placeholder(self):
        """ The placeholder text

        Returns:
            The placeholder text as a `str``.
        """
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = '' if value is None else str(value)
        self._impl.set_placeholder(self._placeholder)

    @property
    def readonly(self):
        """ Whether a user can write into the editor

        Returns:
            `True` if the user can only read, `False` if the user can read and write the text.
        """
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.set_readonly(value)

    @property
    def value(self):
        """ The value of the editor's text

        Returns:
            The text of the editor as a ``str``.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        cleaned_value = '' if value is None else str(value)
        self._impl.set_value(cleaned_value)
        self._impl.rehint()

    def clear(self):
        """ Clears the text from the editor
        """
        self.value = ''

    @property
    def on_change(self):
        """The handler to invoke when the value changes

        Returns:
            The function ``callable`` that is called on a content change.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        """Set the handler to invoke when the value is changed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the value is changed.
        """
        self._on_change = wrapped_handler(self, handler)
        self._impl.set_on_change(self._on_change)
