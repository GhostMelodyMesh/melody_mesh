from src.compressors.CompressorAbstract import CompressorAbstract


class Compressor(CompressorAbstract):
    def compress(self, file_path):
        pass

    def remove_redundancy(self, file):
        pass

    def lower_quality(self, data, quality):
        pass
