# cassave/main.py

from cassave.encoder import encode_file, save_wav
from cassave.decoder import decode_file
from cassave.fileformat import buildHeader, calculateCRC, removeHeader

def main():
    print("Cassave v1 is ready!")
    
    choice = input("Write or Read? ")
    if choice.lower() == 'w':
        
        fileName = input("Enter filename for encoding: ")
        fileNameOut = input("Enter filename for output: ")
        
        with open(fileName, 'rb') as f:
            data = f.read()
        
        
        fileHeader = buildHeader(fileName, len(data), 1)
        fileCRC = calculateCRC(data)

        # Encode to waveform
        waveform = encode_file(fileHeader + data + fileCRC)
        
        # Save to WAV
        save_wav(fileNameOut, waveform)
    
    
    elif choice.lower() == 'r':
    
        # Decode file
        
        fileName = input("Enter filename for decoding: ")
        
        decoded_bytes = decode_file(fileName)
        
        decoded_parsed_bytes, fileNameOut = removeHeader(decoded_bytes)

        # Save decoded data
        with open(fileNameOut, 'wb') as f:
            f.write(decoded_parsed_bytes)
    
    else:
        print("Choose Write or Read")

if __name__ == "__main__":
    main()
