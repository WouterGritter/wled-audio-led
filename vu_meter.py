import math
import struct
from threading import Thread

import pyaudio


class VUMeter:
    def __init__(self, rate=44100, frames_per_buffer=702):
        self.__rate = rate
        self.__frames_per_buffer = frames_per_buffer

        self.__last_audio_value = 0

    def start_audio_thread(self):
        thread = Thread(target=self.__audio_thread)
        thread.start()

    def get_last_audio_value(self):
        return self.__last_audio_value

    def __audio_thread(self):
        audio = pyaudio.PyAudio()

        print("Available input devices:")
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info["maxInputChannels"] > 0:
                print(f"Index {i}: {device_info['name']} (Channels: {device_info['maxInputChannels']})")

        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.__rate,
            input=True,
            frames_per_buffer=self.__frames_per_buffer
        )

        try:
            while True:
                data = stream.read(self.__frames_per_buffer, exception_on_overflow=True)

                count = len(data) / 2
                shorts = struct.unpack("%dh" % count, data)
                sum_squares = sum(s ** 2 * (1.0 / 32768.0) ** 2 for s in shorts)
                amplitude = math.sqrt(sum_squares / count)

                self.__last_audio_value = amplitude
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            print('VUMeter audio thread stopped.')
