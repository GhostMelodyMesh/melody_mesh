from src.dataTypes.AudioFormat import AudioFormat
from src.fileHandlers.AudioFileHandler import AudioFileHandler

print("Hello World!")
# c = CompressorWAVBaseline()
# c.compress("rawAudio/file0.mp3")
# fReader = AudioFileHandler()
# audio = fReader.read_as_wav("rawAudio/file0.mp3")

fp = AudioFileHandler()
audio1 = fp.read(file_path="compressedAudio/file0.wav", return_audio_type=AudioFormat.WAV)
# save
fp.write(audio1, file_path="compressedAudio/file0.wav")
