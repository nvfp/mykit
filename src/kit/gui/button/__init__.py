import tkinter as _tk
import typing as _typing


HEIGHT = 18

COLOR = '#464646'
COLOR_HOVERED = '#5a5a5a'
COLOR_PRESSED = '#6e6e6e'
COLOR_LOCKED = '#282828'

BD_COLOR = '#6e6e6e'
BD_COLOR_LOCKED = '#282828'

LABEL_COLOR = '#fafbfa'
LABEL_COLOR_LOCKED = '#050505'


class Button:

    page: _tk.Canvas = None
    @staticmethod
    def set_page(page: _tk.Canvas, /) -> None:
        Button.page = page

    buttons: dict[str, 'Button'] = {}
    button_tags: dict[str, list['Button']] = {}

    def __init__(
        self,
        id: str,
        x: int,
        y: int,
        label: str,
        fn: _typing.Callable[[], None],
        len: int = 100,
        locked: bool = False,
        visible: bool = True,
        tags: str | list[str] | None = None,
    ) -> None:

        self.id = id
        if id in Button.buttons:
            raise ValueError(f'The id {repr(id)} is duplicated.')
        Button.buttons[id] = self

        self.x = x
        self.y = y
        self.label = label
        self.fn = fn
        self.len = len
        self.locked = locked
        self.visible = visible

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

        self.redraw()

    def redraw(self):

        if self.locked:
            color = COLOR_LOCKED
            bd_color = BD_COLOR_LOCKED
            label_color = LABEL_COLOR_LOCKED
        elif self.pressed:
            color = COLOR_PRESSED
            bd_color = BD_COLOR
            label_color = LABEL_COLOR
        elif self.hovered:
            color = COLOR_HOVERED
            bd_color = BD_COLOR
            label_color = LABEL_COLOR
        else:
            color = COLOR
            bd_color = BD_COLOR
            label_color = LABEL_COLOR

        Button.page.delete(f'button_{self.id}')

        if self.visible:
            Button.page.create_rectangle(
                self.x - self.len/2, self.y - HEIGHT/2,
                self.x + self.len/2, self.y + HEIGHT/2,
                fill=color, width=1, outline=bd_color,
                tags=f'button_{self.id}'
            )
            Button.page.create_text(
                self.x, self.y,
                text=self.label, font='Arial 9',
                fill=label_color,
                tags=f'button_{self.id}'
            )

    def hover(self):
        
        mousex = Button.page.winfo_pointerx()
        mousey = Button.page.winfo_pointery()

        if (
            (self.x - self.len/2 <= mousex <= self.x + self.len/2)
            and
            (self.y - HEIGHT/2 <= mousey <= self.y + HEIGHT/2)
            and
            (not self.locked)
            and
            (self.visible)
            and
            (not self.hovered)
        ):
            self.hovered = True
            self.redraw()
        elif (
            (self.hovered)
            and
            (not ((self.x - self.len/2 <= mousex <= self.x + self.len/2) and (self.y - HEIGHT/2 <= mousey <= self.y + HEIGHT/2)))
        ):
            self.hovered = False
            self.redraw()

    def press(self):
        
        mousex = Button.page.winfo_pointerx()
        mousey = Button.page.winfo_pointery()

        if (
            (self.x - self.len/2 <= mousex <= self.x + self.len/2)
            and
            (self.y - HEIGHT/2 <= mousey <= self.y + HEIGHT/2)
            and
            (not self.locked)
            and
            (self.visible)
        ):
            self.pressed = True
            self.redraw()

    def release(self):
        if self.pressed:
            self.pressed = False
            self.redraw()
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
            self.redraw()
    
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
            self.redraw()

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
            self.redraw()

    @staticmethod
    def set_label_by_id(id: str, label: str | None, /):
        Button.buttons[id].set_label(label)

    def set_fn(self, fn: _typing.Callable[[], None], /):
        if self.fn is not fn:
            self.fn = fn

    @staticmethod
    def set_fn_by_id(id: str, fn: _typing.Callable[[], None], /):
        Button.buttons[id].set_fn(fn)


    def move(self, x: int, y: int, /) -> None:
        self.x = x
        self.y = y
        self.redraw()

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

        Button.page.delete(f'button_{self.id}')
    
    @staticmethod
    def destroy_by_tag(tag: str, /) -> None:

        if tag not in Button.button_tags:
            return

        ## Use `list(Button.label_tags[tag])` instead of `Button.label_tags[tag]`
        ## since `Button.label_tags[tag]` changes during iteration.
        for button in list(Button.button_tags[tag]):
            button.destroy()

    @staticmethod
    def destroy_all() -> None:
        for button in list(Button.buttons.values()):
            button.destroy()