# cassave/fileformat.py

from cassave.utils import formatDosFilename, bytesToASCII
import zlib


def buildHeader(filename, filesizeBits, version):
    """Builds the file header for Cassave format."""

    # Preamble: 256 bits = 32 bytes
    preamble = bytes([0b10101010]) * 32

    # Magic number: 0xDEADBEEF = 4 bytes
    magic = (0xDEADBEEF).to_bytes(4, byteorder='big')

    # Version byte: 1 byte
    versionByte = version.to_bytes(1, byteorder='big')

    # Filename: 11 bytes (DOS 8.3 format)
    dosFilename = formatDosFilename(filename).encode('ascii')  # Make sure it's 11 bytes

    # Filesize: 8 bytes (64-bit unsigned int)
    filesizeBytes = filesizeBits.to_bytes(8, byteorder='big')

    # Combine all parts
    header = preamble + magic + versionByte + dosFilename + filesizeBytes
    return header



def parseHeader(data):
    """Parses the Cassave file header and returns fields."""
    
    print(data)
    magic = (0xDEADBEEF).to_bytes(4, byteorder='big')
    magicIndex = data.find(magic)
    versionByte = int.from_bytes(data[magicIndex + 4: magicIndex + 5], byteorder="big")
    print(f"Recorded with Cassave version {versionByte}")
    filename = bytesToASCII(data[magicIndex + 5:magicIndex + 16])
    print(f"Filename is {filename}")
    filesize = int.from_bytes(data[magicIndex + 16:magicIndex + 24], byteorder="big")
    print(f"Size is {filesize} bytes")
    newData = data[magicIndex + 24:magicIndex + 24 + filesize]
    return newData, filename

def removeHeader(data):
    parsedData = parseHeader(data)
    return parsedData

def calculateCRC(dataBits):
    """Calculate CRC32 checksum and return it as bytes."""
    
    # Calculate the CRC32 checksum (returns an integer)
    crc = zlib.crc32(dataBits)
    
    # Convert the CRC32 checksum to bytes (4 bytes for a 32-bit integer)
    crc_bytes = crc.to_bytes(4, byteorder='big')  # Use 'big' or 'little' depending on your desired byte order
    
    return crc_bytes

    
    
