from travertino.size import at_least

from ..libs.android import R__layout
from ..libs.android.view import Gravity, View__MeasureSpec
from ..libs.android.widget import (
    ArrayAdapter,
    OnItemSelectedListener,
    Spinner,
    SpinnerAdapter,
)
from .base import Widget, align


class TogaOnItemSelectedListener(OnItemSelectedListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onItemSelected(self, parent, view, position, id):
        self.impl.on_change(position)

    def onNothingSelected(self, parent):
        self.impl.on_change(None)


class TogaArrayAdapter(SpinnerAdapter):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl
        self.view_default_textsize = -1
        self.view_default_typeface = None
        self.dropdownview_default_textsize = -1
        self.dropdownview_default_typeface = None
        self.adapter = ArrayAdapter(
            self.impl._native_activity, R__layout.simple_spinner_item
        )
        self.adapter.setDropDownViewResource(R__layout.simple_spinner_dropdown_item)

    def cache_dropdowntextview_defaults(self, tv):
        self.dropdownview_default_textsize = tv.getTextSize()
        self.dropdownview_default_typeface = tv.getTypeface()

    def cache_textview_defaults(self, tv):
        self.view_default_textsize = tv.getTextSize()
        self.view_default_typeface = tv.getTypeface()

    def getDropDownView(self, position, convertView, parent):
        tv = self.adapter.getDropDownView(position, convertView, parent)
        if self.dropdownview_default_textsize == -1:
            self.cache_dropdowntextview_defaults(tv)
        if self.impl._font_impl:
            self.impl._font_impl.apply(
                tv,
                self.dropdownview_default_textsize,
                self.dropdownview_default_typeface,
            )
        return tv

    def getView(self, position, convertView, parent):
        tv = self.adapter.getView(position, convertView, parent)
        if self.view_default_textsize == -1:
            self.cache_textview_defaults(tv)
        if self.impl._font_impl:
            self.impl._font_impl.apply(
                tv, self.view_default_textsize, self.view_default_typeface
            )
        return tv

    def clear(self):
        return self.adapter.clear()

    def getAutofillOptions(self):
        return self.adapter.getAutofillOptions()

    def getCount(self):
        return self.adapter.getCount()

    def getItem(self, position):
        return self.adapter.getItem(position)

    def getItemId(self, position):
        return self.adapter.getItemId(position)

    def getItemViewType(self, position):
        return self.adapter.getItemViewType(position)

    def getViewTypeCount(self):
        return self.adapter.getViewTypeCount()

    def hasStableIds(self):
        return self.adapter.hasStableIds()

    def insert(self, object, index):
        return self.adapter.insert(object, index)

    def isEmpty(self):
        return self.adapter.isEmpty()

    def registerDataSetObserver(self, observer):
        self.adapter.registerDataSetObserver(observer)

    def remove(self, object):
        self.adapter.remove(object)

    def unregisterDataSetObserver(self, observer):
        self.adapter.unregisterDataSetObserver(observer)


class Selection(Widget):
    focusable = False
    _font_impl = None

    def create(self):
        self.native = Spinner(self._native_activity, Spinner.MODE_DROPDOWN)
        self.native.setOnItemSelectedListener(TogaOnItemSelectedListener(impl=self))
        self.adapter = TogaArrayAdapter(impl=self)
        self.native.setAdapter(self.adapter)
        self.last_selection = None

    # Programmatic selection changes do cause callbacks, but they may be delayed until a
    # later iteration of the main loop. So we always generate events immediately after
    # the change, and use self.last_selection to prevent duplication.
    def on_change(self, index):
        if index != self.last_selection:
            self.interface.on_change(None)
            self.last_selection = index

    def insert(self, index, item):
        self.adapter.insert(self.interface._title_for_item(item), index)
        if self.last_selection is None:
            self.select_item(0)
        elif index <= self.last_selection:
            # Adjust the selection index, but do not generate an event.
            self.last_selection += 1
            self.select_item(self.last_selection)

    def change(self, item):
        # Instead of calling self.insert and self.remove, use direct native calls to
        # avoid disturbing the selection.
        index = self.interface._items.index(item)
        self.adapter.insert(self.interface._title_for_item(item), index)
        self.adapter.remove(self.adapter.getItem(index + 1))

    def remove(self, index, item=None):
        self.adapter.remove(self.adapter.getItem(index))

        # Adjust the selection index, but only generate an event if the selected item
        # has been removed.
        removed_selection = self.last_selection == index
        if index <= self.last_selection:
            if self.adapter.getCount() == 0:
                self.last_selection = None
            else:
                self.last_selection = max(0, self.last_selection - 1)
                self.select_item(self.last_selection)

        if removed_selection:
            self.interface.on_change(None)

    def select_item(self, index, item=None):
        self.native.setSelection(index)
        self.on_change(index)

    def get_selected_index(self):
        selected = self.native.getSelectedItemPosition()
        return None if selected == Spinner.INVALID_POSITION else selected

    def clear(self):
        self.adapter.clear()
        self.on_change(None)

    def rehint(self):
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()

    def set_alignment(self, value):
        self.native.setGravity(Gravity.CENTER_VERTICAL | align(value))

    def set_font(self, font):
        self._font_impl = font._impl
