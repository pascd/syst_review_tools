import os
import sys
import bibtexparser

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

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
        print(f"\n\tError reading file: {e}")
        sys.exit(1)

    _bib_file = bibtexparser.loads(_bibtex_str, parser=parser) 

    return _bib_file

def replace_month(_bib_file):

    for _entry in _bib_file.entries:
        
        

def replace_month_main(_input_file):

    _bib_file = bib_load_file(_input_file)



if __name__ == "__main__":

    input_file_ = sys.argv[1]

    replace_month_main(input_file_)


