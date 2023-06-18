import math as _math
import random as _random
import tkinter as _tk
from typing import (
    Dict as _Dict,
    List as _List,
    Optional as _Optional,
    Tuple as _Tuple,
    Union as _Union
)

from mykit.kit.math import (
    get_angle as _get_angle,
    rotate as _rotate
)


class Arrow:

    ## <runtime>

    _page: _tk.Canvas = None
    @staticmethod
    def _set_page(page):
        Arrow._page = page

    arrows: _Dict[str, 'Arrow'] = {}
    arrow_tags: _Dict[str, _List['Arrow']] = {}

    ## </runtime>

    def __init__(
        self,
        from_x: int, from_y: int,
        to_x: int, to_y: int,
        /,
        color: str = '#ddd',
        width_rod: int = 1,
        width_tip: int = 2,
        tip_len: float = 20,
        tip_angle: float = 35,
        visible: bool = True,
        
        id: _Optional[str] = None,
        tags: _Optional[_Union[str, _List[str]]] = None,
    ) -> None:

        ## <dependencies check>

        ## reminder: Arrow isn't actually a widget. it can be used as a utility
        ##           outside App's purposes. so just use Arrow._set_page to achieve it.
        if Arrow._page is None:
            raise AssertionError('Can\'t use widgets before App initialized.')
        
        ## </dependencies check>
        
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y

        self.color = color
        self.width_rod = width_rod
        self.width_tip = width_tip
        self.tip_len = tip_len
        self.tip_angle = tip_angle

        self.visible = visible

        ## <id>

        ## to make sure that we can modify a specific arrow without affecting the others
        if id is None:
            self.id = _random.randint(-10000, 10000)
            while self.id in Arrow.arrows:
                self.id = _random.randint(-10000, 10000)
        else:
            self.id = id
            if self.id in Arrow.arrows:
                raise ValueError(f'The Arrow\'s id {repr(id)} is duplicated.')
        
        Arrow.arrows[self.id] = self

        ## </id>

        ## <tags>

        if type(tags) is str:
            self.tags = [tags]
        elif (type(tags) is list) or (type(tags) is tuple) or (tags is None):
            self.tags = tags
        
        if tags is not None:
            for tag in self.tags:
                if tag in Arrow.arrow_tags:
                    Arrow.arrow_tags[tag].append(self)
                else:
                    Arrow.arrow_tags[tag] = [self]
        
        ## </tags>

        ## init
        self._redraw()

    def _redraw(self):

        Arrow._page.delete(f'Arrow_{self.id}')

        if self.visible:
            Arrow._page.create_line(
                self.from_x, self.from_y,
                self.to_x, self.to_y,
                fill=self.color, width=self.width_rod, tags=f'Arrow_{self.id}'
            )

            ## <creating the tip>
            ## for `angle`: remember to flip the y-sign because tkinter's y-positive direction towards the bottom
            angle = _get_angle(self.from_x, -self.from_y, self.to_x, -self.to_y)
            
            tipx = self.tip_len*_math.sin(self.tip_angle*_math.pi/180)
            tipy = self.tip_len*_math.cos(self.tip_angle*_math.pi/180)
            
            ## Remember `tip_left` and `tip_right` with y-positive towards the top,
            ## as they transformed under normal Cartesian coordinates.
            tip_left = _rotate(-tipx, -tipy, 0, 0, angle)
            tip_right = _rotate(tipx, -tipy, 0, 0, angle)

            ## Revert to the tkinter coordinate scheme, where y-positive is oriented downwards.
            tip_left = (self.to_x+tip_left[0], self.to_y-tip_left[1])
            tip_right = (self.to_x+tip_right[0], self.to_y-tip_right[1])

            tip_points = [tip_left, (self.to_x, self.to_y), tip_right]
            Arrow._page.create_line(tip_points, fill=self.color, width=self.width_tip, tags=f'Arrow_{self.id}')
            ## </creating the tip>


    def set_visibility(self, visible: bool, /):
        if visible != self.visible:
            self.visible = visible
            self._redraw()

    @staticmethod
    def set_visibility_by_id(id: str, visible: bool, /):
        Arrow.arrows[id].set_visibility(visible)

    @staticmethod
    def set_visibility_by_tag(tag: str, visible: bool, /):
        for arrow in Arrow.arrow_tags[tag]:
            arrow.set_visibility(visible)

    @staticmethod
    def set_visibility_all(visible: bool, /):
        for arrow in Arrow.arrows.values():
            arrow.set_visibility(visible)