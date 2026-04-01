// Subsystem classes
class Amplifier {
    public void on()                    { System.out.println("Amplifier on"); }
    public void setVolume(int level)    { System.out.println("Amplifier volume set to " + level); }
    public void off()                   { System.out.println("Amplifier off"); }
}


class DVDPlayer {
    public void on()                    { System.out.println("DVD Player on"); }
    public void play(String movie)      { System.out.println("DVD Player playing '" + movie + "'"); }
    public void stop()                  { System.out.println("DVD Player stopped"); }
    public void off()                   { System.out.println("DVD Player off"); }
}


class Projector {
    public void on()                    { System.out.println("Projector on"); }
    public void wideScreenMode()        { System.out.println("Projector in widescreen mode"); }
    public void off()                   { System.out.println("Projector off"); }
}


class Lights {
    public void dim(int level)          { System.out.println("Lights dimmed to " + level + "%"); }
    public void on()                    { System.out.println("Lights on"); }
}


// Facade
public class HomeTheaterFacade {
    private final Amplifier  amp       = new Amplifier();
    private final DVDPlayer  dvd       = new DVDPlayer();
    private final Projector  projector = new Projector();
    private final Lights     lights    = new Lights();

    public void watchMovie(String movie) {
        System.out.println("-- Getting ready to watch a movie --");
        lights.dim(10);
        projector.on();
        projector.wideScreenMode();
        amp.on();
        amp.setVolume(8);
        dvd.on();
        dvd.play(movie);
    }

    public void endMovie() {
        System.out.println("\n-- Shutting down home theater --");
        dvd.stop();
        dvd.off();
        amp.off();
        projector.off();
        lights.on();
    }

    public static void main(String[] args) {
        HomeTheaterFacade theater = new HomeTheaterFacade();
        theater.watchMovie("Inception");
        theater.endMovie();
    }
}