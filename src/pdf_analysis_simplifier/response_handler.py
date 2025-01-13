import os
import sys
import re

class ResponseHandler:
    def __init__(self):
        print("Created response handler object.")

    # Look for part of text and extract what is after
    def extract_by_identifier(self, response, identifier):

        # Use a regular expression to find the text after the specific identifier
        pattern = re.compile(rf"{re.escape(identifier)}:\s*(.*?)(?=\n\w+:|$)", re.DOTALL)
        match = pattern.search(response)

        if match:
            return match.group(1).strip()
        else:
            print("Error finding identifier or no text after identifier")
            return None