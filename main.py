'''
Created Date: Friday, March 13th 2020, 12:48:29 am
Author: BaDMaN

Copyright (c) 2020 BaDMaN Soft
'''

from cryptography.fernet import Fernet
from config import keyFileName
import json
import argparse


class combinator:
  delimiter = '===='

  def __init__(self, key: bytes, delimiter = None):
    self.key = key
    if delimiter:
      self.delimiter = delimiter

  def combineFiles(self, infile: str, output: str, filenames: list):
    fernet = Fernet(self.key)
    filenames.insert(0, infile)

    with open(output, 'wb') as outfile:
      index = 0
      for fname in filenames:
        with open(fname, 'rb') as infile:
          infile = infile.readlines()
          for line in infile:
            if index == 0:
              outfile.write(line)
            else:
              outfile.write(fernet.encrypt(line) + "\n".encode())

          outfile.write(("\n" + self.delimiter + json.dumps({'filename': fname.split('/')[-1]}) + self.delimiter + "\n").encode())

        index += 1

  def decombain(self, inputFile: str):
    fernet = Fernet(self.key)
    with open(inputFile, 'rb') as infile:
      file = []
      index = 0
      for line in infile.readlines():
        if self.delimiter.encode() in line:
          line = line.replace(self.delimiter.encode(), ''.encode())
          info = json.loads(line)
          with open(info['filename'], 'wb') as outfile:
            outfile.writelines(file)

          file = []
          index += 1
          continue

        if index == 0:
          file.append(line)
        elif line != b'\n':
          print(line)
          file.append(fernet.decrypt(line))
        else:
          continue

def initKey():
  key = Fernet.generate_key()
  with open(keyFileName, "wb") as key_file:
    key_file.write(key)

def loadKey(keyFile):
  return open(keyFile, "rb").read()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='BaDMaN soft')
  parser.add_argument('-i', '--infile', help='Main file to crypt')
  parser.add_argument('-o', '--outfile', help='Output file')
  parser.add_argument('-f', '--files', nargs='+', help='files to encrypr')
  parser.add_argument('-d', '--decrypt',  action='store_true', help='Decrypt flag')
  parser.add_argument('-k', '--key', help='keyfile', default=keyFileName)
  parser.add_argument('--init', action='store_true', help='Init new key')

  args = parser.parse_args()

  if args.init:
    initKey()

  key = loadKey(args.key)
  com = combinator(key)

  if args.decrypt and args.infile:
    com.decombain(args.infile)
  elif args.infile and args.outfile and args.files:
    com.combineFiles(args.infile, args.outfile, args.files)
  else:
    raise Exception('Arguments is empty')