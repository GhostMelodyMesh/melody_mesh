import numpy as np
import scipy.signal
from src.compressors.CompressorAbstract import CompressorAbstract
from src.dataTypes.AudioWAV import AudioWAV
from src.fileHandlers.AudioFileHandler import AudioFileHandler


class CompressorWAVBaseline(CompressorAbstract):
    def compress(self, file_path: str) -> str:
        file_handler = AudioFileHandler()
        audio_wav = file_handler.read_as_wav(file_path)
        audio_wav = self.convert_to_mono(audio_wav)
        audio_wav = self.lower_quality(audio_wav, 4410)
        audio_wav = self.remove_redundancies(audio_wav)
            
        raise NotImplementedError

    def remove_redundancies(self, file: AudioWAV, seg_len_secs: float = 0.5, init_precision: int = 50, precision_reduction: int = 5, sim_threshold: float = 0.8) -> AudioWAV:
        if file.n_channels != 1:
            raise ValueError("Audio file must be mono")
        if seg_len_secs <= 0:
            raise ValueError("Segment length must be positive")
        if init_precision <= 0:
            raise ValueError("Initial precision must be positive")
        if precision_reduction <= 0:
            raise ValueError("Precision reduction must be positive")
        
        groups = self.group_redundancies(file, seg_len_secs, init_precision, precision_reduction, sim_threshold)
        selected_segments = []
        for group in groups:
            selected_segments.append(self.select_from_redundancy_group(file, group))
        
        # Create a new audio file with the selected segments
        new_n_samples = sum([end - start for start, end in selected_segments])
        new_audio = np.zeros(new_n_samples, dtype=np.int16)
        offset = 0
        for start, end in selected_segments:
            new_audio[offset:offset + end - start] = file.audio[start:end]
            offset += end - start
        
        file.audio = new_audio
        file.n_samples = new_n_samples
        return file

    def select_from_redundancy_group(self, file: AudioWAV, group: list[tuple[int, int]]) -> tuple[int, int]:
        # Select a segment with the highest energy
        energies = [np.sum(file.audio[start:end] ** 2) for start, end in group]
        selected_index = np.argmax(energies)
        return group[selected_index]

    def group_redundancies(self, file: AudioWAV, seg_len_secs: float = 0.5, init_precision: int = 50, precision_reduction: int = 5, sim_threshold: float = 0.8) -> list[list[list[int]]]:
        """ Returns a list of groups of segments that are similar to each other, each segment is represented by a list of indices """
        groups: list[list[list[int]]] = []
        seg_len = int(seg_len_secs * file.sample_rate)
        audio_copy = file.audio.copy()
        remaining_indices = [i for i in range(len(audio_copy))]
        while len(audio_copy) > 0:
            # If there are not enough samples left to form a segment, add the remaining indices to a new group
            if len(audio_copy) < seg_len:
                groups.append([remaining_indices])
                
            group: list[list[int]] = []
            # Select a random segment, we will look for segments similar to this one
            start_sample = np.random.randint(0, len(audio_copy) - seg_len)
            group.append(remaining_indices[start_sample:start_sample + seg_len])
            
            # Remove the segment from the audio and the list of remaining indices
            audio_copy = np.delete(audio_copy, slice(start_sample, start_sample + seg_len))
            remaining_indices = remaining_indices[:start_sample] + remaining_indices[start_sample + seg_len:]
            
            # Find similar segments
            while len(audio_copy) >= seg_len:
                precision = init_precision
                similarities = []
                offset = 0
                while offset < len(audio_copy) - seg_len:
                    segment = audio_copy[offset:offset + seg_len]
                    similarity = self.NCC(segment, start_sample)
                    similarities.append(similarity)
                    offset += precision
                best_match_index = np.argmax(similarities)
                offset = best_match_index * precision
                
                # Decrease the precision and find the best match in the neighbourhood
                best_similarity = 1
                while precision > 1:
                    left = max(0, offset - precision)
                    right = min(len(audio_copy) - seg_len, offset + precision)
                    if (precision_reduction > precision):
                        precision = 1
                    else:
                        precision //= precision_reduction
                    similarities = []
                    offset = left
                    while offset < right:
                        segment = audio_copy[offset:offset + seg_len]
                        similarity = self.NCC(segment, start_sample)
                        similarities.append(similarity)
                        offset += precision
                    best_match_index = np.argmax(similarities)
                    best_similarity = similarities[best_match_index]
                    offset = left + best_match_index * precision
                
                # If the best match is not similar enough, stop
                if best_similarity < sim_threshold:
                    break
                
                # Add the segment to the group
                group.append(remaining_indices[offset:offset + seg_len])
                
                # Remove the segment from the audio and the list of remaining indices
                audio_copy = np.delete(audio_copy, slice(offset, offset + seg_len))
                remaining_indices = remaining_indices[:offset] + remaining_indices[offset + seg_len:]
        
            groups.append(group)
            
        return groups
                
            

    def lower_quality(self, file: AudioWAV, new_sample_rate: int = 4410) -> AudioWAV:
        """ Reduce the sample rate of an audio file """
        if (new_sample_rate > file.sample_rate):
            raise ValueError("The new sample rate must be less than the original sample rate.")
        
        # Reduce the number of samples in the audio file to keep the same duration
        new_n_samples = int(file.n_samples * new_sample_rate / file.sample_rate)
        new_audio = scipy.signal.resample(file.audio, new_n_samples).astype(np.int16)
        
        file.audio = new_audio
        file.sample_rate = new_sample_rate
        file.n_samples = new_n_samples
        return file

    def convert_to_mono(self, audio_wav: AudioWAV) -> AudioWAV:
        if (audio_wav.n_channels == 1):
            return audio_wav
        if (audio_wav.n_channels != 2):
            raise ValueError("Audio has more than 2 channels")
        
        audio_wav.audio = audio_wav.audio.mean(axis=1).astype(np.int16)
        audio_wav.n_channels = 1
        return audio_wav
    
    def NCC(self, x: np.ndarray, y: np.ndarray) -> float:
        """ Normalised cross-correlation """
        if x.shape != y.shape:
            raise ValueError("The two signals must have the same length")
        if np.std(x) == 0 or np.std(y) == 0:
            return np.nan
        
        x_normalized = (x - np.mean(x)) / np.std(x)
        y_normalized = (y - np.mean(y)) / np.std(y)
        
        cross_correlation = np.sum(scipy.signal.correlate(y_normalized, x_normalized, mode='valid'), axis=0)
        cross_correlation /= np.sqrt(np.sum(x_normalized**2) * np.sum(y_normalized**2))
        
        return cross_correlation
