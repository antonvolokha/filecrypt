import os
import shutil

from core.encryption_core import EncryptionCore
from test.test_helper import audio_content_compare, binary_compare


def test_encrypt_without_pass():
    input_file = 'test/data/song_orig.mp3'
    out_file = 'out.mp3'
    files = ['test/data/very_secret_doc.pdf']

    core = EncryptionCore(
        infile=input_file,
        outfile=out_file,
        files=files,
    )

    core.encrypt()

    assert os.path.isfile(out_file)
    assert audio_content_compare(input_file, out_file)

    os.remove(out_file)


def test_encrypt_with_pass():
    input_file = 'test/data/song_orig.mp3'
    out_file = 'out.mp3'
    files = ['test/data/very_secret_doc.pdf']
    password = 'myawesomepass'

    core = EncryptionCore(
        infile=input_file,
        outfile=out_file,
        files=files,
        passphrase=password
    )

    core.encrypt()

    assert os.path.isfile(out_file)
    assert audio_content_compare(input_file, out_file)

    os.remove(out_file)


def test_decrypt_without_pass():
    input_file = 'test/data/out_without_pwd.mp3'
    out_folder = 'db0c7f89-f931-4e51-919d-1c91375f3742'
    out_file = f'{out_folder}/very_secret_doc.pdf'
    orig_file = 'test/data/very_secret_doc.pdf'

    core = EncryptionCore(infile=input_file)

    core.decrypt()

    assert os.path.isdir(out_folder)
    assert os.path.isfile(out_file)

    assert binary_compare(out_file, orig_file)
    shutil.rmtree(out_folder)


def test_decrypt_with_pass():
    input_file = 'test/data/out_with_password.mp3'
    out_folder = '55b32fdd-5daf-4a05-bb54-8c5bfd17cc18'
    out_file = f'{out_folder}/very_secret_doc.pdf'
    orig_file = 'test/data/very_secret_doc.pdf'
    password = 'myawesomepass'

    core = EncryptionCore(infile=input_file, passphrase=password)

    core.decrypt()

    assert os.path.isdir(out_folder)
    assert os.path.isfile(out_file)

    assert binary_compare(out_file, orig_file)
    shutil.rmtree(out_folder)


def test_decrypt_with_invalid_pass():
    input_file = 'test/data/out_with_password.mp3'
    out_folder = '55b32fdd-5daf-4a05-bb54-8c5bfd17cc18'
    password = 'invalidpasswprd'

    core = EncryptionCore(infile=input_file, passphrase=password)

    try:
        core.decrypt()
    except Exception as e:
        assert 'Bad password for file' in str(e)

