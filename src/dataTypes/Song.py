class Song:
    def __init__(self):
        lyrics = self.getText()

    def getText(self):
        # get lyrics from db, if empty, extract text and save in db
        ...