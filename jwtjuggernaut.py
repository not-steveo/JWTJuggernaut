"""
JWTJuggernaut: A tool for testing JWT vulnerabilities

This module implements the command-line interface functionality for JWTJuggernaut, providing
various modes and options for using the tool.

Author: Taylor O'Dell

Example:
    $ python3 jwtjuggernaut.py scan --token <token> --url <url>
"""

import argparse


def main():
    """
    Main function for JWTJuggernaut

    This function sets up the command-line interface for the script, parses the provided arguments, and
    initiates the appropriate functions based on the user-selected modes and options. It acts as the central
    control mechanism for the tool.
    :return: None
    """
    parser = argparse.ArgumentParser(description='JWTJuggernaut: A tool for testing JWT vulnerabilities')

    subparsers = parser.add_subparsers(dest='command', help='Sub-commands for different modes')

    # READ mode
    parser_read = subparsers.add_parser('read', help='Read mode - view available details about provided JWT')
    parser_read.add_argument('-t', '--token', required=True, help='JWT to test')

    # TAMPER mode
    parser_tamper = subparsers.add_parser('tamper', help='Tamper mode - edit the provided token')
    parser_tamper.add_argument('-t', '--token', required=True, help='JWT to test')
    parser_tamper.add_argument('hc', '--header-claim', required=False, help='Header claim to edit or add')
    parser_tamper.add_argument('-hv', '--header-value', required=False, help='Header value to edit or add')
    parser_tamper.add_argument('-pc', '--payload-claim', required=False, help='Payload claim to edit or add')
    parser_tamper.add_argument('-pv', '--payload-value', required=False, help='Payload value to edit or add')

    # BRUTEFORCE mode
    parser_brute = subparsers.add_parser('bruteforce', help='Bruteforce mode - bruteforce the JWT signing key')
    parser_brute.add_argument('-t', '--token', required=True, help='JWT to test')
    parser_brute.add_argument('-tk', '--token-key', required=False, help='Single signing key to test against JWT')
    parser_brute.add_argument('-D', '--dict', required=False, help='List of signing keys to test')

    # ATTACK mode
    parser_attack = subparsers.add_parser('attack', help='Attack mode - attempting common JWT attacks against the provided URL, or outputting altered JWTs that can be used to test for vulnerabilities')
    parser_attack.add_argument('-t', '--token', required=True, help='JWT to test')
    parser_attack.add_argument('-r', '--request', required=False, help='File containing HTTP request')
    parser_attack.add_argument('-rv', '--request-verb', required=False, help='HTTP Method to use when making requests (supported: GET, POST, PUT, DELETE)')
    parser_attack.add_argument('-u', '--url', required=False, help='Target URL to test against')
    parser_attack.add_argument('-rh', '--request-header', required=False, help='Request headers to send - can be used more than once or provide a semi-colon delimited list')
    parser_attack.add_argument('-rc', '--request-cookie', required=False, help='Request cookies to send - can be used more than once or provide a semi-colon delimited list')


if __name__ == '__main__':
    main()
