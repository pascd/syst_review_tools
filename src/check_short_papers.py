import os
import sys
import bibtexparser

from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from keras.backend import less
from fontTools.merge.util import equal

def load_bibtex_file(input_file_):
    
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

def is_roman_numeral(s):
    roman_numerals = set('IVXLCDM')
    return all(char in roman_numerals for char in s)

def find_short_papers(bib_file_, _pages_threshold):

    short_papers_ = []

    for entry_ in bib_file_.entries:

        # Get the number of pages for each entry
        pages_ = entry_.get('pages', '')

        # Ensure pages is not empty and is not entirely alphabetic
        if pages_ and not pages_.isalpha():
            pages_indx_ = pages_.split("-", 2)

            if len(pages_indx_) == 2:
                if is_roman_numeral(pages_indx_[0]) or is_roman_numeral(pages_indx_[1]):
                    continue

                try:
                    start_page = int(pages_indx_[0])
                    end_page = int(pages_indx_[1])
                    number_pages_ = (end_page - start_page) + 1
                except ValueError:
                    continue

                if number_pages_ <= int(_pages_threshold):
                    short_papers_.append(entry_.get('title', ''))

    return short_papers_

def dump_short_papers(short_papers_, _output_file_path):
    
    with open(_output_file_path, 'w', encoding="utf-8") as file:
        i = 0
        for title_ in short_papers_:
            i += 1
            file.write(f"\n\n Paper {i}:" + title_)

def check_short_papers_main(input_file_, _pages_threshold):

    _output_dir_name = os.path.dirname(_input_file)
    _output_file_path = os.path.join(_output_dir_name, "short_papers.txt")

    bib_file_ = load_bibtex_file(input_file_)

    short_papers_ = find_short_papers(bib_file_, _pages_threshold)

    dump_short_papers(short_papers_, _output_file_path)

if __name__ == "__main__":

    _input_file = sys.argv[1]
    _pages_threshold = sys.argv[2]

    check_short_papers_main(_input_file, _pages_threshold)