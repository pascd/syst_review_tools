import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
import requests
import re
import sys

from get_data_from_doi import get_data_from_doi_main

def bib_load_file(input_file_):

    # Create the parser
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False
    parser.homogenise_fields = False

    # Open the .bib file with utf-8 encoding
    try:
        with open(input_file_, 'r', encoding='utf-8') as bibtex_file_:
            bibtex_str = bibtex_file_.read()
    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")
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

    # Iterate over the entries dictionary
    for entry_ in bib_file_.entries:
        entry_id_ = entry_.get('id', 'unknown')

        for arg_ in required_args_:
            if arg_ not in entry_:
                print(f"\n\tArgument [{arg_}] not in entry {entry_id_}")
                missing_args_.insert(len(missing_args_)-1, arg_)
            doi = entry_.get("doi", "The entry has no defined DOI")
            get_data_from_doi_main(doi)
            

def bib_parser_main(input_file_, required_args_):

    # Load the bibtex file
    bib_file_ = bib_load_file(input_file_)

    # Execute error checking
    bib_error_checking(bib_file_)

    # Execute arg checking
    bib_arg_checking(bib_file_, required_args_)

if __name__ == "__main__":

    _input_file = sys.argv[1]
    _required_args = sys.argv[2]

    ## Test
    _required_args = ["author", "title"]

    bib_parser_main(_input_file, _required_args)