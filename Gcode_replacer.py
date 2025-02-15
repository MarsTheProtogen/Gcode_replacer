import json
import os

PRESETS_FILE = "presets.json"
NOTES = "(modified G-code using Gcode_replacer by MarsTheProtogen https://github.com/MarsTheProtogen/Gcode_replacer)"

def read_gcode(file_path):
    """Reads a G-code file and returns its contents as a list of lines."""
    with open(file_path, 'r') as file:
        return file.readlines()

def write_gcode(file_path, lines):
    """Writes the modified G-code lines to a new file."""
    with open(file_path, 'w') as file:
        file.writelines(lines)

def find_and_replace(lines, find_str, replace_str):
    """Finds and replaces text in the G-code lines."""
    modified_lines = []

    modified_lines.append(NOTES)

    for line in lines:
        modified_lines.append(line.replace(find_str, replace_str))
    return modified_lines

def load_presets():
    """Loads presets from the JSON file."""
    if os.path.exists(PRESETS_FILE):
        with open(PRESETS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_presets(presets):
    """Saves presets to the JSON file."""
    with open(PRESETS_FILE, 'w') as file:
        json.dump(presets, file, indent=4)

def create_preset(presets):
    """Creates a new preset."""
    name = input("Enter a name for the preset: ")
    find_str = input("Enter text to find: ")
    replace_str = input("Enter text to replace with: ")
    presets[name] = {"find": find_str, "replace": replace_str}
    save_presets(presets)
    print(f"Preset '{name}' created.")

def list_presets(presets):
    """Lists all available presets."""
    if not presets:
        print("No presets available.")
    else:
        print("Available presets:")
        for name, preset in presets.items():
            print(f"{name:<50}: Find '{preset['find']}' -> Replace '{preset['replace']}'")

def apply_preset(lines, preset):
    """Applies a preset to the G-code lines."""
    return find_and_replace(lines, preset["find"], preset["replace"])

def main():
    # Load presets
    presets = load_presets()

    print("Welcome to the G-code editor!")
    print("created by MarsTheProtogen https://github.com/MarsTheProtogen")
    print("--------------------------------------------------------------")
    print("")
    # Input file path
    input_file = input("Enter the path to the G-code file: ")

    if not os.path.exists(input_file):
        print(f"Error: The file or directory does not exist.")
        return
    
    output_file = input("Enter the path to save the modified G-code file: ")

    if os.path.exists(output_file):
        print(f"The output file already exists. Overwrite? (y/n) then press enter: ")
        input_overwrite = input().lower()
        if input_overwrite!= "y":
            print("Exiting...")
            return

    # Read the G-code file
    lines = read_gcode(input_file)

    # Terminal interface
    while True:
        print("\nCurrent G-code preview (first 5 lines):")
        for line in lines[:5]:
            print(line.strip())

        print("\nOptions:")
        print("1. Find and replace manually")
        print("2. Use a preset")
        print("3. Create a new preset")
        print("4. List all presets")
        print("5. Quit and save")

        choice = input("Select an option and press enter (1-5): ")

        if choice == "1":
            find_str = input("Enter text to find: ")
            replace_str = input("Enter text to replace with: ")
            lines = find_and_replace(lines, find_str, replace_str)
            print(f"Replaced '{find_str}' with '{replace_str}'.")

        elif choice == "2":
            list_presets(presets)
            preset_name = input("Enter the name of the preset to apply: ")
            if preset_name in presets:
                lines = apply_preset(lines, presets[preset_name])
                print(f"Applied preset '{preset_name}'.")
            else:
                print("Preset not found.")

        elif choice == "3":
            create_preset(presets)
            print("New preset created.")
            load_presets()

        elif choice == "4":
            list_presets(presets)
        elif choice == "5":
            break
        else:
            print("Invalid option. Please try again.")

    # Write the modified G-code to a new file
    write_gcode(output_file, lines)
    print(f"\nModified G-code saved to {output_file}")

if __name__ == "__main__":
    main()