from abc import ABC, abstractmethod


class PackageSelector(ABC):

    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def run() -> list[str]:
        pass