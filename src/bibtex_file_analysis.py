import os
import sys
import shutil

from bibtex_file_parser import bib_parser_main
from check_short_papers import check_short_papers_main
from merge_bibtex_files import merge_bibtex_main
from bibtex_replace_month import replace_month_main

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

        print(f"  -> The correct format is python bibtex_file_analysis.py <input_folder> <required_args>"
              f"  -> The available sets for required_args parameter are:")

        for key, value in _required_args_options.items():
            print(f"  ** \t {key} : {value}")
        sys.argv(1)

    elif not os.path.exists(_input_folder):
        print(f"  -> Path {_input_folder} is not a valid path for a folder.")
        sys.argv(1)

    _bib_files_arr = []

    for root, dirs, files in os.walk(_input_folder):
        for file_ in files:

            if file_.endswith(".bib"):
                
                _merged_file = ""
                
                try:

                    # Call the merger
                    print("\n# Step 1: Merging BibTeX files")
                    _merged_file = merge_bibtex_main(root)
                    print(f"  -> Merged file created: {_merged_file}")

                    # Check if the returned merged file exists
                    if not os.path.exists(_merged_file):
                        print("It was not possible to return a valid path to a valid .bib file.")
                        sys.exit(1)
                    print("  -> Merged file verified: Exists and valid")

                    # Replace the months from string to int
                    print("\n# Step 2: Replacing months from string to number format")
                    replace_month_main(_merged_file)
                    print("  -> Month replacement completed")

                    # Call the parser
                    print("\n# Step 3: Parsing BibTeX entries")
                    bib_parser_main(_merged_file, _required_args_options[_required_args])
                    print("  -> Parsing completed")

                    # Call the short paper verification
                    print("\n# Step 4: Checking for short papers")
                    check_short_papers_main(_merged_file, _min_pages_paper)
                    print(f"  -> Short paper verification completed (minimum pages: {_min_pages_paper})")

                except:
                    if len(_merged_file) != 0:
                        os.remove(_merged_file)
                    sys.argv(1)
