import os
import socket
import subprocess
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile import layout, bar, hook
from libqtile.dgroups import simple_key_binder
from libqtile.lazy import lazy
from typing import List  # noqa: F401

from widgets import init_widgets_list, init_widgets_screen1, init_widgets_screen2

from preferences import colors, mod, terminal, browser, secondary_browser
import subprocess


def toggle_keyboard_layout():
    output = subprocess.check_output(['setxkbmap', '-query']).decode()
    layout_line = next(line for line in output.splitlines() if 'layout' in line)
    layout = layout_line.split()[1]

    if layout == 'us':
        subprocess.run(['setxkbmap', 'gr'])
    else:
        subprocess.run(['setxkbmap', 'us'])

# My screen are placed in reverse order physically (:
def move_window_to_screen_group_at_left(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i > 0:
        other_screen = qtile.screens[i - 1]
        if other_screen and other_screen.group:
            qtile.current_window.togroup(other_screen.group.name)


def move_window_to_screen_group_at_right(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i <= 0:
        other_screen = qtile.screens[i + 1]
        if other_screen and other_screen.group:
            qtile.current_window.togroup(other_screen.group.name)


keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(terminal), desc="Launches My Terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Bravebrowser"),
    Key([mod, "shift"], "b", lazy.spawn(secondary_browser), desc="Firefox"),
    Key([mod], "v", lazy.spawn("pavucontrol"), desc="Audio Controll"),
    Key([mod], "g", lazy.spawn("lutris"), desc="Gaming/Lutris"),
    Key([mod, "shift"], "v", lazy.spawn("blueman-manager"), desc="Bluetooth Manager"),
    Key([mod], "s", lazy.spawn("spotify"), desc="Spotify"),
    Key([mod], "d", lazy.spawn("discord"), desc="Discord"),
    # To avoid passing qtile to the function, we use lambda for style points (:
    Key([mod], "BackSpace", lazy.function(lambda _: toggle_keyboard_layout())),

    Key([], "Print", lazy.spawn("flameshot gui"), desc="Screenshot"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle through layouts"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Restart Qtile"),
    Key(["control", "shift"], "r", lazy.spawncmd(), desc="Run programs"),
    # Key([mod, "shift"], "q", lazy.spawn("dm-logout"), desc="Logout menu"),
    # Key([mod, "shift"], "Return", lazy.spawn("dm-run"), desc="Run Launcher"),
    Key(["control", "shift"], "w", lazy.window.kill(), desc="Kill active window"),
    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.prev_screen(), desc="Move focus to prev monitor"),
    # Treetab controls
    Key(
        [mod, "control"],
        "h",
        lazy.layout.swap_left(),
        desc="Swap with left window in treetab",
    ),
    Key(
        [mod, "control"],
        "l",
        lazy.layout.swap_right(),
        desc="Swap with right window in treetab",
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.swap_up(),
        desc="Swap with up window in treetab",
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.swap_down(),
        desc="Swap with down window in treetab",
    ),
    # Window controls
    Key([mod], "j", lazy.layout.down(), desc="Move focus down in current stack pane"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up in current stack pane"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), lazy.layout.section_down(), desc="Move windows down in current stack"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), lazy.layout.section_up(), desc="Move windows up in current stack"),
    Key([mod, "shift"], "l", lazy.function(move_window_to_screen_group_at_left), lazy.next_screen(),
        desc="Move window to the group at left (virtually at left)."),
    Key([mod, "shift"], "h", lazy.function(move_window_to_screen_group_at_right), lazy.next_screen(),
        desc="Move window to the group at left (virtually at left)."),
    Key([mod, "control"], "m", lazy.next_screen(), desc="Move windows up in current stack"),
    Key(
        [mod],
        "l",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc="Shrink window (MonadTall), decrease number in master pane (Tile)",
    ),
    Key(
        [mod],
        "h",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc="Expand window (MonadTall), increase number in master pane (Tile)",
    ),
    Key([mod], "n", lazy.layout.normalize(), desc="normalize window size ratios"),
    Key(
        [mod],
        "m",
        lazy.layout.maximize(),
        desc="toggle window between minimum and maximum sizes",
    ),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    # Stack controls
    Key(
        [mod, "shift"],
        "Tab",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc="Switch which side main pane occupies (XmonadTall)",
    ),
    Key(
        [mod],
        "space",
        lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack",
    ),
    Key(
        [mod, "shift"],
        "space",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
]

groups = [
    Group("DEV", layout="monadtall"),
    Group("WWW", layout="monadtall"),
    Group("SYS", layout="monadtall"),
    Group("CHAT", layout="monadtall"),
    Group("MUS", layout="monadtall"),
    Group("GFX", layout="floating"),
    Group("7", layout="monadtall"),
    Group("8", layout="monadtall"),
    Group("9", layout="monadtall"),
]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {
    "border_width": 2,
    "margin": 10,
    "border_focus": "da8548",
    "border_normal": "1D2330",
}

layouts = [
    layout.MonadWide(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Stack(stacks=2, **layout_theme),
    # layout.Columns(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.VerticalTile(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
        font="JetBrainsMono",
        fontsize=10,
        sections=["FIRST", "SECOND", "THIRD", "FOURTH"],
        section_fontsize=10,
        border_width=2,
        bg_color="1c1f24",
        active_bg="eb235f",
        active_fg="000000",
        inactive_bg="a9a1e1",
        inactive_fg="1c1f24",
        padding_left=0,
        padding_x=0,
        padding_y=5,
        section_top=10,
        section_bottom=20,
        level_shift=8,
        vspace=3,
        panel_width=200,
    ),
    layout.Floating(**layout_theme),
]


prompt = f"{os.environ['USER']}@{socket.gethostname()}: "

# DEFAULT WIDGET SETTINGS
widget_defaults = dict(
    font="JetBrainsMono Bold", fontsize=10, padding=10, background=colors[2]
)
extension_defaults = widget_defaults.copy()


def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
        Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
    ]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        # default_float_rules include: utility, notification, toolbar, splash, dialog,
        # file_progress, confirm, download and error.
        *layout.Floating.default_float_rules,
        Match(title="Confirmation"),  # tastyworks exit box
        Match(title="Qalculate!"),  # qalculate-gtk
        Match(wm_class="kdenlive"),  # kdenlive
        Match(wm_class="pinentry-gtk-2"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
