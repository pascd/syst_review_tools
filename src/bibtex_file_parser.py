import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
import requests
import re
import sys

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from get_data_from_doi import get_data_from_doi_main

def bib_load_file(input_file_):

    # Create the parser
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False
    parser.homogenise_fields = True

    # Open the .bib file with utf-8 encoding
    try:
        with open(input_file_, 'r', encoding='utf-8') as bibtex_file_:
            bibtex_str = bibtex_file_.read()
    except UnicodeDecodeError as e:
        print(f"\n\tError reading file: {e}")
        sys.exit(1)

    bib_file_ = bibtexparser.loads(bibtex_str, parser=parser) 

    return bib_file_

# Function to parse bibtex file
def bib_error_checking(bib_file_):

    print(f"\n\t{len(bib_file_.entries)} entries"
    f"\n\t{len(bib_file_.comments)} comments"
    f"\n\t{len(bib_file_.strings)} strings and"
    f"\n\t{len(bib_file_.preambles)} preambles")

    if(len(bib_file_.entries) == 0):
        print(f"\n\tThe parsed bibtex file has no entries to process.")
        sys.exit(1)
        
    print(f"\n\tThe bibtex file was successfully parsed.")

def bib_arg_checking(bib_file_, required_args_):

    missing_args_ = []
    final_entry_arr_ = []
    i = 0

    # Iterate over the entries dictionary
    for entry_ in bib_file_.entries:
        # Print actual entry in execution
        print(f"Entry {i}/{len(bib_file_.entries)}")

        entry_id_ = entry_.get('id', 'unknown')

        for arg_ in required_args_:
            
            if arg_ not in entry_:
                #print(f"\n\tArgument [{arg_}] not in entry: {entry_id_}")
                missing_args_.insert(len(missing_args_)-1, arg_)
        
        if len(missing_args_) > 0:

            doi = entry_.get("doi", "")

            # If the entry does not have a DOI, skip the search
            if len(doi) == 0:
                print(f"\n\tThe entry {entry_id_} has no valid DOI, ignoring auto-fill")
                final_entry_arr_.insert(len(final_entry_arr_)-1, entry_)
                i += 1
                continue
            
            # Get data from doi in bibtex
            entry_data_ = get_data_from_doi_main(doi)
            
            for missing_ in missing_args_:
                if missing_ in entry_data_:
                    entry_[missing_] = entry_data_[missing_]
                    _modified_entries[missing_] += 1
                    #print(f"\n\t ** Added arg [{missing_}] to entry: {entry_id_}")
        
        # Add the new entry to a new array of entries
        final_entry_arr_.insert(len(final_entry_arr_)-1, entry_)

        # Reset the array for missing arguments
        missing_args_ = []
        i += 1

    return final_entry_arr_

def bib_file_dump(final_entry_arr_, _output_file_path, input_bib_file_):

    bibtex_database_ = BibDatabase()
    bibtex_database_.entries = final_entry_arr_

    writer = BibTexWriter()

    with open(_output_file_path, 'w', encoding="utf-8") as bibtex_file:
        bibtex_file.write(writer.write(bibtex_database_))
        #bibtexparser.dump(bibtex_database_, bibtex_file)
    
    print(f"\n\n\tThe output file has: "
          f"\n\t {len(bibtex_database_.entries)} valid entries"
          f"\n\t {len(input_bib_file_.entries) - len(bibtex_database_.entries)} have missing arguments."
          f"\n\t with the respective modifications on: {_modified_entries}")

def bib_parser_main(input_file_, required_args_, _output_file_path):

    # Load the bibtex file
    bib_file_ = bib_load_file(input_file_)

    # Execute error checking
    bib_error_checking(bib_file_)

    # Execute arg checking
    final_entry_arr_ = bib_arg_checking(bib_file_, required_args_)
 
    # Write to a new file the whole content of the new bibtex file
    bib_file_dump(final_entry_arr_, _output_file_path, bib_file_)

if __name__ == "__main__":

    _input_file = sys.argv[1]
    _required_args = sys.argv[2]
    _output_file_name = sys.argv[3]

    _output_dir_name = os.path.dirname(_input_file)
    _output_file_path = os.path.join(_output_dir_name, _output_file_name)

    # Definition of global variables
    _modified_entries = {}

    ## Test
    _required_args = ["author", "title", "abstract", "year", "pages"]

    # Fill the dictionary with pre-values
    for _arg in _required_args:
        _modified_entries[_arg] = 0

    bib_parser_main(_input_file, _required_args, _output_file_path)