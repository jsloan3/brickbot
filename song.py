from yt_dlp import YoutubeDL
from config import YDL_OPTS

class Song:
    def __init__(self, term):
        self.term = term
        self.source = None # youtube source url
        self.title = None # song title
        self.url = None # youtube url
        self.process_term()
    
    def process_term(self):
        with YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(f"ytsearch:{self.term}",
                download=False)['entries'][0]
            self.source = info['url']
            self.title = info['title']
            self.url = info['original_url']

    def get_url(self):
        return self.url
    
    def get_source(self):
        return self.source
    
    def get_title(self):
        return self.title
    
    def get_term(self):
        return self.term