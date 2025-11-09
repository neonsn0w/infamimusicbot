class Song:
    def __init__(self, audio_url: str, title: str, url: str):
        self.audio_url = audio_url
        self.title = title
        self.url = url
    def __str__(self):
        return f"{self.title} ({self.url})"
