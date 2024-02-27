import getpass
from argparse import Namespace

def print_logo():
    print('    ._______ .______  .______  ._____.___ .______  .______       ._______ .______   ____   ____._______ _____._._______      ')
    print('    : __   / :      \\ :_ _   \\ :         |:      \\ :      \\      :_.  ___\\: __   \\  \\   \\_/   /: ____  |\\__ _:|: .___  \\     ')
    print('    |  |>  \\ |   .   ||   |   ||   \\  /  ||   .   ||       |     |  : |/\\ |  \\____|  \\___ ___/ |    :  |  |  :|| :   |  |    ')
    print('    |  |>   \\|   :   || . |   ||   |\\/   ||   :   ||   |   |     |    /  \\|   :  \\     |   |   |   |___|  |   ||     :  |    ')
    print('    |_______/|___|   ||. ____/ |___| |   ||___|   ||___|   |     |. _____/|   |___\\    |___|   |___|      |   | \\_. ___/     ')
    print('                 |___| :/            |___|    |___|    |___|      :/      |___|                           |___|   :/         ')
    print('                       :                                          :                                               :          ')
    print('                                                                                                                             ')
    print('                                                                                                                             ')





def passphrase_input():
    passphrase = getpass.getpass("Your password: ")
    if len(passphrase) == 0:
        passphrase = None

    return passphrase


def encrypt_menu() -> Namespace:
    infile = input("File container: ")
    outfile = input("Output file: ")
    files_input = input("Files to encrypt or folder (separate with space): ")
    files = files_input.split() if files_input else []
    decrypt = False
    passphrase = passphrase_input()

    return Namespace(infile=infile, outfile=outfile, files=files, decrypt=decrypt, passphrase=passphrase)


def decrypt_menu() -> Namespace:
    infile = input("File to decrypt: ")
    decrypt = True
    passphrase = passphrase_input()

    return Namespace(infile=infile, decrypt=decrypt, passphrase=passphrase)


def main_menu() -> Namespace:
    print_logo()
    while True:
        print("[1] Encrypt")
        print("[2] Decrypt")
        print("[0] Exit")
        action = int(input())

        if action == 1:
            return encrypt_menu()
        elif action == 2:
            return decrypt_menu()
        elif action == 0:
            exit(0)
        else:
            print("Invalid option, try again")

        print("\n\n")
