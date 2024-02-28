import uuid


def is_uuid_v4(s):
    try:
        val = uuid.UUID(s, version=4)

        return val.version == 4
    except ValueError:
        return False
