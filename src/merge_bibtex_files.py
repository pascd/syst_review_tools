import os
import sys

def merge_bibtex_files(input_files, output_file):
    """
    Merges multiple BibTeX files into one, with a blank line between each entry.

    Parameters:
        input_files (list): List of paths to BibTeX files to be merged.
        output_file (str): Path to the output merged BibTeX file.
    """
    entries = set()  # To store unique entries
    current_entry = []  # To store lines of the current BibTeX entry

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for bib_file in input_files:
            with open(bib_file, 'r', encoding='utf-8') as infile:
                for line in infile:
                    # Detect the start of a new BibTeX entry
                    if line.strip().startswith('@'):
                        # Write the previous entry (if any) and add a newline between entries
                        if current_entry:
                            entry_text = ''.join(current_entry).strip()
                            if entry_text not in entries:
                                outfile.write(entry_text + "\n\n")  # Write entry followed by a blank line
                                entries.add(entry_text)
                            current_entry = []  # Reset for the next entry

                    # Add line to the current entry
                    current_entry.append(line)

                # After finishing each file, write the last entry (if any)
                if current_entry:
                    entry_text = ''.join(current_entry).strip()
                    if entry_text not in entries:
                        outfile.write(entry_text + "\n\n")  # Write entry followed by a blank line
                        entries.add(entry_text)
                    current_entry = []  # Reset for the next file

    print(f"Merged {len(input_files)} files into {output_file}")

def merge_bibtex_main(input_files_path):

    # Ensure the path to the folder exists and is reachable
    input_files_path = input_files_path.strip()
    if os.path.exists(input_files_path):
        print(f"Path {input_files_path} exists and is reachable.")
    else:
        print(f"Path {input_files_path} does not exist.")
        sys.exit(1)

    input_files_ = []
    output_file_name_ = os.path.basename(input_files_path) + ".bib"

    # It is necessary to find all .bib files in the directory
    for file in os.listdir(input_files_path_):
        if file.endswith(".bib"):
            input_files_.append(os.path.join(input_files_path, file))

    if len(input_files_) > 1:
        output_file = os.path.join(input_files_path, output_file_name_)
        merge_bibtex_files(input_files_, output_file)
    elif len(input_files_) == 1:
        print(f"There's no need to merge BibTeX files since there's only one file in folder: {input_files_path_}")
    else:
        print(f"Could not find any .bib file in folder: {input_files_path_}")

if __name__ == "__main__":
    input_files_path_ = sys.argv[1]
    merge_bibtex_main(input_files_path_)
