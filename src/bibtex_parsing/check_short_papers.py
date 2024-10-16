import os
import sys
import bibtexparser

from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from keras.backend import less
from fontTools.merge.util import equal

def load_bibtex_file(_input_file):
    
    # Create the parser
    _parser = BibTexParser(common_strings=False)
    _parser.ignore_nonstandard_types = False
    _parser.homogenise_fields = True

    # Open the .bib file with utf-8 encoding
    try:
        with open(_input_file, 'r', encoding='utf-8') as _bibtex_file:
            _bibtex_str = _bibtex_file.read()
    except UnicodeDecodeError as e:
        print(f"  -> Error reading file: {e}")
        sys.exit(1)

    _bib_file = bibtexparser.loads(_bibtex_str, parser=_parser) 

    return _bib_file

def is_roman_numeral(s):
    _roman_numerals = set('IVXLCDM')
    return all(char in _roman_numerals for char in s)

def find_short_papers(_bib_file, _pages_threshold):

    _short_papers = []

    for _entry in _bib_file.entries:

        # Get the number of pages for each entry
        _pages = _entry.get('pages', '')

        # Ensure pages is not empty and is not entirely alphabetic
        if _pages and not _pages.isalpha():
            _pages_indx = _pages.split("-", 2)

            if len(_pages_indx) == 2:
                if is_roman_numeral(_pages_indx[0]) or is_roman_numeral(_pages_indx[1]):
                    continue

                try:
                    _start_page = int(_pages_indx[0])
                    _end_page = int(_pages_indx[1])
                    _number_pages = (_end_page - _start_page) + 1
                except ValueError:
                    continue

                if _number_pages <= int(_pages_threshold):
                    _short_papers.append(_entry.get('title', ''))

    return _short_papers

def dump_short_papers(_short_papers, _output_file_path):
    
    with open(_output_file_path, 'w', encoding="utf-8") as file:
        _i = 0
        for _title in _short_papers:
            _i += 1
            file.write(f"\n\n Paper {i}:" + _title)

def check_short_papers_main(_input_file, _pages_threshold):

    _output_dir_name = os.path.dirname(_input_file)
    _output_file_path = os.path.join(_output_dir_name, "short_papers.txt")

    _bib_file_ = load_bibtex_file(_input_file)

    _short_papers = find_short_papers(_bib_file_, _pages_threshold)

    dump_short_papers(_short_papers, _output_file_path)

if __name__ == "__main__":

    input_file_ = sys.argv[1]
    pages_threshold_ = sys.argv[2]

    check_short_papers_main(input_file_, pages_threshold_)