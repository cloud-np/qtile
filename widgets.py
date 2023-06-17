from libqtile import qtile
import os
from preferences import colors, terminal

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration


def init_widgets_list():
    widgets_list = [
        widget.Sep(linewidth=0, padding=6, foreground=colors[2], background=colors[0]),
        widget.Image(
            filename="~/.config/qtile/icons/python-white.png",
            scale="False",
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(terminal)},
        ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[2], background=colors[0]),
        widget.GroupBox(
            font="JetBrainsMono Bold",
            fontsize=9,
            margin_y=3,
            margin_x=0,
            padding_y=5,
            padding_x=3,
            borderwidth=3,
            active=colors[2],
            inactive=colors[7],
            rounded=False,
            highlight_color=colors[1],
            highlight_method="line",
            this_current_screen_border=colors[6],
            this_screen_border=colors[4],
            other_current_screen_border=colors[6],
            other_screen_border=colors[4],
            foreground=colors[2],
            background=colors[0],
        ),
        widget.TextBox(
            text="|",
            font="JetBrainsMono",
            background=colors[0],
            foreground="474747",
            padding=2,
            fontsize=14,
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[2],
            background=colors[0],
            padding=0,
            scale=0.7,
        ),
        widget.CurrentLayout(foreground=colors[2], background=colors[0], padding=5),
        widget.TextBox(
            text="|",
            font="JetBrainsMono",
            background=colors[0],
            foreground="474747",
            padding=2,
            fontsize=14,
        ),
        widget.WindowName(foreground=colors[6], background=colors[0], padding=0),
        widget.Systray(background=colors[0], padding=5),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.Net(
            interface="enp6s0",
            format="Net: {down} ↓↑ {up}",
            foreground=colors[3],
            background=colors[0],
            padding=5,
            decorations=[
                BorderDecoration(
                    colour=colors[3],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.ThermalSensor(
            foreground=colors[4],
            background=colors[0],
            threshold=90,
            fmt="Temp: {}",
            padding=5,
            decorations=[
                BorderDecoration(
                    colour=colors[4],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.CheckUpdates(
            update_interval=1800,
            distro="Arch_checkupdates",
            display_format="Updates: {updates} ",
            foreground=colors[5],
            colour_have_updates=colors[5],
            colour_no_updates=colors[5],
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(
                    terminal + " -e sudo apt install && sudo apt upgrade"
                )
            },
            padding=5,
            background=colors[0],
            decorations=[
                BorderDecoration(
                    colour=colors[5],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.Memory(
            foreground=colors[9],
            background=colors[0],
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(terminal + " -e htop")},
            fmt="Mem: {}",
            padding=5,
            decorations=[
                BorderDecoration(
                    colour=colors[9],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.Volume(
            foreground=colors[7],
            background=colors[0],
            fmt="Vol: {}",
            padding=5,
            decorations=[
                BorderDecoration(
                    colour=colors[7],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.KeyboardLayout(
            foreground=colors[8],
            background=colors[0],
            fmt="Keyboard: {}",
            padding=5,
            decorations=[
                BorderDecoration(
                    colour=colors[8],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
        widget.Clock(
            background=colors[0],
            face_shape="square",
            face_background=colors[6],
            face_border_colour=colors[6],
            face_border_width=4,
            padding=5,
        ),
        widget.Clock(
            foreground=colors[6],
            background=colors[0],
            format="%A, %B %d - %H:%M ",
            decorations=[
                BorderDecoration(
                    colour=colors[6],
                    border_width=[0, 0, 2, 0],
                    padding_x=5,
                    padding_y=None,
                )
            ],
        ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[0], background=colors[0]),
    ]
    return widgets_list


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[
        9:10
    ]  # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2  # Monitor 2 will display all widgets in widgets_list
