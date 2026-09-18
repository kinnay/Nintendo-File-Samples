
from generators.base import Generator
from jungle.common import byaml

import math


class BYAMLGenerator(Generator):
    def __init__(self):
        super().__init__("byaml")
        self._generators = {
            "empty.byaml": self.generate_empty,
            "values.byaml": self.generate_values,
            "values_v5.byaml": self.generate_values_v5,
            "collections.byaml": self.generate_collections,
            "little_endian.byaml": self.generate_little_endian,
            "mariokart8.byaml": self.generate_mariokart8,
            "cycle.yaml": self.generate_cycle
        }

    def generate_empty(self) -> bytes:
        file = byaml.BYAMLFile()
        return file.save()

    def generate_values(self) -> bytes:
        root = byaml.BYAMLArray([
            byaml.BYAMLBool(False),
            byaml.BYAMLBool(True),
            byaml.BYAMLInt(-0x80000000),
            byaml.BYAMLInt(0),
            byaml.BYAMLInt(0x7FFFFFFF),
            byaml.BYAMLFloat(0),
            byaml.BYAMLFloat(100),
            byaml.BYAMLFloat(math.inf),
            byaml.BYAMLFloat(math.nan),
            byaml.BYAMLString("test"),
            byaml.BYAMLNone()
        ])
        file = byaml.BYAMLFile()
        file.root = root
        return file.save()

    def generate_values_v5(self) -> bytes:
        file = byaml.BYAMLFile()
        file.version = 5
        file.root = byaml.BYAMLArray([
            byaml.BYAMLBinary(b"binary data"),
            byaml.BYAMLBinaryAnnotated(b"annotated data", 123),
            byaml.BYAMLUint(0xAABBCCDD),
            byaml.BYAMLInt64(-(1 << 63)),
            byaml.BYAMLInt64((1 << 63) - 1),
            byaml.BYAMLUint64(0xAAAABBBBCCCCDDDD),
            byaml.BYAMLDouble(1 / 3),
        ])
        return file.save()

    def generate_collections(self) -> bytes:
        root = byaml.BYAMLDict({
            "array": byaml.BYAMLArray([
                byaml.BYAMLInt(0),
                byaml.BYAMLInt(1),
                byaml.BYAMLInt(2)
            ]),
            "dict": byaml.BYAMLDict({
                "key1": byaml.BYAMLString("value1"),
                "key2": byaml.BYAMLString("value2")
            })
        })
        file = byaml.BYAMLFile()
        file.root = root
        return file.save()

    def generate_little_endian(self) -> bytes:
        root = byaml.BYAMLArray([
            byaml.BYAMLInt(12345),
            byaml.BYAMLFloat(1234.5),
            byaml.BYAMLBool(True)
        ])
        file = byaml.BYAMLFile()
        file.endianness = "<"
        file.root = root
        return file.save()

    def generate_mariokart8(self) -> bytes:
        file = byaml.BYAMLFile()
        file.has_binary_table = True
        file.root = byaml.BYAMLArray([
            byaml.BYAMLBinary(b"buffer1"),
            byaml.BYAMLBinary(b"buffer2")
        ])
        return file.save()

    def generate_cycle(self) -> bytes:
        array = byaml.BYAMLArray()
        dict = byaml.BYAMLDict()
        dict.value = {"array": array}
        array.value = [dict]

        file = byaml.BYAMLFile()
        file.root = array
        return file.save()