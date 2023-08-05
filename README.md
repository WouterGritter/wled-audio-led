# WLED-audio-led

Groovy led(strip)s running [WLED](https://github.com/Aircoookie/WLED) on an ESP[8266|32] with
an external audiosource (Raspberry Pi), being controlled over UDP.

WLED already supports this functionality with a better user-interface, however you have to solder a
microphone to the ESP. I didn't want this, because I want the led(strip)s reacting to the music only,
and not the background noise. I have achieved this by connecting the headphones out jack of my
television to a USB audio interface to a Raspberry Pi 4.

The code is highly customized for my own setup, but can be usable as a starting point for your own
groovy led(strip)s. It should be as easy as implementing your own WLED device and animations/logic
in `audioled/audio_led.py` (see `action_lights_audio_led.py` and `balken_audio_led.py` as examples),
and instantiating them at the top of the `main.py` file.


# API endpoints

This project does not contain a user-interface, only the backend API. You'd have to write your own
user-interface. Maybe I'll add a crude UI in the future.

- `GET /` - Get a list of all audio led devices
- `GET /<name>` - Get a specific audio led device
- `POST /<name>` - Update a specific audio led device. Updatable fields are `currentMode` and `currentColor`, formatted in the same way as the GET requests sends them.


## API endpoint examples

In my setup, a `GET /` request returns the following:
```json
[
  {
    "name": "action_lights",
    "displayName": "Action lights",
    "availableModes": [
      "off",
      "on"
    ],
    "currentMode": "on",
    "currentColor": {
      "r": 1.0,
      "g": 1.0,
      "b": 1.0
    }
  },
  {
    "name": "balken",
    "displayName": "Balken",
    "availableModes": [
      "off",
      "single",
      "vu"
    ],
    "currentMode": "vu",
    "currentColor": {
      "r": 1.0,
      "g": 0.0,
      "b": 0.0
    }
  }
]
```

And a valid update request to `POST /balken` could look like the this (note that both `currentMode` and `currentColor` are optional and could be updated separately):
```json
{
  "currentMode": "single",
  "currentColor": {
    "r": 1.0,
    "g": 0.0,
    "b": 1.0
  }
}
```