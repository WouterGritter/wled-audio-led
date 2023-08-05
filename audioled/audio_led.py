from abc import ABC, abstractmethod

from wled.wled import WLED


class AudioLED(ABC):
    def __init__(self, name: str, display_name: str, wled: WLED, available_modes: list[str]):
        self.__name = name
        self.__display_name = display_name
        self.__wled = wled
        self.__available_modes = available_modes

        self.__current_mode: str = available_modes[0]
        self.__current_color: tuple[float, float, float] = (1.0, 1.0, 1.0)

    @abstractmethod
    def update(self, value: float) -> None:
        pass

    def to_state(self) -> dict:
        return {
            'name': self.__name,
            'current_mode': self.__current_mode,
            'current_color': {
                'r': self.__current_color[0],
                'g': self.__current_color[1],
                'b': self.__current_color[2],
            },
        }

    def from_state(self, state: dict) -> None:
        assert state['name'] == self.__name

        self.set_current_mode(state['current_mode'])

        self.set_current_color((
            state['current_color']['r'],
            state['current_color']['g'],
            state['current_color']['b'],
        ))

    def get_name(self) -> str:
        return self.__name

    def get_display_name(self) -> str:
        return self.__display_name

    def get_wled(self) -> WLED:
        return self.__wled

    def get_available_modes(self) -> list[str]:
        return self.__available_modes.copy()

    def get_current_mode(self) -> str:
        return self.__current_mode

    def is_valid_mode(self, mode: str) -> bool:
        return mode in self.__available_modes

    def set_current_mode(self, mode: str) -> None:
        assert self.is_valid_mode(mode)
        self.__current_mode = mode

    def is_valid_color(self, color: tuple[float, float, float]) -> bool:
        return (
                color is not None and
                0 <= color[0] <= 1 and
                0 <= color[1] <= 1 and
                0 <= color[2] <= 1
        )

    def get_current_color(self) -> tuple[float, float, float]:
        return self.__current_color

    def set_current_color(self, color: tuple[float, float, float]) -> None:
        assert self.is_valid_color(color)
        self.__current_color = color
