"""
parse_token.py

This file is intended to contain all the functionality needed by the tool to parse information from a provided JWT.

Functions:
- parse_token: The main function for token parsing, calls other functions for easier readability.
- base64_decode: Takes the Base-64 encoded header or payload and returns a Python dict of the decoded data.
- fetch_details: Pulls data from data/claims.json for the claims in the provided JWT. Runs data_updater if data/claims.json does not exist.
- convert_unix_to_utc: Takes a Unix timestamp and returns human-readable datetime string in UTC.
- create_print_string: Creates printable, formatted string on a per-claim basis.
- print_token: The main function for outputting parsed token details to the user.
"""

import os
import sys
import json
import time
import base64
from colorama import Fore, Style
from datetime import datetime

import src.utils.data_updater
import src.utils.error_handler


def parse_token(token: str, details: bool) -> dict:
    """
    Decodes the header and payload of a given token into human-readable format.

    This function separates the token into its respective sections and Base64 decodes the header and payload sections.
    The claims within these sections are then placed in a dictionary, along with the original Base64 encoded sections
    and the token's signature.
    :param token: The JWT to be read.
    :param details: Include additional information? T/F
    :return: Decoded information about the JWT in nested dictionary object.
    """

    header, payload, signature = '', '', ''
    try:
        header, payload, signature = token.split('.')
    except ValueError:
        src.utils.error_handler.print_error('JWT not in correct format. Expected: <header>.<payload>.<signature>')

    token_dict = {}
    details_dict = {}

    header_dict = base64_decode(header)
    payload_dict = base64_decode(payload)

    if details:
        # perform lookup of claim definitions from data/claims.json
        details_dict = fetch_details(header_dict, payload_dict)

    token_dict['original_token'] = token
    token_dict['header_dict'] = header_dict
    token_dict['payload_dict'] = payload_dict
    token_dict['signature'] = signature
    token_dict['details'] = details_dict

    print_token(token_dict)
    return token_dict


def base64_decode(chunk: str) -> dict:
    """
    Performs Base64-decoding of the provided string and returns a dictionary object representation of the string

    :param chunk: A Base64-encoded string (the JWT header or payload section)
    :return: Dictionary object of the decoded data.
    """

    # Add padding if necessary
    padding = len(chunk) % 4
    if padding != 0:
        chunk += '=' * (4 - padding)

    # Decode the Base64 string to a JSON string
    decoded = base64.urlsafe_b64decode(chunk)
    json_str = decoded.decode('utf-8')

    # Convert JSON string to a Python dictionary
    data_dict = json.loads(json_str)

    return data_dict


def fetch_details(header: dict, payload: dict) -> dict:
    """
    Performs definition lookup of the provided claims from data/claims.json. Runs the data_updater script to create
    this file if it does not already exist.

    :param header: Dictionary object of the Base64 decoded JWT header
    :param payload: Dictionary object of the Base64 decoded JWT payload
    :return: Dictionary object containing all claims from both JWT parts and their definitions
    """
    # Define the file path using os.path.join for cross-platform compatibility
    file_path = os.path.join('data', 'claims.json')

    # Check if the file exists
    if not os.path.exists(file_path):
        # call the data_updater script to create the claims.json file
        src.utils.data_updater.main()

    with open(file_path, 'r', encoding='utf-8') as jsonfile:
        definitions = json.loads(jsonfile.read())

    # Merge the two dictionaries
    combined_dict = {**header, **payload}
    # details_dict[claim] = definition (if exists), else '**Custom Claim**'
    details_dict = {k: definitions['claims'].get(k.lower(), "**Custom Claim**") for k in combined_dict}

    return details_dict


def convert_unix_to_utc(unix_timestamp: int) -> str:
    """
    Takes a Unix Timestamp and returns human-readable UTC time, ex. "2024-01-16 15:15:20 UTC"

    :param unix_timestamp: Integer object representing the Unix timestamp
    :return: Formatted, human-readable time string
    """
    utc_time = datetime.utcfromtimestamp(unix_timestamp)
    return utc_time.strftime('%Y-%m-%d %H:%M:%S UTC')


def create_print_string(claim: str, token_dict: dict) -> str:
    """
    This function is called by print_token to generate a formatted, colored line of output on a per-claim basis.

    An output string is created and built based on the inputted claim. If the claim is a timestamp (exp, iat, nbf
    claims), then convert_unix_to_utc is called to add a human-readable time to the print string. The outputted
    printable strings will look like #1 without the -d 'details' flag, or #2 with the -d flag set
    #1.) ➤  alg: HS256
    #2.) ➤  alg: HS256 - Algorithm used to sign or encrypt the JWT

    :param claim:
    :param token_dict:
    :return:
    """
    # TODO: pull symbol from config file so that users can change it, if needed
    start_symbol = Fore.CYAN+'➤ '
    claim_name = str(claim)
    claim_value = ''
    claim_definition = ''
    is_timestamp = False
    print_str = ''
    if claim_name in token_dict['header_dict']:
        claim_value = str(token_dict['header_dict'][claim_name])
    elif claim_name in token_dict['payload_dict']:
        claim_value = str(token_dict['payload_dict'][claim_name])
    else:
        src.utils.error_handler.print_error('The claim - '+claim+' - was not found')

    if claim_name in ['exp', 'iat', 'nbf']:
        is_timestamp = True

    if token_dict['details']:
        claim_definition = str(token_dict['details'][claim_name])

    if claim_definition:
        print_str = start_symbol+Fore.MAGENTA+' '+claim_name+': '+Fore.CYAN+claim_value+' - '+Fore.MAGENTA+claim_definition+Style.RESET_ALL
    else:
        print_str = start_symbol + Fore.MAGENTA + ' ' + claim_name + ': ' + Fore.CYAN + claim_value + Style.RESET_ALL

    if is_timestamp:
        # logic for printing human-readable UTC time
        print_str += Fore.MAGENTA + ' (' + convert_unix_to_utc(int(claim_value)) + ')' + Style.RESET_ALL

    return print_str


def print_token(token_dict: dict):
    """
    Outputs the decoded token contents and optional details to the terminal

    :param token_dict: Decoded JWT contents in dict object
    :return: None
    """

    print(Fore.MAGENTA+'+----------------------------------+'+Style.RESET_ALL)
    print(Fore.MAGENTA+'|'+Fore.CYAN+'              HEADER              '+Fore.MAGENTA+'|'+Style.RESET_ALL)
    print(Fore.MAGENTA+'+----------------------------------+'+Style.RESET_ALL)

    for claim in token_dict['header_dict']:
        print(create_print_string(claim, token_dict))

    print()
    print(Fore.MAGENTA+'+----------------------------------+'+Style.RESET_ALL)
    print(Fore.MAGENTA+'|'+Fore.CYAN+'              PAYLOAD             '+Fore.MAGENTA+'|'+Style.RESET_ALL)
    print(Fore.MAGENTA+'+----------------------------------+'+Style.RESET_ALL)

    # print timestamps as local time
    for claim in token_dict['payload_dict']:
        print(create_print_string(claim, token_dict))

    print()
    print(Fore.MAGENTA+'+----------------------------------+'+Style.RESET_ALL)
    print(Fore.MAGENTA+'|'+Fore.CYAN+'             SIGNATURE            '+Fore.MAGENTA+'|'+Style.RESET_ALL)
    print(Fore.MAGENTA+'+----------------------------------+'+Style.RESET_ALL)
    print(Fore.CYAN+'➤  '+Fore.MAGENTA+'Signature: ' + Fore.CYAN+str(token_dict['signature'])+Style.RESET_ALL)

    print()

