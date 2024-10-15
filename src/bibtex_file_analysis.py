import os
import sys

from bibtex_file_parser import bib_parser_main
from check_short_papers import check_short_papers_main
from merge_bibtex_files import merge_bibtex_main

# Function to execute the analysis in bibtex files inside a folder
if __name__ == "__main__":
    
    _input_folder = sys.argv[1]

    bib_files_arr_ = []

    required_args_ = {

        "set_1" : ["author", "title", "abstract", "year", "pages"],
        "set_2" : ["author", "title", "year", "pages"],
        "set_2" : ["author", "title", "year"]
    }

    for root, dirs, files in os.walk(_input_folder):
        for file_ in files:
            if file_.endswith(".bib"):
                bib_files_arr_.insert(len(bib_files_arr_)-1, os.path.join(root, file_))
        
        # If there's more than one bib file in the folder
        if len(bib_files_arr_) > 1:
            
            # Call the merger
            merged_file_ = merge_bibtex_main(root)

            # Call the parser
            bib_parser_main(merged_file_, required_args_["set_1"])

            # Call the short paper verification
            
