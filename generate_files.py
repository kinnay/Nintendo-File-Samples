
from jungle.sead import sarc, yaz0

import ninty.yaz0

import os
import random


class Generator:
    _folder: str

    def __init__(self, folder: str):
        self._folder = folder
    
    def generate(self) -> None:
        os.makedirs(self._folder, exist_ok=True)
        for name, callback in self.generators.items():
            data = callback()
            with open(os.path.join(self._folder, name), "wb") as f:
                f.write(data)


class SARCGenerator(Generator):
    def __init__(self):
        super().__init__("sarc")
        self.generators = {
            "empty.sarc": self.generate_empty,
            "simple.sarc": self.generate_simple,
            "sign_extension.sarc": self.generate_sign_extension,
            "alternative_multiplier.sarc": self.generate_alternative_multiplier,
            "big_endian.sarc": self.generate_big_endian,
            "multiple_files.sarc": self.generate_multiple_files,
            "folders.sarc": self.generate_folders,
            "alignment.sarc": self.generate_alignment,
            "hash_collisions.sarc": self.generate_hash_collisions,
            "no_filename.sarc": self.generate_no_filename,
            "complex.sarc": self.generate_complex
        }
    
    def generate_empty(self) -> None:
        file = sarc.SARCFile()
        return file.save()
    
    def generate_simple(self) -> None:
        file = sarc.SARCFile()
        file.files["example.txt"] = b"Hello!"
        return file.save()
    
    def generate_sign_extension(self) -> None:
        file = sarc.SARCFile()
        file.files["❤️.txt"] = "I ❤️ unicode".encode()
        return file.save()
    
    def generate_alternative_multiplier(self) -> None:
        file = sarc.SARCFile()
        file.hash_multiplier = 97
        file.files["example.txt"] = b"Hello!"
        return file.save()
    
    def generate_big_endian(self) -> None:
        file = sarc.SARCFile()
        file.endianness = ">"
        file.files["example.txt"] = b"Hello!"
        return file.save()
    
    def generate_multiple_files(self) -> None:
        file = sarc.SARCFile()
        file.files["file1.txt"] = b"File content 1"
        file.files["file2.txt"] = b"File content 2"
        file.files["file3.txt"] = b"File content 3"
        return file.save()
    
    def generate_folders(self) -> None:
        file = sarc.SARCFile()
        file.files["file1.txt"] = b"Root file 1"
        file.files["file2.txt"] = b"Root file 2"
        file.files["folder1/file1.txt"] = b"Sub file 1"
        file.files["folder1/file2.txt"] = b"Sub file 2"
        file.files["folder2/file.txt"] = b"Sub file 3"
        file.files["folder3/nested/nested/nested/file.txt"] = b"Nested file"
        file.files["notafolder"] = b"Root file 3"
        return file.save()
    
    def generate_alignment(self) -> None:
        file = sarc.SARCFile()
        file.alignment = 4096
        file.files["file1"] = b"Aligned file 1"
        file.files["file2"] = b"Aligned file 2"
        return file.save()
    
    def generate_hash_collisions(self) -> None:
        file = sarc.SARCFile()
        file.hash_multiplier = 53
        file.files["xxxx"] = b"File 1"
        file.files["xxyC"] = b"File 2"
        file.files["xyCx"] = b"File 3"
        file.files["yCxx"] = b"File 4"
        return file.save()
    
    def generate_no_filename(self) -> None:
        hash1 = sarc.calculate_hash("example1.txt", 101, False)
        hash2 = sarc.calculate_hash("example2.txt", 101, False)
        hash3 = sarc.calculate_hash("example3.txt", 101, False)

        file = sarc.SARCFile()
        file.unnamed_files[hash1] = b"File 1"
        file.unnamed_files[hash2] = b"File 2"
        file.unnamed_files[hash3] = b"File 3"
        return file.save()
    
    def generate_complex(self) -> None:
        hash = sarc.calculate_hash("example.txt", 53, False)

        file = sarc.SARCFile()
        file.endianness = ">"
        file.hash_multiplier = 53
        file.alignment = 512
        file.files["xxxx"] = b"File 1"
        file.files["xxyC"] = b"File 2"
        file.files["folder/❤️.txt"] = b"File 3"
        file.unnamed_files[hash] = b"File 4"
        return file.save()


class Yaz0Generator(Generator):
    def __init__(self):
        super().__init__("yaz0")
        self.generators = {
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


def main() -> None:
    for cls in Generator.__subclasses__():
        instance = cls()
        instance.generate()

if __name__ == "__main__":
    main()
