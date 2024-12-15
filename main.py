from flask import Flask, request

from audio_led_controller import AudioLedController
from audioled.audio_led import AudioLED
from audioled.audio_led_repository import AudioLEDRepository
from audioled.capybara_audio_led import CapybaraAudioLED
from audioled.action_lights_audio_led import ActionLightsAudioLED
from audioled.balken_audio_led import BalkenAudioLED
from vu_meter import VUMeter
from wled.udpwled import UDPWLED

app = Flask(__name__)

audio_led_repository = AudioLEDRepository([
    CapybaraAudioLED(
        name='capybara',
        display_name='Capybara',
        wled=UDPWLED('10.43.60.187'),
    ),
    # ActionLightsAudioLED(
    #     name='action_lights',
    #     display_name='Action lights',
    #     wled=UDPWLED('10.43.60.238'),
    # ),
    # BalkenAudioLED(
    #     name='balken',
    #     display_name='Balken',
    #     wled=UDPWLED('10.43.60.239'),
    # ),
])

vu_meter = VUMeter()
audio_led_controller = AudioLedController(audio_led_repository, vu_meter)


def color_from_tuple(color):
    try:
        return {
            'r': color[0],
            'g': color[1],
            'b': color[2],
        }
    except:
        return None


def color_to_tuple(color):
    try:
        return float(color['r']), float(color['g']), float(color['b'])
    except:
        return None


def describe_audio_led(audio_led: AudioLED):
    return {
        'name': audio_led.get_name(),
        'displayName': audio_led.get_display_name(),
        'currentMode': audio_led.get_current_mode(),
        'currentColor': color_from_tuple(audio_led.get_current_color()),
        'availableModes': audio_led.get_available_modes(),
    }


@app.route('/')
def route_root():
    return [describe_audio_led(x) for x in audio_led_repository.audio_leds]


@app.route('/<name>')
def route_get_audio_led(name):
    audio_led = audio_led_repository.get_audio_led(name)
    if audio_led is None:
        return {'error': 'Invalid name'}

    return describe_audio_led(audio_led)


@app.route('/<name>', methods=['POST'])
def route_update_audio_led(name):
    audio_led = audio_led_repository.get_audio_led(name)
    if audio_led is None:
        return {'error': 'Invalid name'}

    body = request.get_json()
    new_mode = body.get('currentMode')
    new_color = color_to_tuple(body.get('currentColor'))

    if new_mode is None and new_color is None:
        return {'error': 'No values to update'}

    if new_mode is not None and not audio_led.is_valid_mode(new_mode):
        return {'error': 'Invalid mode'}

    if new_color is not None and not audio_led.is_valid_color(new_color):
        return {'error': 'Invalid color'}

    if new_mode is not None:
        audio_led.set_current_mode(new_mode)

    if new_color is not None:
        audio_led.set_current_color(new_color)

    audio_led_repository.store_current_states()

    return describe_audio_led(audio_led)


if __name__ == '__main__':
    audio_led_repository.load_current_states()
    vu_meter.start_audio_thread()
    audio_led_controller.start_led_thread()

    app.run('0.0.0.0', 1338)
