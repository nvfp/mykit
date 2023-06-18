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


class Button:

    ## <runtime>

    _page: _tk.Canvas = None
    @staticmethod
    def _set_page(page):
        Button._page = page

    buttons: _Dict[str, 'Button'] = {}
    button_tags: _Dict[str, _List['Button']] = {}

    ## </runtime>

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        fn: _Optional[_Callable[[], None]] = None,
        label: str = '',
        label_font: _Union[str, _Tuple[str, int]] = 'Verdana 8',
        anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw',
        width: int = 100,
        height: int = 18,
        locked: bool = False,
        visible: bool = True,

        color_btn_normal: str = '#464646',
        color_btn_hover: str = '#5a5a5a',
        color_btn_press: str = '#6e6e6e',
        color_btn_locked: str = '#282828',
        color_bd_normal: str = '#6e6e6e',
        color_bd_locked: str = '#282828',
        color_lbl_normal: str = '#fafbfa',
        color_lbl_locked: str = '#050505',

        id: _Optional[str] = None,
        tags: _Optional[_Union[str, _List[str]]] = None,
    ) -> None:
        """
        ## Params
        - `x` and `y` is the position of the `anchor` (not the center of the button)
        - `color_btn_normal`: button's color
        - `color_bd_normal`: button's border color
        - `color_lbl_normal`: button's label color
        """

        ## <dependencies check>

        if Button._page is None:
            raise AssertionError('Can\'t use widgets before App initialized.')
        
        ## </dependencies check>

        self.x = x
        self.y = y
        self.fn = fn
        self.label = label
        self.label_font = label_font
        self.anchor = anchor
        self.width = width
        self.height = height
        self.locked = locked
        self.visible = visible

        self.color_btn_normal = color_btn_normal
        self.color_btn_hover = color_btn_hover
        self.color_btn_press = color_btn_press
        self.color_btn_locked = color_btn_locked
        self.color_bd_normal = color_bd_normal
        self.color_bd_locked = color_bd_locked
        self.color_lbl_normal = color_lbl_normal
        self.color_lbl_locked = color_lbl_locked

        ## <id>

        ## self.id ensures that we can modify a specific instance without affecting the others
        if id is None:
            self.id = str(_random.randint(0, 100_000))
            while self.id in Button.buttons:
                self.id = str(_random.randint(0, 100_000))
        else:
            self.id = id
            if self.id in Button.buttons:
                raise ValueError(f'The id {repr(id)} is duplicated.')
        
        Button.buttons[self.id] = self

        ## </id>

        ## <tags>

        if type(tags) is str:
            self.tags = [tags]
        elif (type(tags) is list) or (type(tags) is tuple) or (tags is None):
            self.tags = tags
        
        if tags is not None:
            for tag in self.tags:
                if tag in Button.button_tags:
                    Button.button_tags[tag].append(self)
                else:
                    Button.button_tags[tag] = [self]

        ## </tags>


        ## runtime

        self.default_label = label
        self.pressed = False
        self.hovered = False


        ## init

        self._redraw()


    def _redraw(self):

        if self.locked:
            color_btn = self.color_btn_locked
            color_bd = self.color_bd_locked
            color_lbl = self.color_lbl_locked
        elif self.pressed:
            color_btn = self.color_btn_press
            color_bd = self.color_bd_normal
            color_lbl = self.color_lbl_normal
        elif self.hovered:
            color_btn = self.color_btn_hover
            color_bd = self.color_bd_normal
            color_lbl = self.color_lbl_normal
        else:
            color_btn = self.color_btn_normal
            color_bd = self.color_bd_normal
            color_lbl = self.color_lbl_normal

        Button._page.delete(f'Button_{self.id}')

        if self.visible:

            ## This overhead will be executed each time this function is called.
            ## It may be inefficient, but it makes the code cleaner.
            X, Y = self.get_anchor_loc('center')  # the center of the button

            Button._page.create_rectangle(
                X - self.width/2, Y - self.height/2,
                X + self.width/2, Y + self.height/2,
                fill=color_btn, width=1, outline=color_bd,
                tags=f'Button_{self.id}'
            )
            Button._page.create_text(
                X, Y,
                text=self.label, font=self.label_font,
                fill=color_lbl,
                tags=f'Button_{self.id}'
            )


    def _hover(self):

        w2 = self.width/2
        h2 = self.height/2
        
        x = Button._page.winfo_pointerx()
        y = Button._page.winfo_pointery()

        X, Y = self.get_anchor_loc('center')

        ## `True` if the mouse cursor is inside the button
        inside = (X-w2 <= x <= X+w2) and (Y-h2 <= y <= Y+h2)

        if inside and (not self.locked) and self.visible and (not self.hovered):
            self.hovered = True
            self._redraw()  # just redraw once here

        elif self.hovered and (not inside):
            self.hovered = False
            self._redraw()  # just redraw once here

        ## reminder: don't put self._redraw below here because it will redraw regardless of the "hovered" state
        # self._redraw()

    @staticmethod
    def _hover_listener():  # reminder: hover listeners don't need `e: _tk.Event` arg
        for button in Button.buttons.values():
            button._hover()


    def _press(self):
        
        x = Button._page.winfo_pointerx()
        y = Button._page.winfo_pointery()

        X, Y = self.get_anchor_loc('center')
        w2 = self.width/2
        h2 = self.height/2
        inside = (X-w2 <= x <= X+w2) and (Y-h2 <= y <= Y+h2)

        if inside and (not self.locked) and self.visible:
            self.pressed = True
            self._redraw()

    @staticmethod
    def _press_listener(e: _tk.Event):
        for button in Button.buttons.values():
            button._press()


    def _release(self):
        if self.pressed:
            self.pressed = False
            self._redraw()            
            if self.fn is not None:
                self.fn()

    @staticmethod
    def _release_listener(e: _tk.Event):
        for button in list(Button.buttons.values()):
            button._release()


    def set_lock(self, locked: bool, /):
        if self.locked is not locked:
            self.locked = locked
            self._redraw()
    
    @staticmethod
    def set_lock_by_id(id: str, locked: bool, /):
        Button.buttons[id].set_lock(locked)

    @staticmethod
    def set_lock_by_tag(tag: str, locked: bool, /):
        for button in Button.button_tags[tag]:
            button.set_lock(locked)

    @staticmethod
    def set_lock_all(locked: bool, /):
        for button in Button.buttons.values():
            button.set_lock(locked)


    def set_visibility(self, visible: bool, /):
        if self.visible is not visible:
            self.visible = visible
            self._redraw()

    @staticmethod
    def set_visibility_by_id(id: str, visible: bool, /):
        Button.buttons[id].set_visibility(visible)

    @staticmethod
    def set_visibility_by_tag(tag: str, visible: bool, /):
        for button in Button.button_tags[tag]:
            button.set_visibility(visible)

    @staticmethod
    def set_visibility_all(visible: bool, /):
        for button in Button.buttons.values():
            button.set_visibility(visible)


    def set_label(self, label: _Optional[str], /):
        """
        If `label = None`, the default label (the one assigned
        when the instance was created) will be used.
        """

        if label is None:
            label = self.default_label

        if self.label != label:
            self.label = label
            self._redraw()

    @staticmethod
    def set_label_by_id(id: str, label: _Optional[str], /):
        Button.buttons[id].set_label(label)


    def set_fn(self, fn: _Callable[[], None], /):
        if self.fn is not fn:
            self.fn = fn

    @staticmethod
    def set_fn_by_id(id: str, fn: _Callable[[], None], /):
        Button.buttons[id].set_fn(fn)


    def get_anchor_loc(
        self,
        anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'],
        /
    ) -> _Tuple[int, int]:
        """To get the button's center coordinate, use `anchor='center'`"""

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
        return Button.buttons[id].get_anchor_loc(anchor)


    def move(
        self,
        x: int,
        y: int,
        /,
        anchor: _Optional[_Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']] = None
    ) -> 'Button':
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
        Button.buttons[id].move(x, y, anchor)


    def align(
        self,
        target: 'Button',
        anchor: str = 'nw',
        target_anchor: str = 'ne',
        xgap: float = 15,
        ygap: float = 0
    ) -> 'Button':
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
        ## creating the instance, like `btn_2 = Button().align(btn_1)`.
        return self


    def destroy(self) -> None:
        Button.buttons.pop(self.id)
        
        if self.tags is not None:
            for tag in self.tags:
                Button.button_tags[tag].remove(self)
                if Button.button_tags[tag] == []:
                    Button.button_tags.pop(tag)

        Button._page.delete(f'Button_{self.id}')
    
    @staticmethod
    def destroy_by_id(id: str, /) -> None:
        Button.buttons[id].destroy()

    @staticmethod
    def destroy_by_tag(tag: str, /) -> None:
        for button in list(Button.button_tags[tag]):
            button.destroy()

    @staticmethod
    def destroy_all() -> None:
        for button in list(Button.buttons.values()):
            button.destroy()
