'''
Created Date: Friday, March 13th 2020, 12:48:29 am
Author: BaDMaN

Copyright (c) 2020 BaDMaN Soft
'''

from cryptography.fernet import Fernet
from config import keyFileName, keyValue
import os
import zipfile
import json
import argparse


class combinator:
  delimiter = '===='
  zipName = 'data.zip'

  def __init__(self, key: bytes, delimiter = None):
    self.key = key
    if delimiter:
      self.delimiter = delimiter

  def combineFiles(self, infile: str, output: str, filenames: list):
    fernet = Fernet(self.key)

    for i in range(0, len(filenames), 1):
      if os.path.isdir(filenames[i]):
        archiveName = str(i) + self.zipName
        zipf = zipfile.ZipFile(archiveName, 'w', zipfile.ZIP_DEFLATED)
        self.zipdir(filenames[i], zipf)
        zipf.close()

        filenames[i] = archiveName

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

    self.clear()

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

          if '.zip' in info['filename']:
            self.unzipdir(info['filename'], './')

          file = []
          index += 1
          continue

        if index == 0:
          file.append(line)
        elif line != b'\n':
          file.append(fernet.decrypt(line))
        else:
          continue

  def clear(self):
    os.system('rm *.zip')

  def zipdir(self, path: str, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
      for file in files:
          ziph.write(os.path.join(root, file))

  def unzipdir(self, zipFile: str, path: str):
    with zipfile.ZipFile(zipFile, 'r') as zip_ref:
      zip_ref.extractall(path)

def initKey():
  key = Fernet.generate_key()
  with open(keyFileName, "wb") as key_file:
    key_file.write(key)

def loadKey(keyFile):
  if os.path.exists(keyFile) and os.path.isfile(keyFile):
    return open(keyFile, "rb").read()

  return keyValue

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='BaDMaN soft')
  parser.add_argument('-i', '--infile', help='Main file to crypt')
  parser.add_argument('-o', '--outfile', help='Output file')
  parser.add_argument('-f', '--files', nargs='+', help='files to encrypr or folder')
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
  elif args.infile and args.files:
    if args.outfile == None:
      args.outfile = args.infile

    com.combineFiles(args.infile, args.outfile, args.files)
  else:
    raise Exception('Arguments is empty')