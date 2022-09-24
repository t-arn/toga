from toga.constants import LEFT
from travertino.size import at_least

from toga_android.colors import native_color

from ..libs.android.graphics import Typeface
from ..libs.android.text import InputType, TextWatcher
from ..libs.android.util import TypedValue
from ..libs.android.view import Gravity
from ..libs.android.widget import (
    EditText,
    HorizontalScrollView,
    LinearLayout,
    LinearLayout__LayoutParams,
    ScrollView
)
from .base import Widget, align


class TogaTextWatcher(TextWatcher):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.interface = impl.interface

    def beforeTextChanged(self, _charSequence, _start, _count, _after):
        pass

    def afterTextChanged(self, _editable):
        if self.interface.linenumbers:
            self.impl.generate_linenumbers()
        if self.interface.on_change:
            self.interface.on_change(widget=self.interface)

    def onTextChanged(self, _charSequence, _start, _before, _count):
        pass


class TextEditor(Widget):
    def create(self):
        self._et_numbers = None
        self._prev_linecount = -1
        self._et_text = None
        self._textChangedListener = None
        self.native = LinearLayout(self._native_activity)
        self.native.setOrientation(LinearLayout.VERTICAL)
        mm_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT
        )  # width, height
        mw_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.WRAP_CONTENT
        )  # width, height
        self.native.setLayoutParams(mm_params)
        vsv = ScrollView(self._native_activity)
        vsv.setFillViewport(True)
        vsv.setLayoutParams(mm_params)
        ll_editor = LinearLayout(self._native_activity)
        vsv.addView(ll_editor)
        if self.interface.linenumbers:
            self._et_numbers = EditText(self._native_activity)
            self.set_alignment(self._et_numbers, RIGHT)
            self._et_numbers.setTypeface(Typeface.MONOSPACE)
            self._et_numbers.setText("1")
            self._et_numbers.setEnabled(False)
            ll_editor.addView(self._et_numbers)
        hsv = HorizontalScrollView(self._native_activity)
        hsv.setLayoutParams(mw_params)
        hsv.setFillViewport(True)
        ll_editor.addView(hsv)
        self._et_text = EditText(self._native_activity)
        self.set_alignment(self._et_text, LEFT)
        self._et_text.setTypeface(Typeface.MONOSPACE)
        self._et_text.setInputType(
            InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_MULTI_LINE
        )
        self._et_text.setText("")
        hsv.addView(self._et_text)
        self.native.addView(vsv)
        self._et_text.requestFocus()

    def generate_linenumbers(self):
        line_count = self._et_text.getLineCount()
        if line_count != self._prev_linecount:
            lines = "1"
            for x in range(2, line_count + 1):
                lines += "\n" + str(x)
            self.set_value(lines)
            self._prev_linecount = line_count
    
    def get_value(self):
        return self._et_text.getText().toString()

    def set_readonly(self, value):
        self._et_text.setFocusable(not value)

    def set_placeholder(self, value):
        # Android EditText's setHint() requires a Python string.
        self._et_text.setHint(value if value is not None else "")

    def set_alignment(self, obj, value):
        # Refuse to set alignment unless widget has been added to a container.
        # This is because Android EditText requires LayoutParams before
        # setGravity() can be called.
        if not self.native.getLayoutParams():
            return
        obj.setGravity(Gravity.TOP | align(value))

    def set_color(self, color):
        if color:
            self._et_text.setTextColor(native_color(color))

    def set_font(self, font):
        if font:
            font_impl = font.bind(self.interface.factory)
            self._et_text.setTextSize(TypedValue.COMPLEX_UNIT_SP, font_impl.get_size())
            self._et_text.setTypeface(font_impl.get_typeface(), font_impl.get_style())

    def set_value(self, value):
        self._et_text.setText(value)

    def set_on_change(self, handler):
        if self._textChangedListener:
            self._et_text.removeTextChangedListener(self._textChangedListener)
        self._textChangedListener = TogaTextWatcher(self)
        self._et_text.addTextChangedListener(self._textChangedListener)

    def rehint(self):
        # Android can crash when rendering some widgets until they have their layout params set. Guard for that case.
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED,
            View__MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
