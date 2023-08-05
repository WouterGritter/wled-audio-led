import time
from threading import Thread

from audioled.audio_led_repository import AudioLEDRepository
from vu_meter import VUMeter


class AudioLedController:
    def __init__(self, audio_led_repository: AudioLEDRepository, vu_meter: VUMeter, update_rate=60, lerp_factor=0.5):
        self.__audio_led_repository = audio_led_repository
        self.__vu_meter = vu_meter
        self.__update_rate = update_rate
        self.__lerp_factor = lerp_factor

    def start_led_thread(self):
        thread = Thread(target=self.__led_thread)
        thread.start()

    def update_leds(self, lerped_value: float):
        for audio_led in self.__audio_led_repository.audio_leds:
            audio_led.update(lerped_value)

    def __led_thread(self):
        min_rms = float("inf")
        max_rms = -float("inf")

        lerped_value = 0

        while True:
            start_time = time.time()

            last_audio_value = self.__vu_meter.get_last_audio_value()

            min_rms = min(min_rms, last_audio_value)
            max_rms = max(max_rms, last_audio_value)

            if min_rms == max_rms:
                value = 0
            else:
                value = (last_audio_value - min_rms) / (max_rms - min_rms)

            lerped_value = lerped_value + (value - lerped_value) * self.__lerp_factor

            self.update_leds(lerped_value)

            elapsed = time.time() - start_time
            if elapsed < 1.0 / self.__update_rate:
                time.sleep(1.0 / self.__update_rate - elapsed)
            else:
                print('Can\'t keep up in LED update thread.')
