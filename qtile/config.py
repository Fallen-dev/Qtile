import os
import subprocess

from libqtile import bar, hook, layout, widget
from libqtile.config import Drag, Group, Match, Key, Screen
from libqtile.dgroups import simple_key_binder
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import myfancywidgets as fancy

### VARIABLES
theme = 'dark' # light / dark

homepath = os.getenv('HOME', os.path.expanduser('~'))
homeuser = os.getenv('USER', 'User')

mod = 'mod1' # mod -> main key / mod1 -> Alt
super = 'mod4' # super -> windows key / mod4 windows key

screenshooter = 'scrot' # install scrot
screenshotPath = homepath + '/Pictures/Screenshots/'
screenshotFileName = 'Screenshot_%d-%m-%y.png'
screenshot = screenshooter + ' ' + screenshotPath + screenshotFileName

appLauncher = 'rofi -show' # install rofi

brightnessUp = 'xbacklight -inc 5%'
brightnessDown = 'xbacklight -dec 5%'

terminal = 'kitty' or guess_terminal() # install kitty or any terminal

volumeUp = 'pamixer -i 5' # install pulseaudio
volumeDown = 'pamixer -d 5'
volumeMute = 'pamixer --toggle-mute'

floating_types = ['notification', 'pinentry', 'toolbar', 'splash', 'dialog']

# list of applications
browsers = ['firefox', 'google-chrome', 'falkon', 'midori']
editors = ['code', 'atom', 'kate', 'nvim', 'vim', 'gedit']

# qtile defaults
dgroups_key_binder = simple_key_binder(mod)
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = 'smart'
reconfigure_screens = True
auto_minimize = True
wmname = 'Resha'

### HOOKS
@hook.subscribe.startup_once
def autostart():
    subprocess.call([homepath + '/.config/qtile/autostart'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

keys = [
    # move focus with arrow keys
    Key([super], "Left", lazy.layout.left()),
    Key([super], "Right", lazy.layout.right()),
    Key([super], "Up", lazy.layout.up()),
    Key([super], "Down", lazy.layout.down()),

    # move focus with arrow keys
    Key([super, 'shift'], "Left", lazy.layout.shuffle_left()),
    Key([super, 'shift'], "Right", lazy.layout.shuffle_right()),
    Key([super, 'shift'], "Up", lazy.layout.shuffle_up()),
    Key([super, 'shift'], "Down", lazy.layout.shuffle_down()),

    # grow focus window with arrow keys
    Key([super, 'control'], "Left", lazy.layout.grow_left()),
    Key([super, 'control'], "Right", lazy.layout.grow_right()),
    Key([super, 'control'], "Up", lazy.layout.grow_up()),
    Key([super, 'control'], "Down", lazy.layout.grow_down()),

    # window and Qtile related
    Key([mod], 'q', lazy.window.kill()),
    Key([mod, 'shift'], 'q', lazy.shutdown()),
    Key([mod, 'shift'], 'r', lazy.reload_config()),
    Key([super, 'shift'], 'n', lazy.layout.normalize()),
    Key([super, 'shift'], 'l', lazy.next_layout()),
    Key([super], 'f', lazy.window.toggle_fullscreen()),
    Key([mod], 'tab', lazy.spawn(appLauncher + 'window -theme rosepine-window.rasi')),

    # spawn applications/programs
    Key([mod], 'Return', lazy.spawn(terminal)),
    Key([mod], 'space', lazy.spawn(appLauncher + ' drun')),
    Key([], 'print', lazy.spawn(screenshot)),
    Key(['shift'], 'print', lazy.spawn(screenshot + ' -s')),

    # Volume keys
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(volumeUp)),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(volumeDown)),
    Key([], 'XF86AudioMute', lazy.spawn(volumeMute)),

    # Brightness keys
    Key([], 'XF86MonBrightnessUp', lazy.spawn(brightnessUp)),
    Key([], 'XF86MonBrightnessDown', lazy.spawn(brightnessDown)),
]

# create screen groups
groups = [
    Group(
        name = 'I',
    ),
    Group(
        name = 'II',
        matches = [Match(wm_class=browsers)]
    ),
    Group(
        name = 'III',
        matches = [Match(wm_class=editors)]
    ),
    Group(name = 'IV')
]


### Rose pine theme [url](https://rosepinetheme.com/palette)
def rosytheme(theme):
    dark = {
        'base':'191724',
        'surface':'1f1d2e',
        'muted':'6e6a86',
        'subtle':'908caa',
        'text':'e0def4',
        'love':'eb6f92',
        'gold':'f6c177',
        'rose':'ebbcba',
        'pine':'31748f',
        'foam':'9ccfd8',
        'iris':'c4a7e7',
        'highlight': '403d52'
    }
    light = {
        'base':'faf4ed',
        'surface':'f2e9e1',
        'muted':'9893a5',
        'subtle':'797593',
        'text':'575279',
        'love':'b4637a',
        'gold':'ea9d34',
        'rose':'d7827e',
        'pine':'286983',
        'foam':'56949f',
        'iris':'907aa9',
        'highlight':'dfdad9'
    }
    if theme.lower() == 'dark':
        return dark
    elif theme.lower() == 'light':
        return light
    return {}

c = rosytheme(theme)


### LAYOUTS
layouts = [
    layout.Columns(
        border_focus = c['iris'],
        border_focus_stack= c['iris'],
        border_normal = c['muted'],
        border_normal_stack = c['muted'],
        border_on_single = True,
        border_width = 5,
        margin = [10, 5, 10, 5],
        margin_on_single = [35, 50, 35, 50],
    ),
    layout.Max(
        border_focus = c['iris'],
        border_normal = c['muted'],
        border_width = 0
    )
]


def myfont(type, weight='regular'):
    if type.lower() == 'sans':
        return 'SF Pro' + ' ' + weight
    return 'JetBrainsMono Nerd Font' + ' ' + weight

def fixspace(bg, padding = 0):
    return widget.Sep(
        background = bg,
        foreground = bg,
        padding = padding
    )

def glyph(bg, fg, side, fill = True):
    if not fill:
        return widget.TextBox(
            fmt = '' if side.lower() == 'left' else '',
            fontsize = 17,
            font = myfont('code'),
            background = bg,
            foreground = fg,
            padding = 0,
            margin = 7
        )
    return widget.TextBox(
        fmt = '' if side.lower() == 'left' else '',
        fontsize = 17,
        font = myfont('code'),
        background = bg,
        foreground = fg,
        padding = 0,
        margin = 7
    )

widget_defaults = dict(
    font = myfont('sans', 'medium'),
    fontsize = 13,
    padding = 5,
    background = c['surface'],
    foreground = c['text']
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                fixspace(c['foam'], padding=2),
                widget.TextBox(
                    fmt = homeuser.capitalize(),
                    font = myfont('sans', 'extrabold'),
                    fontsize = 15,
                    background = c['foam'],
                    foreground = c['base'],
                    mouse_callbacks = {'Button1': lazy.spawn('rofi -show drun')}
                ),
                glyph(c['highlight'], c['foam'], 'right'),
                widget.GroupBox(
                    highlight_method = 'text',
                    background = c['highlight'],
                    foreground = c['text'],
                    active = c['gold'],
                    inactive = c['muted'],
                    urgent_border = c['love'],
                    urgent_text = c['love'],
                    padding_x = 5,
                    font = myfont('sans', 'bold'),
                    fontsize = 15,
                    disable_drag = True,
                    use_mouse_wheel = False
                ),
                glyph(c['surface'], c['highlight'], 'right'),
                fixspace(c['surface'], 3),
                widget.CurrentLayout(font = myfont('code', 'bold italic')),
                glyph(c['surface'], c['subtle'], 'right', False),
                widget.Spacer(),
                widget.Systray(),
                fixspace(c['surface'], 10),
                glyph(c['surface'], c['subtle'], 'left', False),
                widget.Net(
                    format = '{down} ',
                ),
                fixspace(c['surface'], 6),
                fancy.MyBattery(
                    update_interval = 5,
                    low_percentage = 0.2,
                    low_foreground = c['love'],
                    low_background = None,
                    notify_below = 20,
                    show_short_text = False,
                ),
                fancy.MyBrightness(
                    backlight_name = 'intel_backlight',
                    brightness_file = 'brightness',
                    step = 5,
                    update_interval = 0.1
                ),
                fancy.MyPAVolume(
                    limit_max_volume = True,
                ),
                fixspace(c['surface'], 5),
                glyph(c['surface'], c['iris'], 'left'),
                widget.Wlan(
                    background = c['iris'],
                    foreground = c['base'],
                    disconnected_message = '睊',
                    format = '直 {essid}',
                    interface = 'wlp2s0'
                ),
                fixspace(c['iris']),
                glyph(c['iris'], c['gold'], 'left'),
                fancy.MyClock(
                    background = c['gold'],
                    foreground = c['base'],
                ),
                fixspace(c['gold']),
                glyph(c['gold'], c['love'], 'left'),
                widget.QuickExit(
                    background = c['love'],
                    foreground = c['base'],
                    default_text = '襤',
                    countdown_start = 7,
                    countdown_format = '{}s',
                    font = myfont('code', 'medium'),
                    fontsize = 18
                ),
                fixspace(c['love'], 3),
                widget.TextBox(
                    background = c['love'],
                    foreground = c['base'],
                    fmt = '勒',
                    mouse_callbacks = {'Button1': lazy.reload_config()},
                    font = myfont('code', 'medium'),
                    fontsize = 18
                ),
                fixspace(c['love'], 3)
            ],
            22, # bar height
        ),
    ),
]


mouse = [
    Drag([super], 'Button1', lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([super], 'Button3', lazy.window.set_size_floating(), start=lazy.window.get_size())
]
