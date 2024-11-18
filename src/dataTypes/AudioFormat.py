from enum import Enum


class AudioFormat(Enum):
    MP3 = "mp3"
    WAV = "wav"
    MIDI = "midi"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"AudioType.{self.name}"

    def __eq__(self, other):
        if isinstance(other, AudioFormat):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        return False

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def from_str(cls, label):
        for item in cls:
            if item.value == label:
                return item
        raise ValueError(f"'{label}' is not a valid AudioType")
