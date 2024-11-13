import numpy as np
import scipy.signal
from src.compressors.CompressorAbstract import CompressorAbstract
from src.dataTypes.AudioWAV import AudioWAV
from src.fileHandlers.AudioFileHandler import AudioFileHandler


class CompressorWAVBaseline(CompressorAbstract):
    """ Warning: This compressor is not efficient and is only used as an example, it could be improved in many ways (including optimization) """
    def compress(self, file_path: str) -> str:
        file_handler = AudioFileHandler()
        audio_wav = file_handler.read_as_wav(file_path)
        audio_wav = self.convert_to_mono(audio_wav)
        audio_wav = self.lower_quality(audio_wav, 4410)
        audio_wav = self.remove_redundancies(audio_wav)
        
        # Save the compressed file
        output_path = file_path.replace("rawAudio", "compressedAudio").split(".")[0] + "_compressed." + audio_wav.format
        file_handler.write(audio_wav, output_path)
        return output_path
    
    def remove_redundancies(self, file: AudioWAV, seg_len_secs: float = 1, init_precision: int = 250, precision_reduction: int = 5, sim_threshold: float = 0.25) -> AudioWAV:
        if file.n_channels != 1:
            raise ValueError("Audio file must be mono")
        if seg_len_secs <= 0:
            raise ValueError("Segment length must be positive")
        if init_precision <= 0:
            raise ValueError("Initial precision must be positive")
        if precision_reduction <= 0:
            raise ValueError("Precision reduction must be positive")
        
        groups = self.group_redundancies(file, seg_len_secs, init_precision, precision_reduction, sim_threshold)
        groups = [group for group in groups if len(group) > 1]
        selected_segments = []
        for group in groups:
            selected_segments.append(self.select_from_redundancy_group(file, group))
        
        # Create a new audio file with the selected segments
        new_n_samples = sum([len(indices) for indices in selected_segments])
        print(new_n_samples)
        new_audio = np.zeros(new_n_samples, dtype=np.float32)
        offset = 0
        for indices in selected_segments:
            new_audio[offset:offset + len(indices)] = file.audio[indices]
            offset += len(indices)
        
        file.audio = new_audio
        file.n_samples = new_n_samples
        return file

    def select_from_redundancy_group(self, file: AudioWAV, group: list[list[int]]) -> list[int]:
        # Select a segment with the highest energy
        energies = [np.sum(file.audio[indices] ** 2) for indices in group]
        
        selected_index = np.argmax(energies)
        return group[selected_index]

    def group_redundancies(self, file: AudioWAV, seg_len_secs: float = 1, init_precision: int = 250, precision_reduction: int = 5, sim_threshold: float = 0.25) -> list[list[list[int]]]:
        """ Returns a list of groups of segments that are similar to each other, each segment is represented by a list of indices """
        groups: list[list[list[int]]] = []
        seg_len = int(seg_len_secs * file.sample_rate)
        audio_copy = file.audio.copy()
        remaining_indices = [i for i in range(len(audio_copy))]
        while len(audio_copy) > 0:
            # If there are not enough samples left to form a segment, add the remaining indices to a new group
            if len(audio_copy) <= seg_len:
                groups.append([remaining_indices])
                break
                
            group: list[list[int]] = []
            # Select a random segment, we will look for segments similar to this one
            first_sample_start = np.random.randint(0, len(audio_copy) - seg_len)
            group.append(remaining_indices[first_sample_start:first_sample_start + seg_len])
            first_sample = audio_copy[first_sample_start:first_sample_start + seg_len]
            
            # Remove the segment from the audio and the list of remaining indices
            audio_copy = np.delete(audio_copy, slice(first_sample_start, first_sample_start + seg_len))
            remaining_indices = remaining_indices[:first_sample_start] + remaining_indices[first_sample_start + seg_len:]
            
            # Find similar segments
            while len(audio_copy) >= seg_len:
                precision = init_precision
                similarities = []
                offset = 0
                while offset < len(audio_copy) - seg_len:
                    segment = audio_copy[offset:offset + seg_len]
                    similarity = self.ncc(segment, first_sample)
                    similarities.append(similarity)
                    offset += precision
                best_match_index = np.argmax(similarities)
                offset = best_match_index * precision
                
                # Decrease the precision and find the best match in the neighborhood
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
                        similarity = self.ncc(segment, first_sample)
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
        new_audio = scipy.signal.resample(file.audio, new_n_samples)
        
        file.audio = new_audio
        file.sample_rate = new_sample_rate
        file.n_samples = new_n_samples
        return file

    def convert_to_mono(self, audio_wav: AudioWAV) -> AudioWAV:
        if (audio_wav.n_channels == 1):
            return audio_wav
        if (audio_wav.n_channels != 2):
            raise ValueError("Audio has more than 2 channels")
        
        audio_wav.audio = audio_wav.audio.mean(axis=1)
        audio_wav.n_channels = 1
        return audio_wav
    
    def ncc(self, x: np.ndarray, y: np.ndarray) -> float:
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
