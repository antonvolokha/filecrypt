import os
import shutil
import tempfile

from core.zip_helper import create_tmp_zip_file, create_zip_from_paths, unzip_to_directory
from test.test_helper import is_uuid_v4


def test_create_tmp_zip_file():
    path = create_tmp_zip_file()
    tmp_path = tempfile.gettempdir()

    filename = path.filename.split('.')[0]
    fileext = path.filename.split('.')[1]
    filepath = '/'.join(path.filepath.split('/')[0:-1])

    print('\n')
    print(filepath, '\n', tmp_path)

    assert filepath == tmp_path
    assert 'zip' == fileext
    assert is_uuid_v4(filename)


def test_zip_without_pass():
    files = ['test/data/song_orig.mp3', 'test/data/very_secret_doc.pdf']
    arch_name = 'test_arch'
    arch_file = f'{arch_name}.zip'
    create_zip_from_paths(paths=files, output_zip_file=arch_file)

    assert os.path.isfile(arch_file)

    unzip_to_directory(arch_file)
    os.remove(arch_file)

    assert os.path.isdir(arch_name)
    dir_content = os.listdir(arch_name)
    assert len(dir_content) == len(files)
    shutil.rmtree(arch_name)


def test_zip_with_pass_success():
    files = ['test/data/song_orig.mp3', 'test/data/very_secret_doc.pdf']
    arch_name = 'test_arch'
    arch_file = f'{arch_name}.zip'
    password = '1234'

    create_zip_from_paths(paths=files, output_zip_file=arch_file, password=password)

    assert os.path.isfile(arch_file)

    unzip_to_directory(arch_file, password=password)
    os.remove(arch_file)

    assert os.path.isdir(arch_name)
    dir_content = os.listdir(arch_name)
    assert len(dir_content) == len(files)
    shutil.rmtree(arch_name)


def test_zip_with_pass_failed():
    files = ['test/data/song_orig.mp3', 'test/data/very_secret_doc.pdf']
    arch_name = 'test_arch'
    arch_file = f'{arch_name}.zip'
    password = '1234'

    create_zip_from_paths(paths=files, output_zip_file=arch_file, password=password)

    assert os.path.isfile(arch_file)

    try:
        unzip_to_directory(arch_file)
    except Exception as e:
        assert 'WZ_AES encryption and requires a password.' in str(e)

    os.remove(arch_file)


def test_zip_with_pass_wrong():
    files = ['test/data/song_orig.mp3', 'test/data/very_secret_doc.pdf']
    arch_name = 'test_arch'
    arch_file = f'{arch_name}.zip'
    password = '1234'

    create_zip_from_paths(paths=files, output_zip_file=arch_file, password=password)

    assert os.path.isfile(arch_file)

    try:
        unzip_to_directory(arch_file, password='wrong')
    except Exception as e:
        assert 'Bad password exception' in str(e)

    os.remove(arch_file)
