import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
import sys

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

def bib_parser_main(input_file_, required_args_):

    # Create the parser
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False
    parser.homogenise_fields = False

    # Link the .bib file
    with open(input_file_) as bibtex_file_:
        bibtex_str = bibtex_file_.read()

    bib_file_ = bibtexparser.loads(bibtex_str) 

    # Execute error checking
    bib_error_checking(bib_file_)

    # Execute arg checking
    bib_arg_checking(bib_file_, required_args_)

if __name__ == "__main__":

    _input_file = sys.argv[1]
    _required_args = sys.argv[2]

    ## Test
    required_args_ = ["author", "title", "mirtilo"]

    bib_parser_main(_input_file, _required_args)