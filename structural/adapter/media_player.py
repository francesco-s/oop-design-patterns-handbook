from abc import ABC, abstractmethod


# Target interface (what the client expects)
class MediaPlayer(ABC):
    @abstractmethod
    def play(self, filename: str) -> None:
        pass


# Adaptee (incompatible interface)
class AdvancedMediaPlayer:
    def play_vlc(self, filename: str) -> None:
        print(f"Playing VLC file: '{filename}'")

    def play_mp4(self, filename: str) -> None:
        print(f"Playing MP4 file: '{filename}'")


# Adapter
class MediaAdapter(MediaPlayer):
    def __init__(self):
        self._advanced_player = AdvancedMediaPlayer()

    def play(self, filename: str) -> None:
        if filename.endswith(".vlc"):
            self._advanced_player.play_vlc(filename)
        elif filename.endswith(".mp4"):
            self._advanced_player.play_mp4(filename)
        else:
            print(f"Format not supported: '{filename}'")


# Client
class AudioPlayer(MediaPlayer):
    def __init__(self):
        self._adapter = MediaAdapter()

    def play(self, filename: str) -> None:
        if filename.endswith(".mp3"):
            print(f"Playing MP3 file: '{filename}'")
        else:
            self._adapter.play(filename)


# Example usage
if __name__ == "__main__":
    player = AudioPlayer()

    player.play("song.mp3")
    player.play("movie.mp4")
    player.play("clip.vlc")
    player.play("track.avi")
    