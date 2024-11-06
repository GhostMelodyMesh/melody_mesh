from src.compressors.CompressorAbstract import CompressorAbstract
from src.dataTypes.AudioWAV import AudioWAV


class CompressorWAVTeamName(CompressorAbstract):
    def compress(self, file_path: str) -> str:
        raise NotImplementedError

    def remove_redundancies(self, file: AudioWAV) -> AudioWAV:
        raise NotImplementedError

    def select_from_redundancy_group(self, file: AudioWAV, group: list[tuple[int, int]]) -> tuple[int, int]:
        raise NotImplementedError

    def group_redundancies(self, file: AudioWAV) -> list[list[tuple[int, int]]]:
        raise NotImplementedError

    def lower_quality(self, file: AudioWAV, sample_rate: int) -> AudioWAV:
        raise NotImplementedError
