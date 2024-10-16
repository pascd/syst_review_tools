import os
import sys
import shutil

def merge_bibtex_files(_input_files, _output_file):

    _entries = set()
    _current_entry = []

    with open(_output_file, 'w', encoding='utf-8') as outfile:
        for _bib_file in _input_files:
            with open(_bib_file, 'r', encoding='utf-8') as infile:
                for _line in infile:
                    # Detect the start of a new BibTeX entry
                    if _line.strip().startswith('@'):
                        
                        if _current_entry:
                            entry_text = ''.join(_current_entry).strip()
                            if entry_text not in _entries:
                                outfile.write(entry_text + "\n\n")
                                _entries.add(entry_text)
                            _current_entry = []

                    # Add line to the current entry
                    _current_entry.append(_line)

                # After finishing each file, write the last entry (if any)
                if _current_entry:
                    _entry_text = ''.join(_current_entry).strip()
                    if _entry_text not in _entries:
                        outfile.write(_entry_text + "\n\n")
                        _entries.add(_entry_text)
                    _current_entry = []

    print(f"  -> Merged {len(_input_files)} files into {_output_file}")

def merge_bibtex_main(_input_files_path):

    # Initiated merger
    print(f"  -> Initiated merger for bibtex files:")

    # Ensure the path to the folder exists and is reachable
    _input_files_path = _input_files_path.strip()

    if os.path.exists(_input_files_path):
        print(f"  -> Path {_input_files_path} exists and is reachable.")
    else:
        print(f"  -> Path {_input_files_path} does not exist.")
        sys.exit(1)

    # Initialize a vector to store multiple .bib files
    _input_files = []

    # The name of the output file
    _output_file_name = os.path.basename(_input_files_path) + ".bib"

    # It is necessary to find all .bib files in the directory
    for _file in os.listdir(_input_files_path):
        if _file.endswith(".bib"):
            _input_files.append(os.path.join(_input_files_path, _file))

    # Outputh file path
    _output_file = os.path.join(_input_files_path, _output_file_name)

    if len(_input_files) > 1:
        merge_bibtex_files(_input_files, _output_file)
    elif len(_input_files) == 1:  
        shutil.copy(_input_files[0], _output_file)      
        print(f"  -> There's no need to merge BibTeX files since there's only one file in folder: {_input_files_path}")
    else:
        print(f"  -> Could not find any .bib file in folder: {_input_files_path}")

    return _output_file
    
if __name__ == "__main__":
    
    # Path of the input file
    input_files_path_ = sys.argv[1]

    merge_bibtex_main(input_files_path_)
