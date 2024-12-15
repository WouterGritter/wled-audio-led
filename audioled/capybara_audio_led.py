from audioled.audio_led import AudioLED
from wled.wled import WLED


class CapybaraAudioLED(AudioLED):
    def __init__(self, name: str, display_name: str, wled: WLED):
        super().__init__(
            name,
            display_name,
            wled,
            ['off', 'on'],
        )

    def update(self, value: float) -> None:
        state = self.get_current_mode()
        if state == 'off':
            return

        color = self.get_current_color()
        self.get_wled().update([(
            value * color[0],
            value * color[1],
            value * color[2],
        )] * 6)

    def is_valid_color(self, color: tuple[float, float, float]) -> bool:
        return super().is_valid_color(color) and color[0] == color[1] == color[2]
