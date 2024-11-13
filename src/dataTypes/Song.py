class Song:
    def __init__(self):
        lyrics = self.get_text()

    def get_text(self):
        # get lyrics from db, if empty, extract text and save in db
        ...