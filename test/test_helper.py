import uuid
from pydub import AudioSegment
import numpy as np


def is_uuid_v4(s):
    try:
        val = uuid.UUID(s, version=4)

        return val.version == 4
    except ValueError:
        return False


def audio_content_compare(file1: str, file2: str) -> bool:
    # Load the two audio files
    audio1 = AudioSegment.from_mp3(file1)
    audio2 = AudioSegment.from_mp3(file2)

    # Convert to same frame rate and channels for a fair comparison
    audio1 = audio1.set_frame_rate(44100).set_channels(1)
    audio2 = audio2.set_frame_rate(44100).set_channels(1)

    # Getting raw audio data
    samples1 = np.array(audio1.get_array_of_samples())
    samples2 = np.array(audio2.get_array_of_samples())

    # Compare lengths and content
    if len(samples1) != len(samples2):
        return False

    return np.array_equal(samples1, samples2)


def binary_compare(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        content1 = f1.read()
        content2 = f2.read()

    return content1 == content2
