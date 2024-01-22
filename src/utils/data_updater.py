"""
data_updater.py

This script intends to automate as much of the updating of the data stored in the data/ folder as possible and will
run @TODO how often? to keep JWTJuggernaut's data up-to-date.

Functions:
- scrape_jwt_claims: Scrapes the officially defined JWT claims from IANA.org
- main: Orchestrates the scraping and file updating process
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def scrape_jwt_claims(url) -> dict:
    """
    Scrapes JWT claims and their descriptions from the provided URL (from IANA.org).

    This function sends a GET request to the given URL and uses BeautifulSoup to parse the HTML content.
    It extracts JWT claims and their descriptions and organizes these into a dictionary object.
    :param url: The URL from which to scrape JWT claims information.
    :return: A dictionary with JWT claims as keys and their descriptions as values.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table by ID
    table = soup.find('table', id='table-claims')

    # Parse the table rows
    claims = {}
    if table:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if columns:
                claim_name = columns[0].text.strip()
                claim_desc = columns[1].text.strip()
                claims[claim_name] = claim_desc.replace('        ', ' ').replace('\n', '').replace('  ', ' ')

    # Adding confirmation method headers to claims dict for ease of lookup
    table = soup.find('table', id='table-confirmation-methods')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if columns:
                claim_name = columns[0].text.strip()
                claim_desc = columns[1].text.strip()
                claims[claim_name] = claim_desc.replace('        ', ' ').replace('\n', '')

    # Manual Entries for typ (https://datatracker.ietf.org/doc/html/rfc7519#section-5.1) and
    # cty (https://datatracker.ietf.org/doc/html/rfc7519#section-5.2) which are defined in RFC 7519 but
    # not in the IANA.org list
    claims['typ'] = 'Declares the media type of the complete JWT'
    claims['cty'] = 'Conveys structural information about the JWT'
    claims['alg'] = 'Algorithm used to sign or encrypt the JWT'

    return claims


def main():
    """
    Main function to orchestrate the data updating process (currently, only the JWT claims updating process).

    Calls scrape_jwt_claims to fetch the latest JWT claims data from the official source and updates data/claims.json. The function also sets the current date as the last updated date in the JSON file.

    :return: None
    """
    url = 'https://www.iana.org/assignments/jwt/jwt.xhtml'
    claims = scrape_jwt_claims(url)
    json_data = {
        "source": url,
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "claims": claims
    }

    # Define the file path using os.path.join for cross-platform compatibility
    file_path = os.path.join('data', 'claims.json')

    # Check if the file exists
    if not os.path.exists(os.path.dirname(file_path)):
        # If the directory does not exist, create it
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, indent=4)


if __name__ == "__main__":
    main()
