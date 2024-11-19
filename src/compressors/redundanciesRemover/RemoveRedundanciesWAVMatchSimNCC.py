import numpy as np
from src.compressors.redundanciesRemover import IRemoveRedundancies
from src.dataTypes.AudioWAV import AudioWAV


class RemoveRedundanciesWAVMatchSimNCC:
    def __init__(self, seg_len_secs: float = 1, init_precision: int = 250, precision_reduction: int = 5, sim_threshold: float = 0.25):
        super().__init__()
        self.seg_len_secs = seg_len_secs
        self.init_precision = init_precision
        self.precision_reduction = precision_reduction
        self.sim_threshold = sim_threshold
    
    def remove_redundancies(self, audio: AudioWAV) -> AudioWAV:
        """ Remove redundancies from the passed audio by looking for segments with high NCC, [AddTest] """
        if audio.n_channels != 1:
            raise ValueError("Audio file must be mono")
        if self.seg_len_secs <= 0:
            raise ValueError("Segment length must be positive")
        if self.init_precision <= 0:
            raise ValueError("Initial precision must be positive")
        if self.precision_reduction <= 0:
            raise ValueError("Precision reduction must be positive")
        if self.sim_threshold < 0 or self.sim_threshold > 1:
            raise ValueError("Similarity threshold must be between 0 and 1")
        
        new_audio = np.ndarray(0, dtype=audio.audio.dtype)
        
        seg_len = int(self.seg_len_secs * audio.sample_rate)
        audio_copy = audio.audio[:, 0].copy()
        
        while len(audio_copy) > 0:
            if len(audio_copy) < seg_len:
                new_audio = np.concatenate((new_audio, audio_copy))
                break
            
            # Select a random segment, we will look for segments similar to this one
            first_sample_start = np.random.randint(0, len(audio_copy) - seg_len)
            first_sample = audio_copy[first_sample_start:first_sample_start + seg_len]
            
            # Add this sample to the new audio
            new_audio = np.concatenate((new_audio, first_sample))
            
            # Remove the segment from the audio and the list of remaining indices
            audio_copy = np.delete(audio_copy, slice(first_sample_start, first_sample_start + seg_len))
            
            # Find similar segments
            while len(audio_copy) >= seg_len:
                precision = self.init_precision
                similarities = []
                offset = 0
                while offset < len(audio_copy) - seg_len:
                    segment = audio_copy[offset:offset + seg_len]
                    similarity = self._NCC(segment, first_sample)
                    similarities.append(similarity)
                    offset += precision
                best_match_index = np.argmax(similarities)
                offset = best_match_index * precision
                
                # Decrease the precision and find the best match in the neighborhood
                best_similarity = 1
                while precision > 1:
                    left = max(0, offset - precision)
                    right = min(len(audio_copy) - seg_len, offset + precision)
                    if (self.precision_reduction > precision):
                        precision = 1
                    else:
                        precision //= self.precision_reduction
                    similarities = []
                    offset = left
                    while offset < right:
                        segment = audio_copy[offset:offset + seg_len]
                        similarity = self._NCC(segment, first_sample)
                        similarities.append(similarity)
                        offset += precision
                    best_match_index = np.argmax(similarities)
                    best_similarity = similarities[best_match_index]
                    offset = left + best_match_index * precision
                
                # If the best match is not similar enough, stop
                if best_similarity < self.sim_threshold:
                    break
                
                # Remove the segment from the audio and the list of remaining indices
                audio_copy = np.delete(audio_copy, slice(offset, offset + seg_len))
        
        # Prepare the new audio for saving
        audio.audio = new_audio.reshape(-1, 1)
        audio.n_samples = len(new_audio)
        
        return audio
    
    def _NCC(self, segX: np.ndarray, segY: np.ndarray) -> float:
        """ Calculate the normalized cross-correlation between two segments """
        segX = segX - np.mean(segX)
        segY = segY - np.mean(segY)
        return np.sum(segX * segY) / (np.linalg.norm(segX) * np.linalg.norm(segY))