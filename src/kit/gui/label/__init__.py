import tkinter as _tk


class Label:

    labels: dict[str, 'Label'] = {}
    # tags: dict[str, list['Label']] = {}  # clash with `self.tags`
    label_tags: dict[str, list['Label']] = {}

    def __init__(
        self,
        id: str,
        x: int,
        y: int,
        text: str,
        font: str | tuple[str, int] = 'Consolas 10',
        justify: str = 'left',
        anchor: str = 'nw',
        fg: str = '#ccc',
        bg: str = '#111',
        bd: str = '#555',
        bd_width: int = 0,
        wraplength: int = 1000,
        padx: int = 0,
        pady: int = 0,
        visible: bool = True,
        tags: str | list[str] | None = None,
    ):

        self.id = id
        if id in Label.labels:
            raise ValueError(f'The id {repr(id)} is duplicated.')
        Label.labels[id] = self

        self.x = x
        self.y = y
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


    def set_text(self, text: str | None, /):
        """if None -> set default text."""

        if text is None:
            text = self.default_text

        if text != self.text:
            self.text = text
            self.label.configure(text=text)

    @staticmethod
    def set_text_by_id(id: str, text: str | None, /):
        Label.labels[id].set_text(text)


    def set_font(self, font: str | tuple[str, int], /):
        if font != self.font:
            self.font = font
            self.label.configure(font=font)

    @staticmethod
    def set_font_by_id(id: str, font: str | tuple[str, int], /):
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

    
    def get_bounding_box(self) -> tuple[int, int, int, int]:

        X = self.x
        Y = self.y
        W = self.get_width()
        H = self.get_height()

        if self.anchor == 'center':
            return (X - W/2, Y - H/2, X + W/2, Y + H/2)
        elif self.anchor == 'n':
            return (X - W/2, Y, X + W/2, Y + H)
        elif self.anchor == 'ne':
            return (X - W, Y, X, Y + H)
        elif self.anchor == 'e':
            return (X - W, Y - H/2, X, Y + H/2)
        elif self.anchor == 'se':
            return (X - W, Y - H, X, Y)
        elif self.anchor == 's':
            return (X - W/2, Y - H, X + W/2, Y)
        elif self.anchor == 'sw':
            return (X, Y - H, X + W, Y)
        elif self.anchor == 'w':
            return (X, Y - H/2, X + W, Y + H/2)
        elif self.anchor == 'nw':
            return (X, Y, X + W, Y + H)

    @staticmethod
    def get_bounding_box_by_id(id: str, /) -> tuple[int, int, int, int]:
        return Label.labels[id].get_bounding_box()

    
    def move(self, x: int, y: int, /) -> None:
        self.x = x
        self.y = y
        self.label.place(x=x, y=y, anchor=self.anchor)

    @staticmethod
    def move_by_id(id: str, x: int, y: int, /) -> None:
        Label.labels[id].move(x, y)


    def destroy(self) -> None:
        Label.labels.pop(self.id)

        if self.tags is not None:
            for tag in list(self.tags):
                Label.label_tags[tag].remove(self)
                if Label.label_tags[tag] == []:
                    Label.label_tags.pop(tag)
        
        self.label.destroy()

    @staticmethod
    def destroy_by_tag(tag: str, /) -> None:

        if tag not in Label.label_tags:
            return

        ## Use `list(Label.label_tags[tag])` instead of `Label.label_tags[tag]`
        ## since `Label.label_tags[tag]` changes during iteration.
        for label in list(Label.label_tags[tag]):
            label.destroy()

    @staticmethod
    def destroy_all() -> None:
        for label in list(Label.labels.values()):
            label.destroy()