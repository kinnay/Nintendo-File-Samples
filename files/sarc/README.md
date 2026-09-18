This folder contains test cases for the [SARC file format](https://nintendo-formats.com/libs/sead/sarc.html).

| File | Description |
| --- | --- |
| `empty.sarc` | The most basic test case, an empty archive. |
| `simple.sarc` | A simple archive that contains a single file. |
| `sign_extension.sarc` | An archive that contains unicode characters in a filename. This can be used to test the sign extension behavior of Nintendo Switch games. |
| `alternative_multiplier.sarc` | An archive that contains a non-standard hash multiplier. |
| `big_endian.sarc` | An archive that uses big endian byte order. |
| `multiple_files.sarc` | An archive that contains multiple files. |
| `folders.sarc` | An archive that contains multiple files in folders. |
| `alignment.sarc` | An archive where individual files have been aligned to 4 KB. |
| `hash_collisions.sarc` | An archive in which hash collisions have occurred. |
| `no_filename.sarc` | An archive in which only filename hashes are stored, but no filenames. |
| `complex.sarc` | An archive in which each of the above test cases has been combined into a single archive. |
