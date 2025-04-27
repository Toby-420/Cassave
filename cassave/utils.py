# cassave/utils.py

def formatDosFilename(name):
    """Format a filename into DOS 8.3 padded format (11 bytes, no dot)."""
    
    if '.' in name:
        base, ext = name.split('.', 1)
    else:
        base, ext = name, ''
    
    base = base.upper().ljust(8)[:8]
    ext = ext.upper().ljust(3)[:3]
    
    return base + ext  # total 11 characters
    
def bytesToASCII(bytesIn):
    # essentially the reverse of above function
    string = bytesIn.decode('ascii')
    stringParts = [string[:8], string[8:10]]
    stringNew = stringParts[0] + '.' + stringParts[1]
    stringNew = stringNew.replace(' ', '')
    return stringNew
    