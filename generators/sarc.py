
from generators.base import Generator
from jungle.sead import sarc


class SARCGenerator(Generator):
    """
    This folder contains test cases for the
    [SARC file format](https://nintendo-formats.com/libs/sead/sarc.html).
    """

    def __init__(self):
        super().__init__("sarc")
        self._generators = {
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
        """The most basic test case, an empty archive."""
        file = sarc.SARCFile()
        return file.save()
    
    def generate_simple(self) -> None:
        """A simple archive that contains a single file."""
        file = sarc.SARCFile()
        file.files["example.txt"] = b"Hello!"
        return file.save()
    
    def generate_sign_extension(self) -> None:
        """
        An archive that contains unicode characters in a filename. This can be
        used to test the sign extension behavior of Nintendo Switch games.
        """
        file = sarc.SARCFile()
        file.files["❤️.txt"] = "I ❤️ unicode".encode()
        return file.save()
    
    def generate_alternative_multiplier(self) -> None:
        """An archive that contains a non-standard hash multiplier."""
        file = sarc.SARCFile()
        file.hash_multiplier = 97
        file.files["example.txt"] = b"Hello!"
        return file.save()
    
    def generate_big_endian(self) -> None:
        """An archive that uses big endian byte order."""
        file = sarc.SARCFile()
        file.endianness = ">"
        file.files["example.txt"] = b"Hello!"
        return file.save()
    
    def generate_multiple_files(self) -> None:
        """An archive that contains multiple files."""
        file = sarc.SARCFile()
        file.files["file1.txt"] = b"File content 1"
        file.files["file2.txt"] = b"File content 2"
        file.files["file3.txt"] = b"File content 3"
        return file.save()
    
    def generate_folders(self) -> None:
        """An archive that contains multiple files in folders."""
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
        """An archive where individual files have been aligned to 4 KB."""
        file = sarc.SARCFile()
        file.alignment = 4096
        file.files["file1"] = b"Aligned file 1"
        file.files["file2"] = b"Aligned file 2"
        return file.save()
    
    def generate_hash_collisions(self) -> None:
        """An archive in which hash collisions have occurred."""
        file = sarc.SARCFile()
        file.hash_multiplier = 53
        file.files["xxxx"] = b"File 1"
        file.files["xxyC"] = b"File 2"
        file.files["xyCx"] = b"File 3"
        file.files["yCxx"] = b"File 4"
        return file.save()
    
    def generate_no_filename(self) -> None:
        """
        An archive in which only filename hashes are stored, but no filenames.
        """

        hash1 = sarc.calculate_hash("example1.txt", 101, False)
        hash2 = sarc.calculate_hash("example2.txt", 101, False)
        hash3 = sarc.calculate_hash("example3.txt", 101, False)

        file = sarc.SARCFile()
        file.unnamed_files[hash1] = b"File 1"
        file.unnamed_files[hash2] = b"File 2"
        file.unnamed_files[hash3] = b"File 3"
        return file.save()
    
    def generate_complex(self) -> None:
        """
        An archive in which each of the above test cases has been combined into
        a single archive.
        """

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
