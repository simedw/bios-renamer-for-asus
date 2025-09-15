import sys
import os

# The specific 16-byte GUID marker from the C code.
# var_20 = 0x4cc14f19 -> 19 4F C1 4C (little-endian)
# var_1c = 0x4ab6c626 -> 26 C6 B6 4A
# var_18 = 0x6ccaea9d -> 9D EA CA 6C
# var_14 = 0xcd10fd01 -> 01 FD 10 CD
GUID_MARKER = bytes([
    0x19, 0x4F, 0xC1, 0x4C, 0x26, 0xC6, 0xB6, 0x4A,
    0x9D, 0xEA, 0xCA, 0x6C, 0x01, 0xFD, 0x10, 0xCD
])

# The $BOOTEFI$ tag to search for after the GUID.
BOOTEFI_TAG = b'$BOOTEFI$'

# The fixed offset from the start of the $BOOTEFI$ tag to the new filename.
# This corresponds to `&lpBuffer[0x91 + esi_1]` in the C code.
FILENAME_OFFSET = 0x91

# The length of the filename string.
# This corresponds to `*(eax_9 + 0xc) = 0;` which null-terminates at the 13th byte.
FILENAME_LENGTH = 12


def extract_bios_name(filepath):
    """
    Opens a BIOS .CAP file, finds the USB BIOS Flashback name, and returns it.

    Args:
        filepath (str): The path to the .CAP file.

    Returns:
        str: The extracted BIOS filename, or None if not found.
    """
    try:
        with open(filepath, 'rb') as f:
            file_content = f.read()
    except IOError as e:
        print(f"Error: Could not read file '{filepath}'.\n{e}", file=sys.stderr)
        return None

    # 1. Find the GUID marker in the file.
    guid_offset = file_content.find(GUID_MARKER)
    if guid_offset == -1:
        print(f"Error: GUID marker not found in '{filepath}'. This may not be a valid BIOS file for this tool.", file=sys.stderr)
        return None

    # 2. Find the '$BOOTEFI$' tag, starting the search from where the GUID was found.
    boote_tag_offset = file_content.find(BOOTEFI_TAG, guid_offset)
    if boote_tag_offset == -1:
        print(f"Error: '$BOOTEFI$' tag not found after the GUID in '{filepath}'.", file=sys.stderr)
        return None

    # 3. Calculate the position of the new filename.
    new_name_start = boote_tag_offset + FILENAME_OFFSET

    if new_name_start + FILENAME_LENGTH > len(file_content):
        print(f"Error: Filename location is out of bounds in '{filepath}'.", file=sys.stderr)
        return None

    # 4. Extract the 12-byte filename, remove trailing null bytes, and decode it.
    new_name_bytes = file_content[new_name_start : new_name_start + FILENAME_LENGTH]
    
    # Clean up by removing any trailing null characters and decode from bytes to string.
    try:
        new_name = new_name_bytes.rstrip(b'\x00').decode('ascii')
    except UnicodeDecodeError:
        print(f"Error: Could not decode the extracted filename from '{filepath}'.", file=sys.stderr)
        return None

    return new_name

def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(sys.argv[0])} <path_to_cap_file.CAP>")
        sys.exit(1)

    cap_filepath = sys.argv[1]

    if not os.path.exists(cap_filepath):
        print(f"Error: File not found at '{cap_filepath}'", file=sys.stderr)
        sys.exit(1)

    bios_name = extract_bios_name(cap_filepath)

    if bios_name:
        print(bios_name)
    else:
        # Errors are already printed to stderr within the function
        sys.exit(1)

if __name__ == '__main__':
    main()
