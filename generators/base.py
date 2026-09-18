
from typing import Callable

import os


class Generator:
    _folder: str

    _generators: dict[str, Callable[[], bytes]]

    def __init__(self, folder: str):
        self._folder = os.path.join("files", folder)
        self._generators = {}
    
    def generate(self) -> None:
        self._generate_files()
        self._generate_readme()

    def _generate_files(self) -> None:
        for name, callback in self._generators.items():
            data = callback()

            path = os.path.join(self._folder, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "wb") as f:
                f.write(data)

    def _generate_readme(self) -> None:
        readme = self._sanitize(self.__doc__) + "\n\n"
        readme += "| File | Description |\n"
        readme += "| --- | --- |\n"
        for name, callback in self._generators.items():
            info = self._sanitize(callback.__doc__)
            readme += "| `" + name + "` | " + info + " |\n"

        with open(os.path.join(self._folder, "README.md"), "w") as f:
            f.write(readme)

    def _sanitize(self, text: str) -> str:
        text = text.replace("\n", " ")
        while "  " in text:
            text = text.replace("  ", " ")
        return text.strip()


