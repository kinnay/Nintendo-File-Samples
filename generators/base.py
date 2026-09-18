
from typing import Callable

import os


class Generator:
    _folder: str

    _generators: dict[str, Callable[[], bytes]]

    def __init__(self, folder: str):
        self._folder = folder
        self._generators = {}
    
    def generate(self) -> None:
        for name, callback in self._generators.items():
            data = callback()

            path = os.path.join(self._folder, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "wb") as f:
                f.write(data)
