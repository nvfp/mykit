import random as _random
import tkinter as _tk
from typing import (
    Callable as _Callable,
    Dict as _Dict,
    List as _List,
    Literal as _Literal,
    Optional as _Optional,
    Tuple as _Tuple,
    Union as _Union
)

from mykit.kit.utils import minmax_normalization as _norm


class _Slider:

    ## <runtime>

    _page: _tk.Canvas = None
    @staticmethod
    def _set_page(page):
        _Slider._page = page

    sliders: _Dict[str, '_Slider'] = {}
    slider_tags: _Dict[str, _List['_Slider']] = {}  # note that the horizontal and vertical sliders store the tags together

    ## </runtime>

    def __init__(
        self,
        min: float = 0,
        max: float = 1,
        step: _Optional[float] = None,
        init: _Optional[float] = None,
        fn: _Optional[_Callable[[], None]] = None,

        x: int = 0,
        y: int = 0,
        anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw',
        tolerance: float = 0.25,
        
        label: _Optional[str] = None,
        label_fg: str = '#ccc',
        label_font: _Union[str, _Tuple[str, int]] = 'Verdana 9',
        show_label_box: bool = False,
        label_box_color: _Optional[str] = None,
        label_box_width: _Optional[int] = None,
        label_box_height: _Optional[int] = None,
        label_y_shift: int = -15,

        show_value: bool = True,
        value_fg: str = '#ccc',
        value_font: _Union[str, _Tuple[str, int]] = 'Consolas 9',
        value_prefix: str = '',
        value_suffix: str = '',
        show_value_box: bool = False,
        value_box_color: _Optional[str] = None,
        value_box_width: _Optional[int] = None,
        value_box_height: _Optional[int] = None,

        rod_len: int = 200,
        rod_thick: int = 3,
        btn_r: int = 5,
        color_rod_normal: str = '#4b4b4b',
        color_rod_locked: str = '#2d2d2d',
        color_btn_normal: str = '#555555',
        color_btn_locked: str = '#373737',
        color_btn_press: str = '#7d7d7d',
        color_btn_hover: str = '#696969',
        color_btn_bd_normal: str = '#f5f5f5',
        color_btn_bd_locked: str = '#373737',

        locked: bool = False,
        visible: bool = True,

        id: _Optional[str] = None,
        tags: _Optional[_Union[str, _List[str]]] = None,
    ) -> None:
        """
        ## Params
        - `x` and `y` is the position of the `anchor` (not the center of the button)
        - `tolerance`: to determine how closely the cursor needs to be to the slider's step values for it to move to a new value

        ## Docs
        - box color, width, and height should be provided if the box shown
        """

        ## <dependencies check>

        if _Slider._page is None:
            raise AssertionError('Can\'t use widgets before App initialized.')
        
        ## </dependencies check>

        self.min = min
        self.max = max
        self.step = step if step is not None else (max-min)/10
        self.init = init if init is not None else (max-min)/2
        self.fn = fn

        self.x = x
        self.y = y
        self.anchor = anchor
        self.tolerance = tolerance

        self.label = label
        self.label_fg = label_fg
        self.label_font = label_font
        self.show_label_box = show_label_box
        self.label_box_color = label_box_color
        self.label_box_width = label_box_width
        self.label_box_height = label_box_height
        self.label_y_shift = label_y_shift

        self.show_value = show_value
        self.value_fg = value_fg
        self.value_font = value_font
        self.value_prefix = value_prefix
        self.value_suffix = value_suffix
        self.show_value_box = show_value_box
        self.value_box_color = value_box_color
        self.value_box_width = value_box_width
        self.value_box_height = value_box_height

        self.rod_len = rod_len
        self.rod_thick = rod_thick
        self.btn_r = btn_r
        self.color_rod_normal = color_rod_normal
        self.color_rod_locked = color_rod_locked
        self.color_btn_normal = color_btn_normal
        self.color_btn_locked = color_btn_locked
        self.color_btn_press = color_btn_press
        self.color_btn_hover = color_btn_hover
        self.color_btn_bd_normal = color_btn_bd_normal
        self.color_btn_bd_locked = color_btn_bd_locked

        self.locked = locked
        self.visible = visible

        ## <id>

        ## self.id ensures that we can modify a specific instance without affecting the others
        if id is None:
            self.id = str(_random.randint(0, 100_000))
            while self.id in _Slider.sliders:
                self.id = str(_random.randint(0, 100_000))
        else:
            self.id = id
            if self.id in _Slider.sliders:
                raise ValueError(f'The id {repr(id)} is duplicated.')
        
        _Slider.sliders[self.id] = self

        ## </id>


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


        ## runtime

        self.value = self.init
        self.prec = len(str(abs(self.step)).split('.')[1]) if '.' in str(self.step) else 0
        self.pressed = False
        self.hovered = False


    @staticmethod
    def _hover_listener():  # reminder: hover listeners don't need `e: _tk.Event` arg
        for slider in _Slider.sliders.values():
            slider._hover()

    @staticmethod
    def _press_listener(e: _tk.Event):
        for slider in _Slider.sliders.values():
            slider._press()

    @staticmethod
    def _hold_listener(e: _tk.Event):
        for slider in list(_Slider.sliders.values()):
            slider._hold()
    

    def _release(self):
        if self.pressed:
            self.pressed = False
            self._redraw()

    @staticmethod
    def _release_listener(e: _tk.Event):
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


    def set_value(self, value: _Optional[int], /) -> None:
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
    def set_value_by_id(id: str, value: _Optional[int], /) -> None:
        _Slider.sliders[id].set_value(value)

    @staticmethod
    def set_value_by_tag(tag: str, value: _Optional[int], /) -> None:
        for slider in _Slider.slider_tags[tag]:
            slider.set_value(value)

    @staticmethod
    def set_value_all(value: _Optional[int], /) -> None:
        """To reset the value of all sliders, use `value = None`."""
        for slider in _Slider.sliders.values():
            slider.set_value(value)


    @staticmethod
    def get_value_by_id(id: str, /) -> None:
        return _Slider.sliders[id].value
    

    def get_anchor_loc(
        self,
        anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'],
        /
    ) -> _Tuple[int, int]:
        """To get the slider-rod's center coordinate, use `anchor='center'`"""

        W = self.width
        H = self.height

        ## get the coordinates for the center (X, Y)
        if self.anchor == 'center':
            X = self.x
            Y = self.y
        elif self.anchor == 'n':
            X = self.x
            Y = self.y + H/2
        elif self.anchor == 'ne':
            X = self.x - W/2
            Y = self.y + H/2
        elif self.anchor == 'e':
            X = self.x - W/2
            Y = self.y
        elif self.anchor == 'se':
            X = self.x - W/2
            Y = self.y - H/2
        elif self.anchor == 's':
            X = self.x
            Y = self.y - H/2
        elif self.anchor == 'sw':
            X = self.x + W/2
            Y = self.y - H/2
        elif self.anchor == 'w':
            X = self.x + W/2
            Y = self.y
        elif self.anchor == 'nw':
            X = self.x + W/2
            Y = self.y + H/2

        ## returning the requested anchor location
        if anchor == 'center':
            return (X, Y)
        elif anchor == 'n':
            return (X, Y-H/2)
        elif anchor == 'ne':
            return (X+W/2, Y-H/2)
        elif anchor == 'e':
            return (X+W/2, Y)
        elif anchor == 'se':
            return (X+W/2, Y+H/2)
        elif anchor == 's':
            return (X, Y+H/2)
        elif anchor == 'sw':
            return (X-W/2, Y+H/2)
        elif anchor == 'w':
            return (X-W/2, Y)
        elif anchor == 'nw':
            return (X-W/2, Y-H/2)
        else:
            raise ValueError(f'Invalid anchor value: {repr(anchor)}')

    @staticmethod
    def get_anchor_loc_by_id(
        id: str,
        anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'],
        /
    ) -> _Tuple[int, int]:
        return _Slider.sliders[id].get_anchor_loc(anchor)


    def move(
        self,
        x: int,
        y: int,
        /,
        anchor: _Optional[_Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']] = None
    ) -> '_Slider':
        """If `anchor = None`, the current anchor will be used."""
        self.x = x
        self.y = y
        if anchor is not None:
            self.anchor = anchor
        self._redraw()
        return self

    @staticmethod
    def move_by_id(
        id: str,
        x: int,
        y: int,
        /,
        anchor: _Optional[_Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']] = None
    ) -> None:
        _Slider.sliders[id].move(x, y, anchor)


    def align(
        self,
        target: '_Slider',
        anchor: str = 'nw',
        target_anchor: str = 'ne',
        xgap: float = 15,
        ygap: float = 0
    ) -> '_Slider':
        """
        Valid options for `anchor` and `target_anchor` are `['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']`.
        """

        ## getting the target anchor location
        x, y = target.get_anchor_loc(target_anchor)

        ## shifting
        x += xgap
        y += ygap

        ## moving the label
        self.move(x, y, anchor)

        ## return the instance so that this method can also be used when
        ## creating the instance, like `sld_2 = Slider().align(sld_1)`.
        return self


    def destroy(self) -> None:
        _Slider.sliders.pop(self.id)

        if self.tags is not None:
            for tag in self.tags:
                _Slider.slider_tags[tag].remove(self)
                if _Slider.slider_tags[tag] == []:
                    _Slider.slider_tags.pop(tag)

        _Slider._page.delete(f'Slider_{self.id}')

    @staticmethod
    def destroy_by_id(id: str, /) -> None:
        _Slider.sliders[id].destroy()

    @staticmethod
    def destroy_by_tag(tag: str, /) -> None:
        for slider in list(_Slider.slider_tags[tag]):
            slider.destroy()

    @staticmethod
    def destroy_all() -> None:
        for slider in list(_Slider.sliders.values()):
            slider.destroy()


class Slider(_Slider):

    def __init__(
        self,
        min: float = 0,
        max: float = 1,
        step: _Optional[float] = None,
        init: _Optional[float] = None,
        fn: _Optional[_Callable[[], None]] = None,

        x: int = 0,
        y: int = 0,
        anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw',
        tolerance: float = 0.25,
        
        label: _Optional[str] = None,
        label_fg: str = '#ccc',
        label_font: _Union[str, _Tuple[str, int]] = 'Verdana 9',
        show_label_box: bool = False,
        label_box_color: _Optional[str] = None,
        label_box_width: _Optional[int] = None,
        label_box_height: _Optional[int] = None,
        label_y_shift: int = -15,

        show_value: bool = True,
        value_fg: str = '#ccc',
        value_font: _Union[str, _Tuple[str, int]] = 'Consolas 9',
        value_prefix: str = '',
        value_suffix: str = '',
        show_value_box: bool = False,
        value_box_color: _Optional[str] = None,
        value_box_width: _Optional[int] = None,
        value_box_height: _Optional[int] = None,
        value_box_x_shift: int = 25,  # extra arg. reminder: this parameter has a different argument name for horizontal and vertical sliders

        rod_len: int = 200,
        rod_thick: int = 3,
        btn_r: int = 5,
        color_rod_normal: str = '#4b4b4b',
        color_rod_locked: str = '#2d2d2d',
        color_btn_normal: str = '#555555',
        color_btn_locked: str = '#373737',
        color_btn_press: str = '#7d7d7d',
        color_btn_hover: str = '#696969',
        color_btn_bd_normal: str = '#f5f5f5',
        color_btn_bd_locked: str = '#373737',

        locked: bool = False,
        visible: bool = True,

        id: _Optional[str] = None,
        tags: _Optional[_Union[str, _List[str]]] = None,
    ) -> None:

        super().__init__(
            min, max, step, init, fn,
            x, y, anchor, tolerance,
            label, label_fg, label_font, show_label_box, label_box_color, label_box_width, label_box_height, label_y_shift,
            show_value, value_fg, value_font, value_prefix, value_suffix, show_value_box, value_box_color, value_box_width, value_box_height,
            rod_len, rod_thick, btn_r, color_rod_normal, color_rod_locked, color_btn_normal, color_btn_locked, color_btn_press, color_btn_hover, color_btn_bd_normal, color_btn_bd_locked,
            locked, visible,
            id, tags
        )

        self.value_box_x_shift = value_box_x_shift

        ## runtime (custom)

        self.width = self.rod_len
        self.height = self.rod_thick

        ## init        
        
        self._redraw()

    def _redraw(self):

        if self.locked:
            color_rod = self.color_rod_locked
            color_btn = self.color_btn_locked
            color_btn_bd = self.color_btn_bd_locked
        elif self.pressed:
            color_rod = self.color_rod_normal
            color_btn = self.color_btn_press
            color_btn_bd = self.color_btn_bd_normal
        elif self.hovered:
            color_rod = self.color_rod_normal
            color_btn = self.color_btn_hover
            color_btn_bd = self.color_btn_bd_normal
        else:
            color_rod = self.color_rod_normal
            color_btn = self.color_btn_normal
            color_btn_bd = self.color_btn_bd_normal

        _Slider._page.delete(f'Slider_{self.id}')

        if self.visible:

            X, Y = self.get_anchor_loc('center')
            w2 = self.width/2
            h2 = self.height/2

            _Slider._page.create_rectangle(
                X-w2, Y-h2,
                X+w2, Y+h2,
                fill=color_rod, width=0, tags=f'Slider_{self.id}'
            )
            _Slider._page.create_oval(
                X-w2+_norm(self.value, self.min, self.max)*self.width-self.btn_r, Y-self.btn_r,
                X-w2+_norm(self.value, self.min, self.max)*self.width+self.btn_r, Y+self.btn_r,
                fill=color_btn, width=1, outline=color_btn_bd, tags=f'Slider_{self.id}'
            )

            if self.show_label_box:
                _Slider._page.create_rectangle(
                    X-self.label_box_width/2, Y-h2+self.label_y_shift-self.label_box_height/2,
                    X+self.label_box_width/2, Y-h2+self.label_y_shift+self.label_box_height/2,
                    fill=self.label_box_color, width=0, tags=f'Slider_{self.id}'
                )
            if self.label is not None:
                _Slider._page.create_text(
                    X, Y-h2+self.label_y_shift,
                    text=self.label, font=self.label_font, fill=self.label_fg, tags=f'Slider_{self.id}'
                )

            if self.show_value_box:
                _Slider._page.create_rectangle(
                    X+w2+self.value_box_x_shift-self.value_box_width/2, Y-self.value_box_height/2,
                    X+w2+self.value_box_x_shift+self.value_box_width/2, Y+self.value_box_height/2,
                    fill=self.value_box_color, width=0, tags=f'Slider_{self.id}'
                )
            if self.show_value:
                _Slider._page.create_text(
                    X+w2+self.value_box_x_shift, Y,
                    text=self.value_prefix + str(self.value) + self.value_suffix,
                    font=self.value_font, fill=self.value_fg, tags=f'Slider_{self.id}'
                )

    def _hover(self):

        X, Y = self.get_anchor_loc('center')

        x = _Slider._page.winfo_pointerx()
        y = _Slider._page.winfo_pointery()

        ## button coordinate
        bx = X - self.width/2 + _norm(self.value, self.min, self.max)*self.width
        by = Y
        br = self.btn_r  # button radius

        ## `True` if the mouse cursor is inside the slider button
        inside = (bx-br <= x <= bx+br) and (by-br <= y <= by+br)

        if inside and (not self.locked) and self.visible and (not self.hovered):
            self.hovered = True
            self._redraw()
        
        elif self.hovered and (not inside):
            self.hovered = False
            self._redraw()

    def _press(self):

        X, Y = self.get_anchor_loc('center')

        x = _Slider._page.winfo_pointerx()
        y = _Slider._page.winfo_pointery()

        bx = X - self.width/2 + _norm(self.value, self.min, self.max)*self.width
        by = Y
        br = self.btn_r

        inside = (bx-br <= x <= bx+br) and (by-br <= y <= by+br)

        if inside and (not self.locked) and self.visible:
            self.pressed = True
            self._redraw()

    def _hold(self):

        if self.pressed:

            X, _ = self.get_anchor_loc('center')

            mousex = _Slider._page.winfo_pointerx()
            value = self.min + ((mousex - (X - self.width/2))/self.width)*(self.max - self.min)

            if self.prec == 0:
                value = int(value)
            else:
                value = round(value, self.prec)

            if abs(value - round(value/self.step)*self.step) < self.tolerance*self.step:

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
        min: float = 0,
        max: float = 1,
        step: _Optional[float] = None,
        init: _Optional[float] = None,
        fn: _Optional[_Callable[[], None]] = None,

        x: int = 0,
        y: int = 0,
        anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw',
        tolerance: float = 0.25,
        
        label: _Optional[str] = None,
        label_fg: str = '#ccc',
        label_font: _Union[str, _Tuple[str, int]] = 'Verdana 9',
        show_label_box: bool = False,
        label_box_color: _Optional[str] = None,
        label_box_width: _Optional[int] = None,
        label_box_height: _Optional[int] = None,
        label_y_shift: int = -15,

        show_value: bool = True,
        value_fg: str = '#ccc',
        value_font: _Union[str, _Tuple[str, int]] = 'Consolas 9',
        value_prefix: str = '',
        value_suffix: str = '',
        show_value_box: bool = False,
        value_box_color: _Optional[str] = None,
        value_box_width: _Optional[int] = None,
        value_box_height: _Optional[int] = None,
        value_box_y_shift: int = 15,  # extra arg. reminder: this parameter has a different argument name for horizontal and vertical sliders

        rod_len: int = 200,
        rod_thick: int = 3,
        btn_r: int = 5,
        color_rod_normal: str = '#4b4b4b',
        color_rod_locked: str = '#2d2d2d',
        color_btn_normal: str = '#555555',
        color_btn_locked: str = '#373737',
        color_btn_press: str = '#7d7d7d',
        color_btn_hover: str = '#696969',
        color_btn_bd_normal: str = '#f5f5f5',
        color_btn_bd_locked: str = '#373737',

        locked: bool = False,
        visible: bool = True,

        id: _Optional[str] = None,
        tags: _Optional[_Union[str, _List[str]]] = None,
    ) -> None:

        super().__init__(
            min, max, step, init, fn,
            x, y, anchor, tolerance,
            label, label_fg, label_font, show_label_box, label_box_color, label_box_width, label_box_height, label_y_shift,
            show_value, value_fg, value_font, value_prefix, value_suffix, show_value_box, value_box_color, value_box_width, value_box_height,
            rod_len, rod_thick, btn_r, color_rod_normal, color_rod_locked, color_btn_normal, color_btn_locked, color_btn_press, color_btn_hover, color_btn_bd_normal, color_btn_bd_locked,
            locked, visible,
            id, tags
        )

        self.value_box_y_shift = value_box_y_shift

        ## runtime (custom)

        self.width = self.rod_thick
        self.height = self.rod_len

        ## init        
        
        self._redraw()

    def _redraw(self):

        if self.locked:
            color_rod = self.color_rod_locked
            color_btn = self.color_btn_locked
            color_btn_bd = self.color_btn_bd_locked
        elif self.pressed:
            color_rod = self.color_rod_normal
            color_btn = self.color_btn_press
            color_btn_bd = self.color_btn_bd_normal
        elif self.hovered:
            color_rod = self.color_rod_normal
            color_btn = self.color_btn_hover
            color_btn_bd = self.color_btn_bd_normal
        else:
            color_rod = self.color_rod_normal
            color_btn = self.color_btn_normal
            color_btn_bd = self.color_btn_bd_normal

        _Slider._page.delete(f'Slider_{self.id}')

        if self.visible:

            X, Y = self.get_anchor_loc('center')
            w2 = self.width/2
            h2 = self.height/2

            _Slider._page.create_rectangle(
                X-w2, Y-h2,
                X+w2, Y+h2,
                fill=color_rod, width=0, tags=f'Slider_{self.id}'
            )
            _Slider._page.create_oval(
                X-self.btn_r, Y+h2-_norm(self.value, self.min, self.max)*self.height-self.btn_r,
                X+self.btn_r, Y+h2-_norm(self.value, self.min, self.max)*self.height+self.btn_r,
                fill=color_btn, width=1, outline=color_btn_bd, tags=f'Slider_{self.id}'
            )

            if self.show_label_box:
                _Slider._page.create_rectangle(
                    X-self.label_box_width/2, Y-h2+self.label_y_shift-self.label_box_height/2,
                    X+self.label_box_width/2, Y-h2+self.label_y_shift+self.label_box_height/2,
                    fill=self.label_box_color, width=0, tags=f'Slider_{self.id}'
                )
            if self.label is not None:
                _Slider._page.create_text(
                    X, Y-h2+self.label_y_shift,
                    text=self.label, font=self.label_font, fill=self.label_fg, tags=f'Slider_{self.id}'
                )

            if self.show_value_box:
                _Slider._page.create_rectangle(
                    X-self.value_box_width/2, Y+h2+self.value_box_y_shift-self.value_box_height/2,
                    X+self.value_box_width/2, Y+h2+self.value_box_y_shift+self.value_box_height/2,
                    fill=self.value_box_color, width=0, tags=f'Slider_{self.id}'
                )
            if self.show_value:
                _Slider._page.create_text(
                    X, Y+h2+self.value_box_y_shift,
                    text=self.value_prefix + str(self.value) + self.value_suffix,
                    font=self.value_font, fill=self.value_fg, tags=f'Slider_{self.id}'
                )

    def _hover(self):

        X, Y = self.get_anchor_loc('center')

        x = _Slider._page.winfo_pointerx()
        y = _Slider._page.winfo_pointery()

        bx = X
        by = Y + self.height/2 - _norm(self.value, self.min, self.max)*self.height
        br = self.btn_r

        inside = (bx-br <= x <= bx+br) and (by-br <= y <= by+br)

        if inside and (not self.locked) and self.visible and (not self.hovered):
            self.hovered = True
            self._redraw()
        
        elif self.hovered and (not inside):
            self.hovered = False
            self._redraw()

    def _press(self):

        X, Y = self.get_anchor_loc('center')

        x = _Slider._page.winfo_pointerx()
        y = _Slider._page.winfo_pointery()

        bx = X
        by = Y + self.height/2 - _norm(self.value, self.min, self.max)*self.height
        br = self.btn_r

        inside = (bx-br <= x <= bx+br) and (by-br <= y <= by+br)

        if inside and (not self.locked) and self.visible:
            self.pressed = True
            self._redraw()

    def _hold(self):

        if self.pressed:

            _, Y = self.get_anchor_loc('center')

            mousey = _Slider._page.winfo_pointery()
            value = self.max - ((mousey - (Y - self.height/2))/self.height)*(self.max - self.min)
    
            if self.prec == 0:
                value = int(value)
            else:
                value = round(value, self.prec)

            if abs(value - round(value/self.step)*self.step) < self.tolerance*self.step:

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