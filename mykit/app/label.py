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


## reminder: Label is different because it uses tkinter.Label
##           instead of tkinter.Canvas. Not sure if it'll be okay,
##           but for now, let's go with it.  @June 18, 2023 - Nicholas
class Label:

    labels: _Dict[str, 'Label'] = {}
    label_tags: _Dict[str, _List['Label']] = {}

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        text: str = '',
        font: _Union[str, _Tuple[str, int]] = 'Verdana 10',
        justify: str = 'left',
        anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw',
        fg: str = '#ccc',
        bg: str = '#111',
        bd: str = '#555',
        bd_width: int = 0,
        wraplength: int = 1000,
        padx: int = 0,
        pady: int = 0,
        visible: bool = True,

        id: _Optional[str] = None,
        tags: _Optional[_Union[str, _List[str]]] = None,
    ):
        """
        `x`: the x-position for the `anchor` argument, not the center of the label
        `y`: the y-position for the `anchor` argument, not the center of the label
        """

        self.x = x  # reminder: this is the x-position for the `anchor` argument, not the center of the label
        self.y = y  # reminder: this is the y-position for the `anchor` argument, not the center of the label
        self.font = font
        self.text = text
        self.anchor = anchor
        self.fg = fg
        self.visible = visible

        self.default_text = text

        self.label = _tk.Label(
            text=text, font=font, justify=justify,
            foreground=fg, background=bg,
            highlightbackground=bd, highlightthickness=bd_width,
            wraplength=wraplength,
            padx=padx, pady=pady
        )

        if visible:
            self.label.place(x=x, y=y, anchor=anchor)


        ## <id>

        ## self.id ensures that we can modify a specific instance without affecting the others
        if id is None:
            self.id = str(_random.randint(0, 100_000))
            while self.id in Label.labels:
                self.id = str(_random.randint(0, 100_000))
        else:
            self.id = id
            if self.id in Label.labels:
                raise ValueError(f'The id {repr(id)} is duplicated.')
        
        Label.labels[self.id] = self

        ## </id>


        ## <tags>
        
        if type(tags) is str:
            self.tags = [tags]
        elif (type(tags) is list) or (type(tags) is tuple) or (tags is None):
            self.tags = tags
        
        if tags is not None:
            for tag in self.tags:
                if tag in Label.label_tags:
                    Label.label_tags[tag].append(self)
                else:
                    Label.label_tags[tag] = [self]
        
        ## <tags>


    def set_text(self, text: _Optional[str], /):
        """if None -> set default text."""

        if text is None:
            text = self.default_text

        if text != self.text:
            self.text = text
            self.label.configure(text=text)

    @staticmethod
    def set_text_by_id(id: str, text: _Optional[str], /):
        Label.labels[id].set_text(text)


    def set_font(self, font: _Union[str, _Tuple[str, int]], /):
        if font != self.font:
            self.font = font
            self.label.configure(font=font)

    @staticmethod
    def set_font_by_id(id: str, font: _Union[str, _Tuple[str, int]], /):
        Label.labels[id].set_font(font)


    def set_fg(self, fg: str, /):
        if fg != self.fg:
            self.fg = fg
            self.label.configure(fg=fg)

    @staticmethod
    def set_fg_by_id(id: str, fg: str, /):
        Label.labels[id].set_fg(fg)


    def set_visibility(self, visible: bool, /):
        if self.visible is not visible:
            self.visible = visible
            if visible:
                self.label.place(x=self.x, y=self.y, anchor=self.anchor)
            else:
                self.label.place_forget()

    @staticmethod
    def set_visibility_by_id(id: str, visible: bool, /):
        Label.labels[id].set_visibility(visible)

    @staticmethod
    def set_visibility_by_tag(tag: str, visible: bool, /):
        for label in Label.label_tags[tag]:
            label.set_visibility(visible)

    @staticmethod
    def set_visibility_all(visible: bool, /):
        for label in Label.labels.values():
            label.set_visibility(visible)


    def get_width(self) -> int:
        return self.label.winfo_reqwidth()

    @staticmethod
    def get_width_by_id(id: str, /) -> int:
        return Label.labels[id].get_width()

    def get_height(self) -> int:
        return self.label.winfo_reqheight()

    @staticmethod
    def get_height_by_id(id: str, /) -> int:
        return Label.labels[id].get_height()


    def get_anchor_loc(self, anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'], /) -> _Tuple[int, int]:
        """To get the center of the label coordinates, use `anchor='center'`"""

        W = self.get_width()
        H = self.get_height()

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
    def get_anchor_loc_by_id(id: str, anchor: _Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'], /) -> _Tuple[int, int]:
        return Label.labels[id].get_anchor_loc(anchor)

    
    def move(
        self,
        x: int,
        y: int,
        /,
        anchor: _Optional[_Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']] = None
    ) -> 'Label':
        """If `anchor = None`, the current anchor will be used."""
        self.x = x
        self.y = y
        if anchor is not None:
            self.anchor = anchor
        # self.label.place(x=x, y=y, anchor=anchor)  # reminder: don't do this because `anchor` could be `None`
        self.label.place(x=x, y=y, anchor=self.anchor)
        return self

    @staticmethod
    def move_by_id(
        id: str,
        x: int,
        y: int,
        /,
        anchor: _Optional[_Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']] = None
    ) -> None:
        Label.labels[id].move(x, y, anchor)


    def align(
        self,
        target: 'Label',
        anchor: str = 'nw',
        target_anchor: str = 'ne',
        xgap: float = 15,
        ygap: float = 0
    ) -> 'Label':
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
        ## creating the instance, like `label_2 = Label(text='foo').align(label_1)`.
        return self


    def destroy(self) -> None:
        Label.labels.pop(self.id)

        if self.tags is not None:
            for tag in list(self.tags):
                Label.label_tags[tag].remove(self)
                if Label.label_tags[tag] == []:
                    Label.label_tags.pop(tag)
        
        self.label.destroy()
    
    @staticmethod
    def destroy_by_id(id: str, /) -> None:
        Label.labels[id].destroy()

    @staticmethod
    def destroy_by_tag(tag: str, /) -> None:
        for label in list(Label.label_tags[tag]):
            label.destroy()

    @staticmethod
    def destroy_all() -> None:
        for label in list(Label.labels.values()):
            label.destroy()