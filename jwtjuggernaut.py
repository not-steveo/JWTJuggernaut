# -*- coding: utf-8 -*-
"""
JWTJuggernaut: A tool for testing JWT vulnerabilities

This module implements the command-line interface functionality for JWTJuggernaut, providing
various modes and options for using the tool.

Author: not-steveo / Taylor O'Dell

Example:
    $ python3 jwtjuggernaut.py scan --token <token> --url <url>
"""

import sys
import argparse
import colorama
from colorama import Fore, Style

import src.utils.parse_token


def main():
    """
    Main function for JWTJuggernaut

    This function sets up the command-line interface for the script, parses the provided arguments, and
    initiates the appropriate functions based on the user-selected modes and options. It acts as the central
    control mechanism for the tool.
    :return: None
    """
    parser = argparse.ArgumentParser(description='JWTJuggernaut: A tool for testing JWT vulnerabilities')
    # parser.add_argument('-t', '--token', help="JWT to test", required=False)

    subparsers = parser.add_subparsers(dest='command', help='Sub-commands for different modes')

    # READ mode
    parser_read = subparsers.add_parser('read', help='Read mode - view available details about provided JWT')
    parser_read.add_argument('-t', '--token', required=False, help='JWT to test')
    parser_read.add_argument('-r', '--request', required=False, help='File containing HTTP request')
    parser_read.add_argument('-d', '--details', required=False, action='store_true',
                             help='Output additional details about the token claims')

    # TAMPER mode
    parser_tamper = subparsers.add_parser('tamper', help='Tamper mode - edit the provided token')
    parser_tamper.add_argument('-t', '--token', required=False, help='JWT to test')
    parser_tamper.add_argument('-r', '--request', required=False, help='File containing HTTP request')
    parser_tamper.add_argument('-w', '--wizard', required=False, action='store_true',
                               help='Interactive wizard to add or edit header/payload claims')
    parser_tamper.add_argument('-hc', '--header_claim', required=False, help='Header claim to edit or add')
    parser_tamper.add_argument('-hv', '--header_value', required=False, help='Header value to edit or add')
    parser_tamper.add_argument('-pc', '--payload_claim', required=False, help='Payload claim to edit or add')
    parser_tamper.add_argument('-pv', '--payload_value', required=False, help='Payload value to edit or add')

    # BRUTEFORCE mode
    parser_brute = subparsers.add_parser('bruteforce', help='Bruteforce mode - bruteforce the JWT signing key')
    parser_brute.add_argument('-t', '--token', required=True, help='JWT to test')
    parser_brute.add_argument('-tk', '--token_key', required=False, help='Single signing key to test against JWT')
    parser_brute.add_argument('-D', '--dict', required=False, help='List of signing keys to test')

    # ATTACK mode
    parser_attack = subparsers.add_parser('attack',
                                          help='Attack mode - attempting common JWT attacks against the provided URL, or outputting altered JWTs that can be used to test for vulnerabilities')
    parser_attack.add_argument('-r', '--request', required=False, help='File containing HTTP request')
    parser_attack.add_argument('-w', '--wizard', required=False, action='store_true',
                               help='Interactive wizard that builds the request for you')
    parser_attack.add_argument('-t', '--token', required=False, help='JWT to test')
    parser_attack.add_argument('-rv', '--request_verb', required=False,
                               help='HTTP Method to use when making requests (supported: GET, POST, PUT, DELETE)')
    parser_attack.add_argument('-u', '--url', required=False, help='Target URL to test against')
    parser_attack.add_argument('-rh', '--request_header', required=False,
                               help='Request headers to send - can be used more than once or provide a semi-colon delimited list')
    parser_attack.add_argument('-rc', '--request_cookie', required=False,
                               help='Request cookies to send - can be used more than once or provide a semi-colon delimited list')

    # parse the arguments provided
    args = parser.parse_args()
    print(args)

    # implement post-parsing checks to ensure arguments are logically provided
    # @TODO: add functionality (regex) to check that tokens are in correct format
    # re.search('eyJ[A-Za-z0-9_\/+-]*\.eyJ[A-Za-z0-9_\/+-]*\.[A-Za-z0-9._\/+-]*', <targetString>)
    if args.command.lower() == 'read':
        if not args.token and not args.request:
            parser.error(
                Fore.RED+'Please provide either a JWT using the -t flag or an HTTP request in a txt file using the -r flag.'+Style.RESET_ALL)
        if args.request:
            # parse JWT from request
            pass
        # pass token (provided by user or parsed from request) to read_token functionality
        # pass details flag as well
        src.utils.parse_token.parse_token(args.token, args.details)
    elif args.command.lower() == 'tamper':
        if not args.token and not args.request and not args.wizard:
            parser.error(
                Fore.RED+'Please provide either a JWT using the -t flag or an HTTP request in a txt file with the -r flag. Alternatively, use the interactive wizard by using the -w flag.'+Style.RESET_ALL)
        if args.wizard:
            # make this implied functionality if no additional args like -hc/-hv or -pc/-pv are used @TODO: how?
            # call wizard functionality, maybe pass in 'tamper' command as well
            # call before token functionality to allow user to do -t <token> -w OR -r <request.txt> -w
            # if token is provided, pass to wizard and don't ask for it
            pass
        if args.request:
            # parse JWT from request
            # check for additional parameters
            # if no additional parameters, pass to wizard
            # call tamper functionality
            pass
        if args.token:
            # check for additional parameters
            # if no additional parameters, pass to wizard
            pass
    elif args.command.lower() == 'bruteforce' or args.command.lower() == 'brute':
        if not args.token:
            parser.error(Fore.RED+'Please provide a JWT using the -t flag.'+Style.RESET_ALL)
        if not args.token_key or not args.dict:
            parser.error(Fore.RED+'Either a single key must be provided using the -tk flag, or a text file list of keys provided using the -D flag.'+Style.RESET_ALL)
    elif args.command.lower() == 'attack':
        if not args.token and not args.request and not args.wizard:
            parser.error(
                Fore.RED+'Please provide either a JWT using the -t flag or an HTTP request in a txt file using the -r flag. Alternatively, use the interactive wizard by using the -w flag.'+Style.RESET_ALL)
    else:
        print(Fore.RED+'Invalid command. Use -h for help.'+Style.RESET_ALL)
        sys.exit(1)


def print_logo():
    print()
    print(
        Fore.MAGENTA + "     ██" + Fore.CYAN + "╗" + Fore.MAGENTA + "██" + Fore.CYAN + "╗" + Fore.MAGENTA + "    ██" + Fore.CYAN + "╗" + Fore.MAGENTA + "████████" + Fore.CYAN + "╗" + Fore.MAGENTA + "  ██" + Fore.CYAN + "╗" + Fore.MAGENTA + "██" + Fore.CYAN + "╗" + Fore.MAGENTA + "   ██" + Fore.CYAN + "╗" + Fore.MAGENTA + " ██████" + Fore.CYAN + "╗" + Fore.MAGENTA + "  ██████" + Fore.CYAN + "╗" + Fore.MAGENTA + " ███████" + Fore.CYAN + "╗" + Fore.MAGENTA + "██████" + Fore.CYAN + "╗" + Fore.MAGENTA + " ███" + Fore.CYAN + "╗" + Fore.MAGENTA + "   ██" + Fore.CYAN + "╗" + Fore.MAGENTA + " █████" + Fore.CYAN + "╗" + Fore.MAGENTA + " ██" + Fore.CYAN + "╗" + Fore.MAGENTA + "   ██" + Fore.CYAN + "╗" + Fore.MAGENTA + "████████" + Fore.CYAN + "╗" + Style.RESET_ALL)
    print(
        Fore.MAGENTA + "     ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "    ██" + Fore.CYAN + "║╚══" + Fore.MAGENTA + "██" + Fore.CYAN + "╔══╝" + Fore.MAGENTA + "  ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "╔════╝" + Fore.MAGENTA + " ██" + Fore.CYAN + "╔════╝" + Fore.MAGENTA + " ██" + Fore.CYAN + "╔════╝" + Fore.MAGENTA + "██" + Fore.CYAN + "╔══" + Fore.MAGENTA + "██" + Fore.CYAN + "╗" + Fore.MAGENTA + "████" + Fore.CYAN + "╗" + Fore.MAGENTA + "  ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "╔══" + Fore.MAGENTA + "██" + Fore.CYAN + "╗" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║╚══" + Fore.MAGENTA + "██" + Fore.CYAN + "╔══╝" + Style.RESET_ALL)
    print(
        Fore.MAGENTA + "     ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + " █" + Fore.CYAN + "╗" + Fore.MAGENTA + " ██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "     ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "  ███" + Fore.CYAN + "╗" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "  ███" + Fore.CYAN + "╗" + Fore.MAGENTA + "█████" + Fore.CYAN + "╗" + Fore.MAGENTA + "  ██████" + Fore.CYAN + "╔╝" + Fore.MAGENTA + "██" + Fore.CYAN + "╔" + Fore.MAGENTA + "██" + Fore.CYAN + "╗" + Fore.MAGENTA + " ██" + Fore.CYAN + "║" + Fore.MAGENTA + "███████" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║   " + Style.RESET_ALL)
    print(
        Fore.MAGENTA + "██   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "███" + Fore.CYAN + "╗" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "╔══╝" + Fore.MAGENTA + "  ██" + Fore.CYAN + "╔══" + Fore.MAGENTA + "██" + Fore.CYAN + "╗" + Fore.MAGENTA + "██" + Fore.CYAN + "║╚" + Fore.MAGENTA + "██" + Fore.CYAN + "╗" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "╔══" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║   " + Style.RESET_ALL)
    print(
        Fore.CYAN + "╚" + Fore.MAGENTA + "█████" + Fore.CYAN + "╔╝╚" + Fore.MAGENTA + "███" + Fore.CYAN + "╔" + Fore.MAGENTA + "███" + Fore.CYAN + "╔╝" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║╚" + Fore.MAGENTA + "█████" + Fore.CYAN + "╔╝╚" + Fore.MAGENTA + "██████" + Fore.CYAN + "╔╝╚" + Fore.MAGENTA + "██████" + Fore.CYAN + "╔╝╚" + Fore.MAGENTA + "██████" + Fore.CYAN + "╔╝" + Fore.MAGENTA + "███████" + Fore.CYAN + "╗" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "  ██" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║ ╚" + Fore.MAGENTA + "████" + Fore.CYAN + "║" + Fore.MAGENTA + "██" + Fore.CYAN + "║" + Fore.MAGENTA + "  ██" + Fore.CYAN + "║╚" + Fore.MAGENTA + "██████" + Fore.CYAN + "╔╝" + Fore.MAGENTA + "   ██" + Fore.CYAN + "║   " + Style.RESET_ALL)
    print(
        Fore.CYAN + " ╚════╝  ╚══╝╚══╝    ╚═╝ ╚════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   " + Style.RESET_ALL)
    print(
        Fore.MAGENTA + "Developed by:" + Fore.CYAN + "  @not_steveo / Taylor O'Dell" + Fore.MAGENTA + "   Version: 1.0" + Style.RESET_ALL)
    print()


if __name__ == '__main__':
    colorama.init(autoreset=True)
    print_logo()
    main()
