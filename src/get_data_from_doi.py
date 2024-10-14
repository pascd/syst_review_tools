import requests
import re
import os
import sys
import json
import urllib.parse

def request_data_crossref(doi_):

    entry_request_ = {}

    # Encode the DOI to handle special characters
    encoded_doi_ = urllib.parse.quote(doi_, safe='')

    # CrossRef API endpoint for the DOI
    url = f"http://api.crossref.org/works/{encoded_doi_}"
    
    try:
        # Send a GET request to the API
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()

        # Extract various fields from the JSON data
        title = data.get('message', {}).get('title', ['No title available'])[0]
        authors = data.get('message', {}).get('author', [])
        publication_year = data.get('message', {}).get('published-print', {}).get('date-parts', [[None]])[0][0]
        journal = data.get('message', {}).get('container-title', ['No journal title available'])[0]
        pages = data.get('message', {}).get('page', 'No page information available')

        # Format authors
        author_names = ', '.join([f"{author['given']} {author['family']}" for author in authors if 'given' in author and 'family' in author])

        # Check if abstract exists and process it
        abstract = data.get('message', {}).get('abstract', None)
        if abstract:
            # Clean the abstract if it exists
            abstract_cleaned = abstract.replace('<jats:p>', '\n').replace('</jats:p>', '\n')
            abstract_cleaned = re.sub(r'<[^>]*>', ' ', abstract_cleaned)
        else:
            abstract_cleaned = "No abstract available."

        entry_request_ = {
            "title" : title,
            "authors" : author_names,
            "year" : publication_year,
            "pages" : pages,
            "journal" : journal,
            "abstract" : abstract
        }

        # Print the formatted information
        #print("Title:", title)
        #print("Authors:", author_names)
        #print("Publication Year:", publication_year)
        #print("Journal:", journal)
        #print("Pages:", pages)
        #print("Abstract:\n", abstract_cleaned)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CrossRef: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return entry_request_

def get_data_from_doi_main(doi_):

    data_request_ = request_data_crossref(doi_)

    return data_request_

if __name__ == "__main__":
    
    _doi = sys.argv[1]
    get_data_from_doi_main(_doi)