import os

from core.file_meta_data import FileMetaData, delimiter_encoded
from core.zip_helper import create_zip_from_paths, unzip_to_directory, create_tmp_zip_file


class EncryptionCore:
    def __init__(
            self,
            infile: str,
            outfile: str | None = None,
            files: list | None = None,
            passphrase: str | None = None,
    ):
        if files is None:
            files = []

        self.zip_file = create_tmp_zip_file()
        self.input_file = infile
        self.out_file = outfile or infile
        self.files = files
        self.passphrase = passphrase

    def encrypt(self):
        files = [
            FileMetaData(filename=self.input_file.split('/')[-1], filepath=self.input_file),
            self.zip_file,
        ]

        create_zip_from_paths(self.files, self.zip_file.filepath, self.passphrase)

        with open(self.out_file, 'wb') as outfile:
            for meta in files:
                with open(meta.filepath, 'rb') as infile:
                    for line in infile.readlines():
                        outfile.write(line)

                    outfile.write(meta.encode())

        self.clear()

    def decrypt(self):
        with open(self.input_file, 'rb') as infile:
            file = []
            for line in infile.readlines():
                if delimiter_encoded in line:
                    metadata = FileMetaData(json_data=line.replace(delimiter_encoded, ''.encode()))

                    if metadata.is_zip():
                        self.zip_file = metadata
                        with open(metadata.filepath, 'wb') as outfile:
                            outfile.writelines(file)

                        unzip_to_directory(metadata.filepath, self.passphrase)

                    file = []
                    continue

                file.append(line)

        self.clear()

    def clear(self):
        if os.path.exists(self.zip_file.filepath):
            os.remove(self.zip_file.filepath)
