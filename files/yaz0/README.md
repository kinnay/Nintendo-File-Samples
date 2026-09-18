This folder contains test cases for the [Yaz0 file format](https://nintendo-formats.com/libs/sead/yaz0.html).

| File | Description |
| --- | --- |
| `simple.szs` | A basic test case with a repetitive payload. |
| `random.szs` | 8 KB of random data compressed. |
| `weak.szs` | This test case uses the weakest compression level, which increases the file size. |
| `alignment.szs` | This file specifies a minimum required alignment in the header. The payload contains a [SARC file](https://nintendo-formats.com/libs/sead/sarc.html) in which every file is aligned to 256 bytes. |
