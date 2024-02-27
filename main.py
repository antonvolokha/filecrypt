"""
Created Date: Friday, March 13th 2020, 12:48:29 am
Author: BaDMaN

Copyright (c) 2024 BaDMaN Soft
"""

import argparse
from core.encryption_core import EncryptionCore


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BaDMaN soft')
    parser.add_argument('-i', '--infile', help='Main file to crypt')
    parser.add_argument('-o', '--outfile', help='Output file')
    parser.add_argument('-f', '--files', nargs='+', help='files to encrypr or folder')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt flag')
    parser.add_argument('-p', '--passphrase', help='Your password')

    args = parser.parse_args()

    core = EncryptionCore(
        infile=args.infile,
        outfile=args.outfile,
        files=args.files,
        passphrase=args.passphrase
    )

    if args.decrypt and args.infile:
        core.decrypt()
    elif args.infile:
        core.encrypt()
    else:
        raise Exception('Arguments is empty')
