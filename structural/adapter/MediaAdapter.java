// Target interface (what the client expects)
interface MediaPlayer {
    void play(String filename);
}


// Adaptee (incompatible interface)
class AdvancedMediaPlayer {
    public void playVlc(String filename) {
        System.out.println("Playing VLC file: '" + filename + "'");
    }

    public void playMp4(String filename) {
        System.out.println("Playing MP4 file: '" + filename + "'");
    }
}


// Adapter
public class MediaAdapter implements MediaPlayer {
    private final AdvancedMediaPlayer advancedPlayer = new AdvancedMediaPlayer();

    @Override
    public void play(String filename) {
        if (filename.endsWith(".vlc")) {
            advancedPlayer.playVlc(filename);
        } else if (filename.endsWith(".mp4")) {
            advancedPlayer.playMp4(filename);
        } else {
            System.out.println("Format not supported: '" + filename + "'");
        }
    }

    public static void main(String[] args) {
        AudioPlayer player = new AudioPlayer();

        player.play("song.mp3");
        player.play("movie.mp4");
        player.play("clip.vlc");
        player.play("track.avi");
    }
}


// Client
class AudioPlayer implements MediaPlayer {
    private final MediaAdapter adapter = new MediaAdapter();

    @Override
    public void play(String filename) {
        if (filename.endsWith(".mp3")) {
            System.out.println("Playing MP3 file: '" + filename + "'");
        } else {
            adapter.play(filename);
        }
    }
}