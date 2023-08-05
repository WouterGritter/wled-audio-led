import json
from typing import Optional

from audioled.audio_led import AudioLED


class AudioLEDRepository:
    def __init__(self, audio_leds: Optional[list[AudioLED]] = None, states_file: str = 'states.json'):
        self.audio_leds = audio_leds or []
        self.states_file = states_file

    def get_audio_led(self, name: str) -> Optional[AudioLED]:
        for x in self.audio_leds:
            if x.get_name() == name:
                return x

        return None

    def store_current_states(self):
        states = [x.to_state() for x in self.audio_leds]

        with open(self.states_file, 'w') as f:
            json.dump(states, f)

    def load_current_states(self):
        with open(self.states_file, 'r') as f:
            states = json.load(f)

        for state in states:
            audio_led = self.get_audio_led(state['name'])
            if audio_led is None:
                continue

            audio_led.from_state(state)
