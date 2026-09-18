
from generators.base import Generator
from jungle.sead import sarc, yaz0

import ninty.yaz0
import random


class Yaz0Generator(Generator):
    def __init__(self):
        super().__init__("yaz0")
        self._generators = {
            "simple.szs": self.generate_simple,
            "random.szs": self.generate_random,
            "weak.szs": self.generate_weak,
            "alignment.szs": self.generate_alignment
        }
    
    def generate_simple(self) -> None:
        data = b"Hello" * 20

        file = yaz0.Yaz0File()
        file.size = len(data)
        file.data = ninty.yaz0.compress(data, 4096)
        return file.save()
    
    def generate_random(self) -> None:
        # Generate 8 KB of random data with a constant seed
        random.seed(123)
        data = bytes(random.getrandbits(8) for i in range(8192))
        
        file = yaz0.Yaz0File()
        file.size = len(data)
        file.data = ninty.yaz0.compress(data, 4096)
        return file.save()
    
    def generate_weak(self) -> None:
        data = b"Hello" * 20

        file = yaz0.Yaz0File()
        file.size = len(data)
        file.data = ninty.yaz0.compress(data, 0)
        return file.save()
    
    def generate_alignment(self) -> None:
        archive = sarc.SARCFile()
        archive.alignment = 256
        archive.files["file1.txt"] = b"File 1"
        archive.files["file2.txt"] = b"File 2"
        data = archive.save()

        file = yaz0.Yaz0File()
        file.alignment = 256
        file.size = len(data)
        file.data = ninty.yaz0.compress(data, 4096)
        return file.save()
