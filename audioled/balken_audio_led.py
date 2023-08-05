from audioled.audio_led import AudioLED
from wled.wled import WLED


class BalkenAudioLED(AudioLED):
    def __init__(self, name: str, display_name: str, wled: WLED):
        super().__init__(
            name,
            display_name,
            wled,
            ['off', 'single', 'vu'],
        )

    def update(self, value: float) -> None:
        state = self.get_current_mode()
        if state == 'off':
            return

        color = self.get_current_color()

        led_amount = 130

        if state == 'single':
            colored_value = (
                value * color[0],
                value * color[1],
                value * color[2],
            )

            arr = [colored_value] * (2 * led_amount)
            self.get_wled().update(arr)
        elif state == 'vu':
            arr = []
            fadeout_led_amount = 30
            for i in range(0, led_amount):
                if value * (led_amount - fadeout_led_amount) > i:
                    arr.append(color)
                else:
                    dist = i - value * (led_amount - fadeout_led_amount)
                    if dist < 10:
                        colored_dist = (
                            (1 - dist / fadeout_led_amount) * color[0],
                            (1 - dist / fadeout_led_amount) * color[1],
                            (1 - dist / fadeout_led_amount) * color[2],
                        )
                        arr.append(colored_dist)
                    else:
                        arr.append((0, 0, 0))
            arr.reverse()
            self.get_wled().update(arr + arr)
