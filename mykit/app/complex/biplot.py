import random as _random
import tkinter as _tk
from typing import (
    Dict as _Dict,
    List as _List,
    Optional as _Optional,
    Tuple as _Tuple,
    Union as _Union
)


class Biplot:

    ## <runtime>

    _page: _tk.Canvas = None
    @staticmethod
    def _set_page(page):
        Biplot._page = page

    biplots: _Dict[str, 'Biplot'] = {}
    biplot_tags: _Dict[str, _List['Biplot']] = {}

    ## </runtime>

    def __init__(
        self,
        points1: _List[_Tuple[float, float]] = [],
        points2: _List[_Tuple[float, float]] = [],

        xmin: _Optional[float] = None,
        xmax: _Optional[float] = None,
        ymin: _Optional[float] = None,
        ymax: _Optional[float] = None,

        width: int = 300,
        height: int = 200,
        tl_x: int = 0,
        tl_y: int = 0,

        pad_x: float = 0.03,
        pad_y: float = 0.07,
        show_tick: bool = True,
        show_grid: bool = True,
        ntick_x: int = 10,
        ntick_y: int = 10,
        tick_len: int = 12,
        arrow_size: int = 7,
        arrow_width: int = 2,

        grid_color: str = '#555',
        axes_color: str = '#ccc',
        axes_label_color: str = '#ccc',

        title: str = '',
        title_color: str = '#fff',
        title_font: _Union[str, tuple] = ('Arial Bold', 15),

        x_axis_label: str = '',
        x_axis_label_shift: int = 15,
        x_axis_label_font: _Union[str, tuple] = ('Arial Bold', 12),
        y_axis_label: str = '',
        y_axis_label_shift: int = 15,
        y_axis_label_font: _Union[str, tuple] = ('Arial Bold', 12),

        tick_x_prefix: str = '',
        tick_x_suffix: str = '',
        tick_x_shift: int = 0,
        tick_x_font: _Union[str, tuple] = 'Consolas 9',
        tick_x_prec: int = 1,
        tick_y_prefix: str = '',
        tick_y_suffix: str = '',
        tick_y_shift: int = 0,
        tick_y_font: _Union[str, tuple] = 'Consolas 9',
        tick_y_prec: int = 1,
        tick_color: str = '#ccc',

        plot_color1: str = '#7f7',
        plot_color2: str = '#f77',
        plot_thick: int = 1,  # line width

        show_points: bool = False,
        points_rad: int = 7,
        points_color: str = '#a77',
        points_border: str = '#eee',

        legend1: _Optional[str] = None,
        legend2: _Optional[str] = None,
        legends_bar_width: int = 30,
        legends_bar_height: int = 6,
        legends_pad_x: int = 7,
        legends_pad_y: int = 20,
        legends_font: _Union[str, tuple] = ('Arial Bold', 13),
        legends_color: str = '#f5f5f5',
        legends_shift_x: int = 30,
        legends_shift_y: int = 10,

        visible: bool = True,

        id: _Optional[str] = None,
        tags: _Optional[_Union[str, _List[str]]] = None,
    ):
        """
        Please ensure that `points1` and `points2` always have the same length.
        The graph can be displayed without any given points,
        but in order to show the plot, two points need to be specified.

        ---
        
        ## Params
        - `xrange`: if `None` -> using the x-range from `points`
        - `yrange`: if `None` -> using the y-range from `points`
        """

        ## <dependencies check>

        ## reminder: Biplot isn't actually a widget. it can be used as a utility
        ##           outside App's purposes. so just use Biplot._set_page to achieve it.
        if Biplot._page is None:
            raise AssertionError('Can\'t use widgets before App initialized.')
        
        ## </dependencies check>

        self.points1 = points1
        self.points2 = points2

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        self.width = width
        self.height = height
        self.tl_x = tl_x
        self.tl_y = tl_y

        self.pad_x = pad_x
        self.pad_y = pad_y
        self.show_tick = show_tick
        self.show_grid = show_grid
        self.ntick_x = ntick_x
        self.ntick_y = ntick_y
        self.tick_len = tick_len
        self.arrow_size = arrow_size
        self.arrow_width = arrow_width

        self.grid_color = grid_color
        self.axes_color = axes_color
        self.axes_label_color = axes_label_color

        self.title = title
        self.title_color = title_color
        self.title_font = title_font

        self.x_axis_label = x_axis_label
        self.x_axis_label_shift = x_axis_label_shift
        self.x_axis_label_font = x_axis_label_font
        self.y_axis_label = y_axis_label
        self.y_axis_label_shift = y_axis_label_shift
        self.y_axis_label_font = y_axis_label_font

        self.tick_x_prefix = tick_x_prefix
        self.tick_x_suffix = tick_x_suffix
        self.tick_x_shift = tick_x_shift
        self.tick_x_font = tick_x_font
        self.tick_x_prec = tick_x_prec
        self.tick_y_prefix = tick_y_prefix
        self.tick_y_suffix = tick_y_suffix
        self.tick_y_shift = tick_y_shift
        self.tick_y_font = tick_y_font
        self.tick_y_prec = tick_y_prec
        self.tick_color = tick_color

        self.plot_color1 = plot_color1
        self.plot_color2 = plot_color2
        self.plot_thick = plot_thick

        self.show_points = show_points
        self.points_rad = points_rad
        self.points_color = points_color
        self.points_border = points_border

        self.legend1 = legend1
        self.legend2 = legend2
        self.legends_bar_width = legends_bar_width
        self.legends_bar_height = legends_bar_height
        self.legends_pad_x = legends_pad_x
        self.legends_pad_y = legends_pad_y
        self.legends_font = legends_font
        self.legends_color = legends_color
        self.legends_shift_x = legends_shift_x
        self.legends_shift_y = legends_shift_y

        self.visible = visible

        ## <id>

        ## `self.id`: to make sure that we can modify a specific instance without affecting the others
        if id is None:
            self.id = _random.randint(-10000, 10000)
            while self.id in Biplot.biplots:
                self.id = _random.randint(-10000, 10000)
        else:
            self.id = id
            if self.id in Biplot.biplots:
                raise ValueError(f'The id {repr(id)} is duplicated.')
        
        Biplot.biplots[self.id] = self

        ## </id>

        ## <tags>

        if type(tags) is str:
            self.tags = [tags]
        elif (type(tags) is list) or (type(tags) is tuple) or (tags is None):
            self.tags = tags

        if tags is not None:
            for tag in self.tags:
                if tag in Biplot.biplot_tags:
                    Biplot.biplot_tags[tag].append(self)
                else:
                    Biplot.biplot_tags[tag] = [self]
        
        ## </tags>


        ## <preprocessing>
        self.plot_width = width*(1-pad_x)
        self.plot_height = height*(1-pad_y)
        ## </preprocessing>


        ## init
        self._redraw()

    def _redraw(self):
        """redraw the entire graph"""

        ## 2 points need to be specified in order to draw the graph
        if len(self.points1) < 3:
            self.points1 = [(0, 0), (1, 0)]
            self.points2 = [(0, 0), (1, 0)]

        x_values = [p[0] for p in self.points1]
        if self.xmin is None:
            XMIN = min(x_values)
        else:
            XMIN = self.xmin
        if self.xmax is None:
            XMAX = max(x_values)
        else:
            XMAX = self.xmax

        y_values = [p[1] for p in (self.points1 + self.points2)]
        if self.ymin is None:
            YMIN = min(y_values)
        else:
            YMIN = self.ymin
        if self.ymax is None:
            YMAX = max(y_values)
        else:
            YMAX = self.ymax

        LEN_X = XMAX - XMIN
        LEN_Y = YMAX - YMIN


        ## title
        Biplot._page.create_text(
            self.tl_x+self.width/2, self.tl_y,
            text=self.title, font=self.title_font, fill=self.title_color,
            tags=f'Biplot_{self.id}'
        )


        ## grids
        if self.show_grid:

            ## vertical grids
            for x in range(self.ntick_x):
                X = self.tl_x + ((x+1)/self.ntick_x)*self.plot_width
                Biplot._page.create_line(
                    X, self.tl_y+(self.height-self.plot_height),
                    X, self.tl_y+self.height,
                    fill=self.grid_color, width=1, tags=f'Biplot_{self.id}'
                )

            ## horizontal grids
            for y in range(self.ntick_y):
                Y = self.tl_y+self.height - ((y+1)/self.ntick_y)*self.plot_height
                Biplot._page.create_line(
                    self.tl_x                , Y,
                    self.tl_x+self.plot_width, Y,
                    fill=self.grid_color, width=1, tags=f'Biplot_{self.id}'
                )


        ## x-axis
        Biplot._page.create_line(
            self.tl_x           , self.tl_y+self.height,
            self.tl_x+self.width, self.tl_y+self.height,
            fill=self.axes_color, width=1, tags=f'Biplot_{self.id}'
        )
        ## x-axis arrow
        Biplot._page.create_line(
            self.tl_x+self.width-self.arrow_size, self.tl_y+self.height-self.arrow_size,
            self.tl_x+self.width                , self.tl_y+self.height,
            self.tl_x+self.width-self.arrow_size, self.tl_y+self.height+self.arrow_size,
            fill=self.axes_color, width=self.arrow_width, tags=f'Biplot_{self.id}'
        )
        ## x-axis label
        Biplot._page.create_text(
            self.tl_x+self.width+self.x_axis_label_shift, self.tl_y+self.height,
            text=self.x_axis_label, anchor='w', fill=self.axes_label_color, font=self.x_axis_label_font, tags=f'Biplot_{self.id}'
        )

        ## y-axis
        Biplot._page.create_line(
            self.tl_x, self.tl_y,
            self.tl_x, self.tl_y+self.height,
            fill=self.axes_color, width=1, tags=f'Biplot_{self.id}'
        )
        ## y-axis arrow
        Biplot._page.create_line(
            self.tl_x-self.arrow_size, self.tl_y+self.arrow_size,
            self.tl_x, self.tl_y,
            self.tl_x+self.arrow_size, self.tl_y+self.arrow_size,
            fill=self.axes_color, width=self.arrow_width, tags=f'Biplot_{self.id}'
        )
        ## y-axis label
        Biplot._page.create_text(
            self.tl_x, self.tl_y-self.y_axis_label_shift,
            text=self.y_axis_label, anchor='s', fill=self.axes_label_color, font=self.y_axis_label_font, tags=f'Biplot_{self.id}'
        )


        ## ticks
        if self.show_tick:

            ## x-axis ticks
            for x in range(self.ntick_x+1):
                X = self.tl_x + (x/self.ntick_x)*self.plot_width

                ## tick
                Biplot._page.create_line(
                    X, self.tl_y+self.height-self.tick_len/2,
                    X, self.tl_y+self.height+self.tick_len/2,
                    fill=self.tick_color, width=1, tags=f'Biplot_{self.id}'
                )

                ## tick-label
                _num = XMIN + (x/self.ntick_x)*(LEN_X)
                if self.tick_x_prec == 0:
                    _num = int(_num)
                else:
                    _num = round(_num, self.tick_x_prec)
                text = self.tick_x_prefix + str(_num) + self.tick_x_suffix
                Biplot._page.create_text(
                    X, self.tl_y+self.height+self.tick_len+self.tick_x_shift,
                    text=text, anchor='n', font=self.tick_x_font, fill=self.axes_label_color,
                    tags=(f'Biplot_{self.id}', f'Biplot_{self.id}_ticks')
                )

            ## y-axis ticks
            for y in range(self.ntick_y+1):
                Y = self.tl_y+self.height - (y/self.ntick_y)*self.plot_height

                ## tick
                Biplot._page.create_line(
                    self.tl_x-self.tick_len/2, Y,
                    self.tl_x+self.tick_len/2, Y,
                    fill=self.tick_color, width=1, tags=f'Biplot_{self.id}'
                )

                ## tick-label
                _num = YMIN + (y/self.ntick_y)*(LEN_Y)
                if self.tick_y_prec == 0:
                    _num = int(_num)
                else:
                    _num = round(_num, self.tick_y_prec)
                text = self.tick_y_prefix + str(_num) + self.tick_y_suffix
                Biplot._page.create_text(
                    self.tl_x-self.tick_len-self.tick_y_shift, Y,
                    text=text, anchor='e', font=self.tick_y_font, fill=self.axes_label_color,
                    tags=(f'Biplot_{self.id}', f'Biplot_{self.id}_ticks')
                )


        ## plot 1
        coords1 = []
        for x, y in self.points1:
            X = self.tl_x + (x - XMIN)*(self.plot_width/LEN_X)
            Y = self.tl_y + self.height - (y - YMIN)*(self.plot_height/LEN_Y)
            coords1.append((X, Y))
        Biplot._page.create_line(
            coords1,
            fill=self.plot_color1, width=self.plot_thick,
            tags=(f'Biplot_{self.id}', f'Biplot_{self.id}_plot')
        )

        ## plot 2
        coords2 = []
        for x, y in self.points2:
            X = self.tl_x + (x - XMIN)*(self.plot_width/LEN_X)
            Y = self.tl_y + self.height - (y - YMIN)*(self.plot_height/LEN_Y)
            coords2.append((X, Y))
        Biplot._page.create_line(
            coords2,
            fill=self.plot_color2, width=self.plot_thick,
            tags=(f'Biplot_{self.id}', f'Biplot_{self.id}_plot')
        )

        if self.show_points:
            for x, y in (coords1 + coords2):
                Biplot._page.create_oval(
                    x-self.points_rad/2, y-self.points_rad/2,
                    x+self.points_rad/2, y+self.points_rad/2,
                    fill=self.points_color, outline=self.points_border, width=1, tags=f'Biplot_{self.id}'
                )
        

        ## legends
        if self.legend1 is not None:
            Biplot._page.create_rectangle(
                self.tl_x+self.legends_shift_x, self.tl_y+self.legends_shift_y,
                self.tl_x+self.legends_shift_x+self.legends_bar_width, self.tl_y+self.legends_shift_y+self.legends_bar_height,
                fill=self.plot_color1, width=0, tags=f'Biplot_{self.id}'
            )
            Biplot._page.create_text(
                self.tl_x+self.legends_shift_x+self.legends_bar_width+self.legends_pad_x,
                self.tl_y+self.legends_shift_y+self.legends_bar_height/2,
                text=self.legend1, font=self.legends_font, justify='left', anchor='w', fill=self.legends_color,
                tags=f'Biplot_{self.id}'
            )
        if self.legend2 is not None:
            Biplot._page.create_rectangle(
                self.tl_x+self.legends_shift_x,
                self.tl_y+self.legends_shift_y+self.legends_pad_y,
                self.tl_x+self.legends_shift_x+self.legends_bar_width,
                self.tl_y+self.legends_shift_y+self.legends_pad_y+self.legends_bar_height,
                fill=self.plot_color2, width=0, tags=f'Biplot_{self.id}'
            )
            Biplot._page.create_text(
                self.tl_x+self.legends_shift_x+self.legends_bar_width+self.legends_pad_x,
                self.tl_y+self.legends_shift_y+self.legends_pad_y+self.legends_bar_height/2,
                text=self.legend2, font=self.legends_font, justify='left', anchor='w', fill=self.legends_color,
                tags=f'Biplot_{self.id}'
            )

    def redraw_plot(self, points1: _List[_Tuple[float, float]], points2: _List[_Tuple[float, float]], /) -> None:
        """
        Redraws the plot and updates the tick labels with a new set of given points.
        """

        ## reminder: to optimize things, only redraw the necessary part
        ##           so the code below is duplicated from `_redraw`.
        ##           it's redundant, but currently the easiest way to
        ##           achieve the desired functionality

        self.points1 = points1
        self.points2 = points2

        ## 2 points need to be specified in order to draw the graph
        if len(self.points1) < 3:
            self.points1 = [(0, 0), (1, 0)]
            self.points2 = [(0, 0), (1, 0)]

        x_values = [p[0] for p in self.points1]
        if self.xmin is None:
            XMIN = min(x_values)
        else:
            XMIN = self.xmin
        if self.xmax is None:
            XMAX = max(x_values)
        else:
            XMAX = self.xmax

        y_values = [p[1] for p in (self.points1 + self.points2)]
        if self.ymin is None:
            YMIN = min(y_values)
        else:
            YMIN = self.ymin
        if self.ymax is None:
            YMAX = max(y_values)
        else:
            YMAX = self.ymax

        ## LEN_X and LEN_Y can't be zero
        LEN_X = max(10**(-self.tick_x_prec), XMAX - XMIN)
        LEN_Y = max(10**(-self.tick_y_prec), YMAX - YMIN)


        ## redraw the ticks

        Biplot._page.delete(f'Biplot_{self.id}_ticks')

        if self.show_tick:

            ## x-axis ticks
            for x in range(self.ntick_x+1):
                X = self.tl_x + (x/self.ntick_x)*self.plot_width

                ## tick-label
                _num = XMIN + (x/self.ntick_x)*(LEN_X)
                if self.tick_x_prec == 0:
                    _num = int(_num)
                else:
                    _num = round(_num, self.tick_x_prec)
                text = self.tick_x_prefix + str(_num) + self.tick_x_suffix
                Biplot._page.create_text(
                    X, self.tl_y+self.height+self.tick_len+self.tick_x_shift,
                    text=text, anchor='n', font=self.tick_x_font, fill=self.axes_label_color,
                    tags=(f'Biplot_{self.id}', f'Biplot_{self.id}_ticks')
                )

            ## y-axis ticks
            for y in range(self.ntick_y+1):
                Y = self.tl_y+self.height - (y/self.ntick_y)*self.plot_height

                ## tick-label
                _num = YMIN + (y/self.ntick_y)*(LEN_Y)
                if self.tick_y_prec == 0:
                    _num = int(_num)
                else:
                    _num = round(_num, self.tick_y_prec)
                text = self.tick_y_prefix + str(_num) + self.tick_y_suffix
                Biplot._page.create_text(
                    self.tl_x-self.tick_len-self.tick_y_shift, Y,
                    text=text, anchor='e', font=self.tick_y_font, fill=self.axes_label_color,
                    tags=(f'Biplot_{self.id}', f'Biplot_{self.id}_ticks')
                )


        ## redraw the plot

        Biplot._page.delete(f'Biplot_{self.id}_plot')

        ## plot 1
        coords1 = []
        for x, y in self.points1:
            X = self.tl_x + (x - XMIN)*(self.plot_width/LEN_X)
            Y = self.tl_y + self.height - (y - YMIN)*(self.plot_height/LEN_Y)
            coords1.append((X, Y))
        Biplot._page.create_line(
            coords1,
            fill=self.plot_color1, width=self.plot_thick,
            tags=(f'Biplot_{self.id}', f'Biplot_{self.id}_plot')
        )

        ## plot 2
        coords2 = []
        for x, y in self.points2:
            X = self.tl_x + (x - XMIN)*(self.plot_width/LEN_X)
            Y = self.tl_y + self.height - (y - YMIN)*(self.plot_height/LEN_Y)
            coords2.append((X, Y))
        Biplot._page.create_line(
            coords2,
            fill=self.plot_color2, width=self.plot_thick,
            tags=(f'Biplot_{self.id}', f'Biplot_{self.id}_plot')
        )

    def shift_plot(self, new_points1: _List[_Tuple[float, float]], new_points2: _List[_Tuple[float, float]], /) -> None:
        """
        Shifts the plot by inserting `new_points` and removing the leftmost points.
        For example, if 2 pairs are inserted, 2 leftmost pairs will be removed.
        Make sure that the new x values are always greater than the rightmost x value.
        For instance, if the current rightmost x is 100, the new x values
        should follow a sequence like 100, 101, 102.
        """
        
        n_new = len(new_points1)
        
        points1 = self.points1[n_new:] + new_points1
        points2 = self.points2[n_new:] + new_points2
        
        self.redraw_plot(points1, points2)

    def add_point(self, point1: _Tuple[float, float], point2: _Tuple[float, float], max: _Optional[int] = None):
        """
        Adding the new point to the current plot.
        If a max value is specified (e.g., max=100), and the total number of points
        exceeds 100, the plot will shift by inserting the new point and removing
        the leftmost point. If max is not specified, the point will simply be added.
        """

        points1 = self.points1
        points2 = self.points2

        if max is None:
            points1.append(point1)
            points2.append(point2)
            self.redraw_plot(points1, points2)
        else:
            if len(points1) < max:
                points1.append(point1)
                points2.append(point2)
                self.redraw_plot(points1, points2)
            else:
                self.shift_plot([point1], [point2])


    def set_visibility(self, visible: bool, /):
        if self.visible is not visible:
            self.visible = visible
            self._redraw()

    @staticmethod
    def set_visibility_by_id(id: str, visible: bool, /):
        Biplot.biplots[id].set_visibility(visible)

    @staticmethod
    def set_visibility_by_tag(tag: str, visible: bool, /):
        for bp in Biplot.biplot_tags[tag]:
            bp.set_visibility(visible)

    @staticmethod
    def set_visibility_all(visible: bool, /):
        for bp in Biplot.biplots.values():
            bp.set_visibility(visible)