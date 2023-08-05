from abc import ABC, abstractmethod


class WLED(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def update(self, data: list[tuple[float, float, float]]) -> None:
        pass
