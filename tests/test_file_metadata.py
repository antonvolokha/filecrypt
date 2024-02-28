import json

from core.file_meta_data import FileMetaData


def test_file_metadata_setup():
    filename = 'tests.zip'
    filepath = 'tests/tests.zip'

    meta = FileMetaData(filename=filename, filepath=filepath)

    assert meta.filename == filename
    assert meta.filepath == filepath


def test_file_metadata_setup_filename_only():
    filename = 'tests.zip'
    meta = FileMetaData(filename=filename)

    assert meta.filename == filename
    assert meta.filepath == filename
    assert meta.is_zip()


def test_file_metadata_setup_all_fields():
    filename = 'tests.zip'
    filename_json = 'test2.zip'
    filepath = 'tests/tests.zip'
    json_data = '{"filename": "' + filename_json + '"}'

    meta = FileMetaData(filename=filename, filepath=filepath, json_data=json_data.encode())

    assert meta.filename == filename_json
    assert meta.filepath == filename_json


def test_file_metadata_setup_from_json():
    filename_json = 'test2.zip'
    json_data = '{"filename": "' + filename_json + '"}'

    meta = FileMetaData(json_data=json_data.encode())

    assert meta.filename == filename_json
    assert meta.filepath == filename_json


def test_file_metadata_setup_from_invalid_json():
    filename_json = 'test2.zip'

    try:
        json_data = '{"abracadabra": "' + filename_json + '"}'
        FileMetaData(json_data=json_data.encode())
    except Exception as e:
        assert isinstance(e, KeyError)
        assert "'filename'" in str(e)


def test_file_metadata_setup_from_corupted_json():
    filename_json = 'test2.zip'

    try:
        json_data = '{"abracadabra": "' + filename_json + '"'
        FileMetaData(json_data=json_data.encode())
    except Exception as e:
        assert isinstance(e, json.decoder.JSONDecodeError)
        assert "Expecting ',' delimiter: line 1 column 28 (char 27)" in str(e)


def test_file_metadata_empty():
    meta = FileMetaData()

    assert meta.filename is None
    assert meta.filepath is None


def test_to_json_string():
    filename = 'tests.zip'
    meta = FileMetaData(filename=filename)


def test_encode():
    filename = 'tests.zip'
    delimiter = '===='
    json_data = json.dumps({"filename": filename})
    expected = f"\n{delimiter}{json_data}{delimiter}\n".encode()

    meta = FileMetaData(filename=filename)

    assert expected == meta.encode()


def test_is_zip():
    filename = 'tests.rar'
    meta = FileMetaData(filename=filename)

    assert not meta.is_zip()