import os
import subprocess
from typing import List
import glob

# Assuming the scripts are located relative to this Python file
PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'awesome-align'))
orig_dir = os.getcwd()

def write_list_to_file(lines: List[str], filename: str) -> None:
    with open(filename, 'w') as f:
        for line in lines:
            f.write(f"{line}\n")

def read_file_to_list(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return [line.rstrip() for line in f]  # Removing trailing newline characters
    
def delete_files(prefixes, directory='.'):
    for prefix in prefixes:
        file_pattern = os.path.join(directory, prefix + '*.txt')
        files = glob.glob(file_pattern)

        for file in files:
            try:
                os.remove(file)
                print(f"File {file} has been removed successfully")
            except Exception as e:
                print(f"Error occurred while deleting file {file}: {e}")

def run_script(script_path: str, *args: str) -> None:
    subprocess.run([script_path, *args], check=True, cwd=PATH)

def run_extractv2(source_file: str, target_file: str) -> List[str]:

    try:

        # Run the bash script
        run_script("bash", "extractv2.sh", source_file, target_file)

        alignment_file = 'source.txt.target.txt.aligned'
        # Read the aligned file to a list and return
        result = read_file_to_list(alignment_file)
        
        # Clean up the alignment file
        return result
    
    except:

        return []

def main_process(source_lines: List[str], target_lines: List[str]) -> List[str]:
    source_file = 'source.txt'
    target_file = 'target.txt'
    os.chdir(PATH)
    # Write source_lines and target_lines to files
    write_list_to_file(source_lines, source_file)
    write_list_to_file(target_lines, target_file)
    alignment_lines = run_extractv2(source_file, target_file)
    delete_files(['source', 'target'])
    os.chdir(orig_dir)
    return alignment_lines


if __name__ == "__main__":
    print(main_process(["hello my name is Roy Batty"], ["Hola me llamo Roy Batty"]))