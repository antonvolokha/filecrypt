import os
from typing import Tuple

import pyzipper
import uuid
import tempfile

from core.exception.bad_passwprd_exception import BadPasswordException
from core.file_meta_data import FileMetaData


def create_zip_from_paths(paths: list, output_zip_file: str, password: str | None = None) -> str:
    """
     Creates a password-protected zip file using pyzipper with AES encryption.

     :param paths: A list of paths to files or directories to include in the zip file.
     :param output_zip_file: The output file path for the zip file.
     :param password: The password for encrypting the zip file.
     """
    with pyzipper.AESZipFile(output_zip_file,
                             'w',
                             compression=pyzipper.ZIP_DEFLATED,
                             encryption=pyzipper.WZ_AES if password is not None else None,
                             ) as zf:
        if password is not None:
            zf.setpassword(password.encode('utf-8'))

        for path in paths:
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zf.write(file_path, arcname=os.path.relpath(file_path, os.path.split(path)[0]))
            else:
                zf.write(path, arcname=os.path.basename(path))

        return zf.filename


def unzip_to_directory(zip_file_path: str, password: str | None = None):
    """
    Unzips a zip file into a directory with the same name as the zip file (excluding the extension).

    :param zip_file_path: The path to the zip file.
    :param password: Optional. The password used for decrypting the zip file. If None, assumes the zip file is not encrypted
    """
    # Extract the directory name from the zip file path and remove the extension
    output_directory = os.path.splitext(zip_file_path)[0]

    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        with pyzipper.AESZipFile(zip_file_path, 'r') as zip_ref:
            if password is not None:
                zip_ref.pwd = password.encode('utf-8')
            zip_ref.extractall(output_directory)

    except Exception as e:
        os.rmdir(output_directory)

        if 'Bad password for file' in str(e):
            raise BadPasswordException()

        raise e


def create_tmp_zip_file() -> FileMetaData:
    zip_filename = f'{str(uuid.uuid4())}.zip'
    metadata = FileMetaData(filename=zip_filename, filepath=f'{tempfile.gettempdir()}/{zip_filename}')

    return metadata
