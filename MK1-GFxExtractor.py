import struct
import sys

def main():
    if len(sys.argv) == 3:
        input_path = sys.argv[1].strip('"')
        if not input_path.lower().endswith(".uasset"):
            print("\033[31mError: Input must be a .uasset file\033[0m")
            sys.exit(1)
        
        out_path = sys.argv[2].strip('"')
    elif len(sys.argv) == 1 or (len(sys.argv) == 2 and (sys.argv[1].lower() == "-h" or sys.argv[1].lower() == "--help")):
        print("Usage: MK1-GFxExtractor.py <input> <output>")
        return
    else:
        print(f"\033[31mIncorrect usage! Run with \"-h\" to display usages.\033[0m")
        sys.exit(1)
    
    try:
        with open(input_path, "rb") as file:
            bytes = file.read()
    except Exception as e:
        print(f"\033[31m{e}\033[0m")
        sys.exit(1)
        
    pattern = b"GFX"
    index = bytes.find(pattern)
    if index != -1:
        size_bytes = bytes[index - 4:index]
        size = struct.unpack("<I", size_bytes)[0]
        gfx = bytes[index:index + size]
        
        try:
            try:
                with open(out_path, "xb") as out:
                    out.write(gfx)
            except FileExistsError:
                should_overwrite = input(f"File '{out_path}' already exists. Overwite? [y/N]: ").strip().lower()
                if should_overwrite == "y":
                    with open(out_path, "wb") as out:
                        out.write(gfx)
                else:
                    print("Extraction cancelled")
                    return
                    
        except Exception as e:
            print(f"\033[31m{e}\033[0m")
            sys.exit(1)
        
        print(f"Successfully extracted GFX data to: '{out_path}'")
    else:
        print("\033[31mError: Could not find expected pattern in the provided file!\033[0m")
        sys.exit(1)
        
main()