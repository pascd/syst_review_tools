import os
import sys

month_conversion_ = {
    "jan" : "01",
    "feb" : "02",
    "mar" : "03",
    "apr" : "04",
    "may" : "05",
    "jun" : "06",
    "jul" : "07",
    "aug" : "08",
    "sep" : "09",
    "oct" : "10",
    "nov" : "11",
    "dec" : "12"
}

def replace_month(_bib_file):
    # Read the lines from bibtex
    with open(_bib_file, 'r', encoding='utf-8') as _file:
        lines = _file.readlines()

    try:
        with open(_bib_file, 'w', encoding='utf-8') as _file:
            for line in lines:
                # Look for the 'month =' line
                if 'month =' in line.lower():
                    # Extract the month abbreviation
                    _month_value = line.split('=')[1].strip().strip('{}",')
                    # Replace if found in the dictionary
                    if _month_value in month_conversion_ and not isinstance(_month_value, int):
                        line = f'month = {{{month_conversion_[_month_value]}}},\n'
                _file.write(line)
        print(f"  -> File {_bib_file} has all the month fields in INT format.")
    except:
        print("  -> An error occured when executing [month_replacement]")

def replace_month_main(_input_file):

    replace_month(_input_file)

if __name__ == "__main__":

    input_file_ = sys.argv[1]

    replace_month_main(input_file_)


