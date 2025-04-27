# Cassave

**Cassave** is a software project that allows you to write digital files onto a standard audio cassette or similar devices by producing audio files containing the data.
It uses a robust, simple file format and error correction to maximize reliability even with the limitations of analog tape.

---

## Features

Features in bold are planned for future versions

### Decode
- Read `.wav` file containing recorded tape data
- Find clock pulse **and correct for speed drift if necessary**
- Decode using differential Manchester encoding
- Parse file header
- **Verify CRC checksum (with options to skip or ignore on failure)**
- Save recovered file **(user can accept original filename or specify a custom one)**

### Encode
- Take an input file and encode it with differential Manchester encoding
- Create structured headers / footers (preamble, magic number, version, filename, size, CRC)
- **Warn if file size exceeds practical limits for tape recording**
- **Estimate total recording time needed**
- Generate a `.wav` file ready to record onto tape

---

## File Format Specification

### Audio Structure

```
[Preamble] [Magic Number] [Version Byte] [Filename] [Filesize] [File Data] [CRC Checksum]
```

- **Preamble:**  
  256 bits of alternating `1`s and `0`s (`10101010…`) to allow synchronization.

- **Magic Number:**  
  Fixed value `0xDEADBEEF` (`11011110 10101101 10111110 11101111`) for format recognition.

- **Version Byte:**  
  Single byte to indicate the Cassave file format version.

- **Filename:**  
  DOS 8.3 filename format (uppercase, padded with spaces).

- **File Size:**  
  64-bit unsigned integer representing file size in **bytes**.
  This means the maximum storage capacity with this version of Cassave is 2^64 bytes or 16 whole exabytes.

- **File Data:**  
  Raw binary file data.

- **CRC Checksum:**  
  CRC32 checksum for integrity verification.

### File Data Structure

8 different tones are used to allow 1 whole byte to be sent at once.
This simplifies how the data can be stored.
The lowest tone used is bit 1 and the highest is bit 8.
The tones are far enough apart in this implementation that there will likely be no confusion between them.

---

## How to Use

### Encoding a File
1. Choose your input file (e.g., `hello.txt`).
2. Encode it using Cassave:
3. Record the generated `.wav` onto a cassette tape.

### Decoding a File
1. Play back the tape and record it to a `.wav` file.
2. Decode it using Cassave:
3. Recover the original file automatically.

> When playing back, please be aware that a high volume may cause excessive noise or even clipping, so you should start at 25% volume or lower and change from there.
> I recommend listening back to at least a little of the tape once recorded to make sure that there was no distortion during recording.

> **Note:** Some tape decks may run fast or slow; Cassave may attempt to correct for this automatically in future versions.

---

## Development Setup

### Requirements (in requirements.txt)
- Python 3.10+ (tested with 3.13)
- numpy
- scipy

### Setup
```bash
pip install -r requirements.txt
```

### Run
```bash
python -m cassave.main
```

---

## License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.  
See the [LICENSE](LICENSE) file for full details.


---

## Why "Cassave"?

Named after the **cassava plant** - both are tough, reliable, and work under rough conditions!
It's also a combination of the words 'Cassette' and 'Save'.

