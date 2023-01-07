from libqtile import widget
from libqtile.widget.battery import BatteryState, BatteryStatus

import subprocess

class MyBattery(widget.Battery):
    icons = {
        'charging': {
            10: '\uf585',
            20: '\uf586',
            30: '\uf586',
            40: '\uf587',
            50: '\uf587',
            60: '\uf588',
            70: '\uf588',
            80: '\uf589',
            90: '\uf58a',
            100: '\uf584'
        },
        'discharging': {
            10: '\uf579',
            20: '\uf57a',
            30: '\uf57b',
            40: '\uf57c',
            50: '\uf57d',
            60: '\uf57e',
            70: '\uf57f',
            80: '\uf580',
            90: '\uf581',
            100: '\uf578'
        }
    }

    def build_string(self, status: BatteryStatus) -> str:
        percentage: int = int(status.percent * 100)
        space = ' '

        if self.layout is not None:
            if status.state == BatteryState.DISCHARGING and status.percent < self.low_percentage:
                self.layout.colour = self.low_foreground
                self.background = self.low_background
            else:
                self.layout.colour = self.foreground
                self.background = self.normal_background

        if status.state == BatteryState.CHARGING:
            space += space # add 2 spaces so the icon and text have the same gap
        return self._battery_icon(status.state, percentage) + space + str(percentage) + '%'

    def _battery_icon(self, state: BatteryState, percentage: int) -> str:
        if state == BatteryState.FULL:
            return '\uf578'
        if state == BatteryState.EMPTY:
            return '\uf58d'
        if state == BatteryState.UNKNOWN:
            return '\uf590'
        low_boundary = percentage // 10 * 10 if percentage >= 10 else 10
        if state == BatteryState.CHARGING:
            return self.icons['charging'][low_boundary]
        if state == BatteryState.DISCHARGING:
            if percentage < 10:
                return '\uf582'
            return self.icons['discharging'][low_boundary]


class MyBrightness(widget.Backlight):
    icons = {
        'min': '\uf5dd',
        'low': '\uf5dc',
        'med': '\uf5de',
        'high': '\uf5df'
    }

    def _current_brightness(self) -> int:
        brightness: int = self._load_file(self.brightness_file)
        max_value: int = self._load_file(self.max_brightness_file)

        return int((brightness / max_value) * 100)

    def _current_brightness_icon(self) -> str:
        percentage: int = self._current_brightness()

        if percentage <= 20:
            return self.icons['min']
        elif percentage <= 40:
            return self.icons['low']
        elif percentage <= 60:
            return self.icons['med']
        else:
            return self.icons['high']

    def poll(self) -> str:
        try:
            percent: str = str(self._current_brightness())
            icon: str = self._current_brightness_icon()

        except RuntimeError as e:
            return "Error: {}".format(e)

        return icon + '  ' + percent + '%'

class MyPAVolume(widget.Volume):
    icons = {
        'mute': '\ufa80',
        'low': '\ufa7e',
        'med': '\ufa7f',
        'high': '\ufa7d'
    }

    icon = icons['mute']

    defaults = [
        ('step', 5, 'Steps to increase/decrease volume'),
    ]

    def __init__(self, **config):
        widget.Volume.__init__(self, **config)
        self.add_defaults(self.defaults)
        self.add_callbacks({
            'Button3': self.toggle_mute,
            'Button4': self.increase_vol,
            'Button5': self.decrease_vol,
        })
        self.short_format = 'FFF'

    def volume_cmd(self, *args):
        cmd = ['pamixer']

        cmd.extend([x for x in args])

        return ' '.join(cmd)

    def get_volume(self) -> int:
        try:
            volume: int = int(subprocess.getoutput(self.volume_cmd('--get-volume')))

        except subprocess.CalledProcessError:
            return -1
        check_mute: str = subprocess.getoutput(self.volume_cmd('--get-mute'))

        if check_mute == 'true':
            return -1
        return volume

    def update(self):
        vol = self.get_volume()
        if vol != self.volume:
            self.volume = vol
            self._volume_icon()
            self.bar.draw()
        self.timeout_add(self.update_interval, self.update)

    def _volume_icon(self):
        if self.volume <= 0:
            icon = self.icons['mute']
        elif self.volume <= 30:
            icon = self.icons['low']
        elif self.volume <= 60:
            icon = self.icons['med']
        else:
            icon = self.icons['high']

        if self.volume == -1:
            self.text = self.icons['mute']
        else:
            self.text = icon + '  ' + str(self.volume) + '%'


    def increase_vol(self):
        subprocess.call(self.volume_cmd('-i', str(self.step)), shell = True)

    def decrease_vol(self):
        subprocess.call(self.volume_cmd('-d', str(self.step)), shell = True)

    def toggle_mute(self):
        subprocess.call(self.volume_cmd('--toggle-mute'), shell = True)

class MyClock(widget.Clock):
    defaults = [
        ('format', '%I:%M %p', 'Normal format'),
        ('format_alt', '%a, %b %d', 'Format when mouse is over widget')
    ]

    def __init__(self, **config):
        widget.Clock.__init__(self, **config)
        self.add_defaults(self.defaults)
        self.short_format = self.format

    def mouse_enter(self, *args, **kwargs):
        self.format = self.format_alt
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.format = self.short_format
        self.bar.draw()
