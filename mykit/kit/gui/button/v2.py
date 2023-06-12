import random as _random
import tkinter as _tk
import typing as _typing


class Button:
    """
    The next version of `carbon.gui.button.Button`.

    ## What's new
    - Arguments reordering, default value changes
    - Added colors (button color, border color, label color) parameters
    - Added height (button's height) parameters
    - Param `id` and `label` are now optional
    """

    page: _tk.Canvas = None
    @staticmethod
    def set_page(page: _tk.Canvas, /) -> None:
        Button.page = page

    buttons: dict[str, 'Button'] = {}
    button_tags: dict[str, list['Button']] = {}

    def __init__(
        self,
        x: int,
        y: int,
        fn: _typing.Callable[[], None],
        
        label: str = '',

        anchor: _typing.Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw',

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

        id: str | None = None,
        tags: str | list[str] | None = None,
    ) -> None:
        """
        ## Params
        - `x` and `y` is the position of the `anchor`
        - `color_btn_normal`: button's color
        - `color_bd_normal`: button's border color
        - `color_lbl_normal`: button's label color
        """

        self.x = x
        self.y = y
        self.fn = fn

        ## below isn't necessary because will be checked at `self._anchoring()`  (delete below code soon)
        # if anchor.lower() not in ['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
        #     raise ValueError(f'Invalid anchor value: {repr(anchor)}')
        # self.anchor = anchor.lower()
        self.anchor = anchor

        self.label = label
        
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

        ## self.id ensures that we can modify a specific instance without affecting the others
        if id is None:
            self.id = str(_random.randint(-10000, 10000))
            while self.id in Button.buttons:
                self.id = str(_random.randint(-10000, 10000))
        else:
            self.id = id
            if self.id in Button.buttons:
                raise ValueError(f'The id {repr(id)} is duplicated.')
        Button.buttons[self.id] = self

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


        ## preprocess
        self._anchoring()


        ## runtime
        self.default_label = label
        self.pressed = False
        self.hovered = False


        ## init
        self._redraw()

    def _anchoring(self):
        
        self.anchor = self.anchor.lower()
        
        if self.anchor == 'center':
            self.ctr_x = self.x
            self.ctr_y = self.y
        elif self.anchor == 'n':
            self.ctr_x = self.x
            self.ctr_y = self.y + self.height/2
        elif self.anchor == 'ne':
            self.ctr_x = self.x - self.width/2
            self.ctr_y = self.y + self.height/2
        elif self.anchor == 'e':
            self.ctr_x = self.x - self.width/2
            self.ctr_y = self.y
        elif self.anchor == 'se':
            self.ctr_x = self.x - self.width/2
            self.ctr_y = self.y - self.height/2
        elif self.anchor == 's':
            self.ctr_x = self.x
            self.ctr_y = self.y - self.height/2
        elif self.anchor == 'sw':
            self.ctr_x = self.x + self.width/2
            self.ctr_y = self.y - self.height/2
        elif self.anchor == 'w':
            self.ctr_x = self.x + self.width/2
            self.ctr_y = self.y
        elif self.anchor == 'nw':
            self.ctr_x = self.x + self.width/2
            self.ctr_y = self.y + self.height/2
        else:
            raise ValueError(f'Unexpected anchor value: {repr(self.anchor)}')

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

        Button.page.delete(f'Button_{self.id}')

        if self.visible:

            Button.page.create_rectangle(
                self.ctr_x - self.width/2, self.ctr_y - self.height/2,
                self.ctr_x + self.width/2, self.ctr_y + self.height/2,
                fill=color_btn, width=1, outline=color_bd,
                tags=f'Button_{self.id}'
            )
            Button.page.create_text(
                self.ctr_x, self.ctr_y,
                text=self.label, font='Arial 9',
                fill=color_lbl,
                tags=f'Button_{self.id}'
            )

    def hover(self):
        
        mousex = Button.page.winfo_pointerx()
        mousey = Button.page.winfo_pointery()

        if (
            (self.ctr_x-self.width/2 <= mousex <= self.ctr_x+self.width/2)
            and
            (self.ctr_y-self.height/2 <= mousey <= self.ctr_y+self.height/2)
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
            (not ((self.ctr_x-self.width/2 <= mousex <= self.ctr_x+self.width/2) and (self.ctr_y-self.height/2 <= mousey <= self.ctr_y+self.height/2)))
        ):
            self.hovered = False
            self._redraw()

    def press(self):
        
        mousex = Button.page.winfo_pointerx()
        mousey = Button.page.winfo_pointery()

        if (
            (self.ctr_x-self.width/2 <= mousex <= self.ctr_x+self.width/2)
            and
            (self.ctr_y-self.height/2 <= mousey <= self.ctr_y+self.height/2)
            and
            (not self.locked)
            and
            (self.visible)
        ):
            self.pressed = True
            self._redraw()

    def release(self):
        if self.pressed:
            self.pressed = False
            self._redraw()
            self.fn()

    @staticmethod
    def hover_listener():
        for button in Button.buttons.values():
            button.hover()

    @staticmethod
    def press_listener():
        for button in Button.buttons.values():
            button.press()

    @staticmethod
    def release_listener():
        for button in list(Button.buttons.values()):
            button.release()

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


    def set_label(self, label: str | None, /):
        """if `None` -> default label."""

        if label is None:
            label = self.default_label

        if self.label != label:
            self.label = label
            self._redraw()

    @staticmethod
    def set_label_by_id(id: str, label: str | None, /):
        Button.buttons[id].set_label(label)


    def set_fn(self, fn: _typing.Callable[[], None], /):
        if self.fn is not fn:
            self.fn = fn

    @staticmethod
    def set_fn_by_id(id: str, fn: _typing.Callable[[], None], /):
        Button.buttons[id].set_fn(fn)


    def move(self, x: int, y: int, /, anchor: str | None = None) -> None:
        """move the button (using the default anchor if `anchor=None`)"""
        
        self.x = x
        self.y = y
        
        if anchor is not None:
            self.anchor = anchor

        self._anchoring()
        self._redraw()

    @staticmethod
    def move_by_id(id: str, x: int, y: int, /) -> None:
        Button.buttons[id].move(x, y)


    def destroy(self) -> None:
        Button.buttons.pop(self.id)
        
        if self.tags is not None:
            for tag in self.tags:
                Button.button_tags[tag].remove(self)
                if Button.button_tags[tag] == []:
                    Button.button_tags.pop(tag)

        Button.page.delete(f'Button_{self.id}')

    @staticmethod
    def destroy_by_tag(tag: str, /) -> None:

        if tag not in Button.button_tags:
            return

        for button in list(Button.button_tags[tag]):
            button.destroy()

    @staticmethod
    def destroy_all() -> None:
        for button in list(Button.buttons.values()):
            button.destroy()
    

    def get_bounding_box(self) -> tuple[float, float, float, float]:
        tl_x = self.ctr_x - self.width/2
        tl_y = self.ctr_y - self.height/2
        dr_x = self.ctr_x + self.width/2
        dr_y = self.ctr_y + self.height/2
        return [tl_x, tl_y, dr_x, dr_y]

    @staticmethod
    def get_bounding_box_by_id(id: str, /) -> tuple[float, float, float, float]:
        return Button.buttons[id].get_bounding_box()