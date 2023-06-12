import tkinter as _tk
import typing as _typing

from carbon.color import get_gray as _g
from carbon.utils import minmax_normalization as _norm


ROD_LEN = 200
ROD_THICK = 3

BUTTON_SIZE = 5

FONT_COLOR = '#fafbfa'

BUTTON_COLOR_LOCKED = _g(55)
BUTTON_COLOR_PRESSED = _g(125)
BUTTON_COLOR_HOVER = _g(105)
BUTTON_COLOR = _g(85)

BUTTON_BD_COLOR_LOCKED = _g(55)
BUTTON_BD_COLOR = _g(245)

SLIDER_COLOR_LOCKED = _g(45)
SLIDER_COLOR = _g(75)

TOLERANCE = 0.5  # if 0.01 -> 1% of the precision


class _Slider:

    page: _tk.Canvas = None
    @staticmethod
    def set_page(page: _tk.Canvas, /):
        _Slider.page = page

    page_focus = None
    @staticmethod
    def set_page_focus(page_focus: list[_typing.Any], /):
        _Slider.page_focus = page_focus

    sliders: dict[str, '_Slider'] = {}
    slider_tags: dict[str, list['_Slider']] = {}  # note that the horizontal and vertical sliders store the tags together

    def _release(self):
        if self.pressed:
            self.pressed = False
            self._redraw()
            _Slider.page_focus[0] = None

    @staticmethod
    def hover_listener():
        for slider in _Slider.sliders.values():
            slider._hover()

    @staticmethod
    def press_listener():
        for slider in _Slider.sliders.values():
            slider._press()

    @staticmethod
    def hold_listener():
        for slider in list(_Slider.sliders.values()):
            slider._hold()

    @staticmethod
    def release_listener():
        for slider in list(_Slider.sliders.values()):
            slider._release()

    def set_lock(self, locked: bool, /) -> None:
        if self.locked is not locked:
            self.locked = locked
            self._redraw()
    
    @staticmethod
    def set_lock_by_id(id: str, locked: bool, /) -> None:
        _Slider.sliders[id].set_lock(locked)

    @staticmethod
    def set_lock_by_tag(tag: str, locked: bool, /) -> None:
        for slider in _Slider.slider_tags[tag]:
            slider.set_lock(locked)
    
    @staticmethod
    def set_lock_all(locked: bool, /) -> None:
        for slider in _Slider.sliders.values():
            slider.set_lock(locked)

    def set_visibility(self, visible: bool, /) -> None:
        if self.visible is not visible:
            self.visible = visible
            self._redraw()
    
    @staticmethod
    def set_visibility_by_id(id: str, visible: bool, /) -> None:
        _Slider.sliders[id].set_visibility(visible)
    
    @staticmethod
    def set_visibility_by_tag(tag: str, visible: bool, /) -> None:
        for slider in _Slider.slider_tags[tag]:
            slider.set_visibility(visible)
    
    @staticmethod
    def set_visibility_all(visible: bool, /) -> None:
        for slider in _Slider.sliders.values():
            slider.set_visibility(visible)

    def set_value(self, value: int | None, /) -> None:
        """if `None` -> default value."""

        if value is None:
            value = self.init

        if value < self.min:
            value = self.min
        if value > self.max:
            value = self.max

        if value != self.value:
            self.value = value
            self._redraw()
    
    @staticmethod
    def set_value_by_id(id: str, value: int | None, /) -> None:
        _Slider.sliders[id].set_value(value)

    @staticmethod
    def set_value_by_tag(tag: str, value: int | None, /) -> None:
        for slider in _Slider.slider_tags[tag]:
            slider.set_value(value)

    @staticmethod
    def set_value_all(value: int | None, /) -> None:
        for slider in _Slider.sliders.values():
            slider.set_value(value)

    @staticmethod
    def get_value_by_id(id: str, /) -> None:
        return _Slider.sliders[id].value


    def destroy(self) -> None:
        _Slider.sliders.pop(self.id)

        if self.tags is not None:
            for tag in self.tags:
                _Slider.slider_tags[tag].remove(self)
                if _Slider.slider_tags[tag] == []:
                    _Slider.slider_tags.pop(tag)

        _Slider.page.delete(f'slider_{self.id}')
    
    @staticmethod
    def destroy_by_tag(tag: str, /) -> None:

        if tag not in _Slider.slider_tags:
            return

        for slider in list(_Slider.slider_tags[tag]):
            slider.destroy()

    @staticmethod
    def destroy_all() -> None:
        for slider in list(_Slider.sliders.values()):
            slider.destroy()


class Slider(_Slider):

    def __init__(
        self,
        id: str,
        min: float,
        max: float,
        step: float,
        init: float,
        x: int,
        y: int,
        fn: _typing.Optional[_typing.Callable[[], None]] = None,
        label: _typing.Optional[str] = None,
        show_value: bool = True,
        prefix: str = '',
        suffix: str = '',
        show_label_box: bool = False,
        label_box_color: _typing.Optional[str] = None,
        label_box_width: _typing.Optional[int] = None,
        label_box_height: _typing.Optional[int] = None,
        label_y_shift: int = -15,
        show_yield_box: bool = False,
        yield_box_color: _typing.Optional[str] = None,
        yield_box_width: _typing.Optional[int] = None,
        yield_box_height: _typing.Optional[int] = None,
        yield_x_shift: int = 15,
        locked: bool = False,
        visible: bool = True,
        tags: str | list[str] | tuple[str, ...] | None = None,
    ) -> None:
        """box color, width, and height must be provided if the box shown."""

        self.id = id
        if id in self.sliders:
            raise ValueError(f'The id {repr(id)} is not available.')
        self.sliders[id] = self

        self.min = min
        self.max = max
        self.step = step
        self.init = init
        self.x = x
        self.y = y
        self.fn = fn
        self.label = label
        self.show_value = show_value
        self.prefix = prefix
        self.suffix = suffix
        self.show_label_box = show_label_box
        self.label_box_color = label_box_color
        self.label_box_width = label_box_width
        self.label_box_height = label_box_height
        self.label_y_shift = label_y_shift
        self.show_yield_box = show_yield_box
        self.yield_box_color = yield_box_color
        self.yield_box_width = yield_box_width
        self.yield_box_height = yield_box_height
        self.yield_x_shift = yield_x_shift
        self.locked = locked
        self.visible = visible

        self.value = init
        self.prec = len(str(abs(step)).split('.')[1]) if '.' in str(step) else 0
        self.pressed = False
        self.hovered = False

        ## <tags>
        if type(tags) is str:
            self.tags = [tags]
        elif (type(tags) is list) or (type(tags) is tuple) or (tags is None):
            self.tags = tags
        
        if tags is not None:
            for tag in self.tags:
                if tag in _Slider.slider_tags:
                    _Slider.slider_tags[tag].append(self)
                else:
                    _Slider.slider_tags[tag] = [self]
        ## </tags>
        
        self._redraw()

    def _redraw(self):

        if self.locked:
            slider_color = SLIDER_COLOR_LOCKED
            button_color = BUTTON_COLOR_LOCKED
            button_bd_color = BUTTON_BD_COLOR_LOCKED
        elif self.pressed:
            slider_color = SLIDER_COLOR
            button_color = BUTTON_COLOR_PRESSED
            button_bd_color = BUTTON_BD_COLOR
        elif self.hovered:
            slider_color = SLIDER_COLOR
            button_color = BUTTON_COLOR_HOVER
            button_bd_color = BUTTON_BD_COLOR
        else:
            slider_color = SLIDER_COLOR
            button_color = BUTTON_COLOR
            button_bd_color = BUTTON_BD_COLOR

        self.page.delete(f'slider_{self.id}')

        if self.visible:

            self.page.create_rectangle(
                self.x - ROD_LEN/2, self.y - ROD_THICK/2,
                self.x + ROD_LEN/2, self.y + ROD_THICK/2,
                fill=slider_color, width=0, tags=f'slider_{self.id}'
            )
            self.page.create_oval(
                self.x - ROD_LEN/2 + _norm(self.value, self.min, self.max)*ROD_LEN - BUTTON_SIZE, self.y - BUTTON_SIZE,
                self.x - ROD_LEN/2 + _norm(self.value, self.min, self.max)*ROD_LEN + BUTTON_SIZE, self.y + BUTTON_SIZE,
                fill=button_color, width=1, outline=button_bd_color, tags=f'slider_{self.id}'
            )

            if self.show_label_box:
                self.page.create_rectangle(
                    self.x - self.label_box_width/2, self.y - ROD_THICK/2 + self.label_y_shift - self.label_box_height/2,
                    self.x + self.label_box_width/2, self.y - ROD_THICK/2 + self.label_y_shift + self.label_box_height/2,
                    fill=self.label_box_color, width=0, tags=f'slider_{self.id}'
                )
            if self.label is not None:
                self.page.create_text(
                    self.x, self.y - ROD_THICK/2 + self.label_y_shift,
                    text=self.label, font=('Arial Bold', 9), fill=FONT_COLOR, tags=f'slider_{self.id}'
                )

            if self.show_yield_box:
                self.page.create_rectangle(
                    self.x + ROD_LEN/2 + self.yield_x_shift - self.yield_box_width/2, self.y - self.yield_box_height/2,
                    self.x + ROD_LEN/2 + self.yield_x_shift + self.yield_box_width/2, self.y + self.yield_box_height/2,
                    fill=self.yield_box_color, width=0, tags=f'slider_{self.id}'
                )
            if self.show_value:
                self.page.create_text(
                    self.x + ROD_LEN/2 + self.yield_x_shift, self.y,
                    text=self.prefix + str(self.value) + self.suffix,
                    font='Consolas 10', fill=FONT_COLOR, tags=f'slider_{self.id}'
                )

    def _hover(self):

        mousex = self.page.winfo_pointerx()
        mousey = self.page.winfo_pointery()

        buttonx = self.x - ROD_LEN/2 + _norm(self.value, self.min, self.max)*ROD_LEN
        buttony = self.y

        if (
            (buttonx - BUTTON_SIZE <= mousex <= buttonx + BUTTON_SIZE)
            and
            (buttony - BUTTON_SIZE <= mousey <= buttony + BUTTON_SIZE)
            and
            (not self.locked)
            and
            (self.visible)
            and
            (not self.hovered)
        ):
            self.hovered = True
            self._redraw()
        elif (
            (self.hovered)
            and
            (not ((buttonx - BUTTON_SIZE <= mousex <= buttonx + BUTTON_SIZE) and (buttony - BUTTON_SIZE <= mousey <= buttony + BUTTON_SIZE)))
        ):
            self.hovered = False
            self._redraw()

    def _press(self):

        mousex = self.page.winfo_pointerx()
        mousey = self.page.winfo_pointery()

        buttonx = self.x - ROD_LEN/2 + _norm(self.value, self.min, self.max)*ROD_LEN
        buttony = self.y

        if (
            (buttonx - BUTTON_SIZE <= mousex <= buttonx + BUTTON_SIZE)
            and
            (buttony - BUTTON_SIZE <= mousey <= buttony + BUTTON_SIZE)
            and
            (not self.locked)
            and
            (self.visible)
        ):
            self.pressed = True
            self._redraw()
            self.page_focus[0] = self

    def _hold(self):

        if self.pressed:

            mousex = self.page.winfo_pointerx()
            value = self.min + ((mousex - (self.x - ROD_LEN/2))/ROD_LEN)*(self.max - self.min)

            if self.prec == 0:
                value = int(value)
            else:
                value = round(value, self.prec)

            if abs(value - round(value/self.step)*self.step) < TOLERANCE*self.step:

                if value < self.min:
                    value = self.min
                if value > self.max:
                    value = self.max
                
                if value == self.value:
                    return
                self.value = value

                self._redraw()
                if self.fn is not None:
                    self.fn()


class VSlider(_Slider):

    def __init__(
        self,
        id: str,
        min: float,
        max: float,
        step: float,
        init: float,
        x: int,
        y: int,
        fn: _typing.Optional[_typing.Callable[[], None]] = None,
        label: _typing.Optional[str] = None,
        show_value: bool = True,
        prefix: str = '',
        suffix: str = '',
        show_label_box: bool = False,
        label_box_color: _typing.Optional[str] = None,
        label_box_width: _typing.Optional[int] = None,
        label_box_height: _typing.Optional[int] = None,
        label_y_shift: int = -15,
        show_yield_box: bool = False,
        yield_box_color: _typing.Optional[str] = None,
        yield_box_width: _typing.Optional[int] = None,
        yield_box_height: _typing.Optional[int] = None,
        yield_y_shift: int = 15,
        locked: bool = False,
        visible: bool = True,
        tags: str | list[str] | tuple[str, ...] | None = None,
    ) -> None:
        """box color, width, and height must be provided if the box shown."""

        self.id = id
        if id in self.sliders:
            raise ValueError(f'The id {repr(id)} is not available.')
        self.sliders[id] = self

        self.min = min
        self.max = max
        self.step = step
        self.init = init
        self.x = x
        self.y = y
        self.fn = fn
        self.label = label
        self.show_value = show_value
        self.prefix = prefix
        self.suffix = suffix
        self.show_label_box = show_label_box
        self.label_box_color = label_box_color
        self.label_box_width = label_box_width
        self.label_box_height = label_box_height
        self.label_y_shift = label_y_shift
        self.show_yield_box = show_yield_box
        self.yield_box_color = yield_box_color
        self.yield_box_width = yield_box_width
        self.yield_box_height = yield_box_height
        self.yield_y_shift = yield_y_shift
        self.locked = locked
        self.visible = visible

        self.value = init
        self.prec = len(str(abs(step)).split('.')[1]) if '.' in str(step) else 0
        self.pressed = False
        self.hovered = False

        ## <tags>
        if type(tags) is str:
            self.tags = [tags]
        elif (type(tags) is list) or (type(tags) is tuple) or (tags is None):
            self.tags = tags
        
        if tags is not None:
            for tag in self.tags:
                if tag in _Slider.slider_tags:
                    _Slider.slider_tags[tag].append(self)
                else:
                    _Slider.slider_tags[tag] = [self]
        ## </tags>

        self._redraw()

    def _redraw(self):

        if self.locked:
            slider_color = SLIDER_COLOR_LOCKED
            button_color = BUTTON_COLOR_LOCKED
            button_bd_color = BUTTON_BD_COLOR_LOCKED
        elif self.pressed:
            slider_color = SLIDER_COLOR
            button_color = BUTTON_COLOR_PRESSED
            button_bd_color = BUTTON_BD_COLOR
        elif self.hovered:
            slider_color = SLIDER_COLOR
            button_color = BUTTON_COLOR_HOVER
            button_bd_color = BUTTON_BD_COLOR
        else:
            slider_color = SLIDER_COLOR
            button_color = BUTTON_COLOR
            button_bd_color = BUTTON_BD_COLOR

        self.page.delete(f'slider_{self.id}')

        if self.visible:

            self.page.create_rectangle(
                self.x - ROD_THICK/2, self.y - ROD_LEN/2,
                self.x + ROD_THICK/2, self.y + ROD_LEN/2,
                fill=slider_color, width=0, tags=f'slider_{self.id}'
            )
            self.page.create_oval(
                self.x - BUTTON_SIZE, self.y + ROD_LEN/2 - _norm(self.value, self.min, self.max)*ROD_LEN - BUTTON_SIZE,
                self.x + BUTTON_SIZE, self.y + ROD_LEN/2 - _norm(self.value, self.min, self.max)*ROD_LEN + BUTTON_SIZE,
                fill=button_color, width=1, outline=button_bd_color, tags=f'slider_{self.id}'
            )

            if self.show_label_box:
                self.page.create_rectangle(
                    self.x - self.label_box_width/2, self.y - ROD_LEN/2 + self.label_y_shift - self.label_box_height/2,
                    self.x + self.label_box_width/2, self.y - ROD_LEN/2 + self.label_y_shift + self.label_box_height/2,
                    fill=self.label_box_color, width=0, tags=f'slider_{self.id}'
                )
            if self.label is not None:
                self.page.create_text(
                    self.x, self.y - ROD_LEN/2 + self.label_y_shift,
                    text=self.label, font=('Arial Bold', 9), fill=FONT_COLOR, tags=f'slider_{self.id}'
                )

            if self.show_yield_box:
                self.page.create_rectangle(
                    self.x - self.yield_box_width/2, self.y + ROD_LEN/2 + self.yield_y_shift - self.yield_box_height/2,
                    self.x + self.yield_box_width/2, self.y + ROD_LEN/2 + self.yield_y_shift + self.yield_box_height/2,
                    fill=self.yield_box_color, width=0, tags=f'slider_{self.id}'
                )
            if self.show_value:
                self.page.create_text(
                    self.x, self.y + ROD_LEN/2 + self.yield_y_shift,
                    text=self.prefix + str(self.value) + self.suffix,
                    font='Consolas 10', fill=FONT_COLOR, tags=f'slider_{self.id}'
                )

    def _hover(self):

        mousex = self.page.winfo_pointerx()
        mousey = self.page.winfo_pointery()

        buttonx = self.x
        buttony = self.y + ROD_LEN/2 - _norm(self.value, self.min, self.max)*ROD_LEN

        if (
            (buttonx - BUTTON_SIZE <= mousex <= buttonx + BUTTON_SIZE)
            and
            (buttony - BUTTON_SIZE <= mousey <= buttony + BUTTON_SIZE)
            and
            (not self.locked)
            and
            (self.visible)
            and
            (not self.hovered)
        ):
            self.hovered = True
            self._redraw()
        elif (
            (self.hovered)
            and
            (not ((buttonx - BUTTON_SIZE <= mousex <= buttonx + BUTTON_SIZE) and (buttony - BUTTON_SIZE <= mousey <= buttony + BUTTON_SIZE)))
        ):
            self.hovered = False
            self._redraw()

    def _press(self):

        mousex = self.page.winfo_pointerx()
        mousey = self.page.winfo_pointery()

        buttonx = self.x
        buttony = self.y + ROD_LEN/2 - _norm(self.value, self.min, self.max)*ROD_LEN

        if (
            (buttonx - BUTTON_SIZE <= mousex <= buttonx + BUTTON_SIZE)
            and
            (buttony - BUTTON_SIZE <= mousey <= buttony + BUTTON_SIZE)
            and
            (not self.locked)
            and
            (self.visible)
        ):
            self.pressed = True
            self._redraw()
            self.page_focus[0] = self

    def _hold(self):

        if self.pressed:

            mousey = self.page.winfo_pointery()
            value = self.max - ((mousey - (self.y - ROD_LEN/2))/ROD_LEN)*(self.max - self.min)
            value = round(value, self.prec)

            if abs(value - round(value/self.step)*self.step) < TOLERANCE*self.step:

                if value < self.min:
                    value = self.min
                if value > self.max:
                    value = self.max
                
                if value == self.value:
                    return
                self.value = value
                
                self._redraw()
                if self.fn is not None:
                    self.fn()