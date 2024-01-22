
import sys
import random
from colorama import Fore, Style

ascii_fart = [
    Fore.GREEN+"""
  _______    ____
 /       \  |  o |    ,--------------------------------.
|  {}  |/ ___\|  <( Somewhere, something went wrong. )
|__________/          `--------------------------------^
|_|_| |_|_|""".format(Fore.RED+"ERROR"+Fore.GREEN)+Style.RESET_ALL,
    Fore.GREEN+"""
 _    _
(o)__(o)   
 \ .. /    ,--------------------------------.
 ==\/==  <( Somewhere, something went wrong. )
 (m  m)    `--------------------------------^
m(____)m"""+Style.RESET_ALL,
    Fore.GREEN+"""
            __
(\,--------'()'--o   ,--------------------------------.
 (_    ___    /~"  <( Somewhere, something went wrong. )
  (_)_)  (_)_)       `--------------------------------^"""+Style.RESET_ALL
]


def print_error(error_msg: str):
    # randomly select ASCII art
    ascii_art = random.choice(ascii_fart)

    # print the ASCII art and error message
    print(ascii_art)
    print(Fore.RED+'ERROR:', error_msg+Style.RESET_ALL)
    print()
    sys.exit(1)


# example usage
if __name__ == "__main__":
    print_error("Example error message.")

