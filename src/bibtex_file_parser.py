import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
import requests
import re
import sys

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from get_data_from_doi import get_data_from_doi_main

# Definition of global variables
modified_entries_ = {}

def bib_load_file(_input_file):

    # Create the parser
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False
    parser.homogenise_fields = True

    # Open the .bib file with utf-8 encoding
    try:
        with open(_input_file, 'r', encoding='utf-8') as _bibtex_file_:
            _bibtex_str = _bibtex_file_.read()
    except UnicodeDecodeError as e:
        print(f"  -> Error reading file: {e}")
        sys.exit(1)

    _bib_file = bibtexparser.loads(_bibtex_str, parser=parser) 

    return _bib_file

# Function to parse bibtex file
def bib_error_checking(_bib_file):

    print(f"  -> The input file has:")
    print(f"\n  ** {len(_bib_file.entries)} entries"
    f"\n  ** {len(_bib_file.comments)} comments"
    f"\n  ** {len(_bib_file.strings)} strings and"
    f"\n  ** {len(_bib_file.preambles)} preambles")

    if(len(_bib_file.entries) == 0):
        print(f"  -> The parsed bibtex file has no entries to process.")
        sys.exit(1)
        
    print(f"  -> The bibtex file was successfully parsed.")

def bib_arg_checking(_bib_file, _required_args):

    _missing_args = []
    _final_entry_arr = []
    _i = 0

    # Iterate over the entries dictionary
    for _entry in _bib_file.entries:
        # Print actual entry in execution
        print(f"  ** Entry {_i}/{len(_bib_file.entries)}")

        _entry_id = _entry.get('id', 'unknown')

        for _arg in _required_args:
            
            if _arg not in _entry:
                #print(f"\n\tArgument [{arg_}] not in entry: {entry_id_}")
                _missing_args.insert(len(_missing_args)-1, _arg)
        
        if len(_missing_args) > 0:

            doi = _entry.get("doi", "")

            # If the entry does not have a DOI, skip the search
            if len(doi) == 0:
                print(f"  -> The entry {_entry_id} has no valid DOI, ignoring auto-fill")
                _final_entry_arr.insert(len(_final_entry_arr)-1, _entry)
                _i += 1
                continue
            
            # Get data from doi in bibtex
            entry_data_ = get_data_from_doi_main(doi)
            
            for _missing in _missing_args:
                if _missing in entry_data_:
                    _entry[_missing] = entry_data_[_missing]
        
        # Add the new entry to a new array of entries
        _final_entry_arr.insert(len(_final_entry_arr)-1, _entry)

        # Reset the array for missing arguments
        _missing_args = []
        _i += 1

    return _final_entry_arr

def bib_file_dump(_final_entry_arr, _output_file_path, _input_bib_file):

    _bibtex_database = BibDatabase()
    _bibtex_database.entries = _final_entry_arr

    _writer = BibTexWriter()

    with open(_output_file_path, 'w', encoding="utf-8") as bibtex_file:
        bibtex_file.write(_writer.write(_bibtex_database))
    
    print(f"  -> The output file has: "
          f"\n  -> {len(_bibtex_database.entries)} valid entries"
          f"\n  -> {len(_input_bib_file.entries) - len(_bibtex_database.entries)} have missing arguments."
          f"\n  -> with the respective modifications on: {modified_entries_}")

def bib_parser_main(_input_file, _required_args):

    _output_dir_name = os.path.dirname(_input_file)
    _output_file = os.path.join(_output_dir_name, f"{_output_dir_name}_parsed.txt")

    _modified_entries = {}

    # Fill the dictionary with pre-values
    for _arg in _required_args:
        _modified_entries[_arg] = 0

    # Load the bibtex file
    _bib_file = bib_load_file(_input_file)

    # Execute error checking
    bib_error_checking(_bib_file)

    # Execute arg checking
    _final_entry_arr = bib_arg_checking(_bib_file, _required_args)
 
    # Write to a new file the whole content of the new bibtex file
    bib_file_dump(_final_entry_arr, _output_file, _bib_file)

if __name__ == "__main__":

    input_file_ = sys.argv[1]
    required_args_ = sys.argv[2]

    ## Test for terminal request
    required_args_ = ["author", "title", "abstract", "year", "pages"]

    bib_parser_main(input_file_, required_args_)