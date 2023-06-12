import tkinter as _tk
import typing as _typing


def graph2d(
    page: _tk.Canvas,
    points: list[tuple[float, float]],
    xmin: _typing.Optional[float] = None,
    xmax: _typing.Optional[float] = None,
    ymin: _typing.Optional[float] = None,
    ymax: _typing.Optional[float] = None,

    width: int = 300,
    height: int = 200,
    pos: tuple[int, int] = (0, 0),
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
    title_font: str | tuple = ('Arial Bold', 15),

    x_axis_label: str = '',
    x_axis_label_shift: int = 15,
    x_axis_label_font: str | tuple = ('Arial Bold', 12),
    y_axis_label: str = '',
    y_axis_label_shift: int = 15,
    y_axis_label_font: str | tuple = ('Arial Bold', 12),

    tick_x_prefix: str = '',
    tick_x_suffix: str = '',
    tick_x_shift: int = 0,
    tick_x_font: str | tuple = 'Consolas 9',
    tick_y_prefix: str = '',
    tick_y_suffix: str = '',
    tick_y_shift: int = 0,
    tick_y_font: str | tuple = 'Consolas 9',
    tick_color: str = '#ccc',

    graph_color: str = '#7f7',
    graph_width: int = 1,

    show_points: bool = False,
    points_rad: int = 7,
    points_color: str = '#a77',
    points_border: str = '#eee',
):
    """
    if `xrange` is None, using the x-range from `points`
    if `yrange` is None, using the y-range from `points`
    `pos`: the position of graph top-left corner
    """
    
    TL_X, TL_Y = pos

    x_values = [p[0] for p in points]
    if xmin is None:
        xmin = min(x_values)
    if xmax is None:
        xmax = max(x_values)

    y_values = [p[1] for p in points]
    if ymin is None:
        ymin = min(y_values)
    if ymax is None:
        ymax = max(y_values)

    len_x = xmax - xmin
    len_y = ymax - ymin

    WIDTH = width*(1-pad_x)
    HEIGHT = height*(1-pad_y)


    ## title
    page.create_text(
        TL_X + width/2, TL_Y,
        text=title, font=title_font, fill=title_color, tags='graph2d'
    )


    ## z-order: grids -> axes -> ticks -> graph


    ## grids
    if show_grid:
        ## vertical grids
        for x in range(ntick_x):
            page.create_line(
                TL_X + ((x+1)/ntick_x)*WIDTH, TL_Y + (height - HEIGHT),
                TL_X + ((x+1)/ntick_x)*WIDTH, TL_Y + height,
                fill=grid_color, width=1, tags='graph2d'
            )
        ## horizontal grids
        for y in range(ntick_y):
            page.create_line(
                TL_X, TL_Y + (height - HEIGHT) + (y/ntick_y)*HEIGHT,
                TL_X + WIDTH, TL_Y + (height - HEIGHT) + (y/ntick_y)*HEIGHT,
                fill=grid_color, width=1, tags='graph2d'
            )

    ## x-axis
    page.create_line(
        TL_X, TL_Y + height,
        TL_X + width, TL_Y + height,
        fill=axes_color, width=1, tags='graph2d'
    )
    ## x-axis arrow
    page.create_line(
        TL_X + width - arrow_size, TL_Y + height - arrow_size,
        TL_X + width, TL_Y + height,
        TL_X + width - arrow_size, TL_Y + height + arrow_size,
        fill=axes_color, width=arrow_width, tags='graph2d'
    )
    ## x-axis label
    page.create_text(
        TL_X + width + x_axis_label_shift, TL_Y + height,
        text=x_axis_label, anchor='w', fill=axes_label_color, font=x_axis_label_font, tags='graph2d'
    )
    ## y-axis
    page.create_line(
        TL_X, TL_Y,
        TL_X, TL_Y + height,
        fill=axes_color, width=1, tags='graph2d'
    )
    ## y-axis arrow
    page.create_line(
        TL_X - arrow_size, TL_Y + arrow_size,
        TL_X, TL_Y,
        TL_X + arrow_size, TL_Y + arrow_size,
        fill=axes_color, width=arrow_width, tags='graph2d'
    )
    ## y-axis label
    page.create_text(
        TL_X, TL_Y - y_axis_label_shift,
        text=y_axis_label, anchor='s', fill=axes_label_color, font=y_axis_label_font, tags='graph2d'
    )

    ## ticks
    if show_tick:
        ## x-axis ticks
        for x in range(ntick_x + 1):
            X = TL_X + (x/ntick_x)*WIDTH
            page.create_line(
                X, TL_Y + height - tick_len/2,
                X, TL_Y + height + tick_len/2,
                fill=tick_color, width=1, tags='graph2d'
            )
            page.create_text(
                X, TL_Y + height + tick_len + tick_x_shift,
                text=f'{tick_x_prefix}{round(xmin + (x/ntick_x)*(len_x), 1)}{tick_x_suffix}',
                anchor='n', font=tick_x_font, fill=axes_label_color, tags='graph2d'
            )
        ## y-axis ticks
        for y in range(ntick_y + 1):
            Y = TL_Y + height - (y/ntick_y)*HEIGHT
            page.create_line(
                TL_X - tick_len/2, Y,
                TL_X + tick_len/2, Y,
                fill=tick_color, width=1, tags='graph2d'
            )
            page.create_text(
                TL_X - tick_len - tick_y_shift, Y,
                text=f'{tick_y_prefix}{round(ymin + (y/ntick_y)*(len_y), 1)}{tick_y_suffix}',
                anchor='e', font=tick_y_font, fill=axes_label_color, tags='graph2d'
            )

    ## graph
    coords = []
    for x, y in points:
        X = TL_X + (x - xmin)*(WIDTH/len_x)
        Y = TL_Y + height - (y - ymin)*(HEIGHT/len_y)
        coords.append((X, Y))
    page.create_line(coords, fill=graph_color, width=graph_width, tags='graph2d')

    if show_points:
        for x, y in coords:
            page.create_oval(
                x - points_rad/2, y - points_rad/2,
                x + points_rad/2, y + points_rad/2,
                fill=points_color, outline=points_border, tags='graph2d', width=1
            )