from src.compressors.ICompress import ICompress
from src.compressors.bitrateDecreasers.DecreaseBitrateWAVFourier import DecreaseBitrateWAVFourier
from src.compressors.monoMakers.MakeMonoWAVGetFirstChannel import MakeMonoWAVGetFirstChannel
from src.compressors.redundanciesRemover.RemoveRedundanciesWAVMatchSimNCC import RemoveRedundanciesWAVMatchSimNCC
from src.compressors.trimmers.TrimWAVEnds10Percent import TrimWAVEnds10Percent
from src.dataTypes.AudioFormat import AudioFormat
from src.fileHandlers.AudioFileHandler import AudioFileHandler


class CompressorWAVBaseline(ICompress):
    def compress(self, file_path: str) -> str:
        file_handler = AudioFileHandler()
        audio = file_handler.read(file_path, AudioFormat.WAV)
        
        TrimWAVEnds10Percent().trim(audio)
        DecreaseBitrateWAVFourier().decrease_bitrate(audio, 3000)
        MakeMonoWAVGetFirstChannel().make_mono(audio)
        RemoveRedundanciesWAVMatchSimNCC(seg_len_secs=0.6, sim_threshold=0.25).remove_redundancies(audio)
        
        new_file_path = "compressedAudio/" + file_path.split(".")[0].split("/")[-1] + ".wav"        
        file_handler.write(audio, new_file_path)