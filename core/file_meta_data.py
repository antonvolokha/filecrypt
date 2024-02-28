import json

delimiter = '===='
delimiter_encoded = delimiter.encode()


class FileMetaData:
    def __init__(self, filename: str | None = None, filepath: str | None = None, json_data: bytes | None = None):
        if json_data is not None:
            info = json.loads(json_data)
            filename = info['filename']
            filepath = filename

        self.filename = filename
        self.filepath = filepath or filename

    def to_json_string(self):
        return json.dumps({"filename": self.filename})

    def encode(self) -> bytes:
        return f"\n{delimiter}{self.to_json_string()}{delimiter}\n".encode()

    def is_zip(self) -> bool:
        return '.zip' in self.filename
