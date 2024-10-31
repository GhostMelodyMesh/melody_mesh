from abc import ABC, abstractmethod


class FeatureExtractorAbstract(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def extract(self):
        pass

# Tekst
# TO DO:
def extract(self, text):
    pass

# Audio
def extract(self, audio):
    pass


