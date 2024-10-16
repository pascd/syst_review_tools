import os
import sys
import shutil

from bibtex_file_parser import bib_parser_main
from check_short_papers import check_short_papers_main
from merge_bibtex_files import merge_bibtex_main

_required_args_options = {

    "set_1" : ["author", "title", "abstract", "year", "pages"],
    "set_2" : ["author", "title", "year", "pages"],
    "set_3" : ["author", "title", "year"]
}

_min_pages_paper = 4

# Function to execute the analysis in bibtex files inside a folder
if __name__ == "__main__":
    
    _input_folder = sys.argv[1]
    _required_args = sys.argv[2]

    if len(sys.argv) != 3 or sys.argv[1] == "--h":

        print(f"\nThe correct format is python bibtex_file_analysis.py <input_folder> <required_args>"
              f"\nThe available sets for required_args parameter are:")

        for key, value in _required_args_options.items():
            print(f"\t {key} : {value}")
        sys.argv(1)

    elif not os.path.exists(_input_folder):
        print(f"Path {_input_folder} is not a valid path for a folder.")
        sys.argv(1)

    _bib_files_arr = []

    for root, dirs, files in os.walk(_input_folder):
        for file_ in files:
            if file_.endswith(".bib"):
                _bib_files_arr.insert(len(_bib_files_arr)-1, os.path.join(root, file_))
        
        # If there's more than one bib file in the folder
        if len(_bib_files_arr) > 1:

            _merged_file = ""

            try:
                # Call the merger
                _merged_file = merge_bibtex_main(root)

                print(_merged_file)

                # Check if the returned merged file exists
                if not os.path.exists(_merged_file):
                    print("It was not possible to return a valid path to a valid .bib file.")
                    sys.exit(1)

                # Call the parser
                bib_parser_main(_merged_file, _required_args_options[_required_args])

                # Call the short paper verification
                check_short_papers_main(_merged_file, _min_pages_paper, os.path.dirname(file_))
            except:
                os.remove(_merged_file)
                sys.argv(1)
