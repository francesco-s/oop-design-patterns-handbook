# Subsystem classes
class Amplifier:
    def on(self) -> None:
        print("Amplifier on")

    def set_volume(self, level: int) -> None:
        print(f"Amplifier volume set to {level}")

    def off(self) -> None:
        print("Amplifier off")


class DVDPlayer:
    def on(self) -> None:
        print("DVD Player on")

    def play(self, movie: str) -> None:
        print(f"DVD Player playing '{movie}'")

    def stop(self) -> None:
        print("DVD Player stopped")

    def off(self) -> None:
        print("DVD Player off")


class Projector:
    def on(self) -> None:
        print("Projector on")

    def wide_screen_mode(self) -> None:
        print("Projector in widescreen mode")

    def off(self) -> None:
        print("Projector off")


class Lights:
    def dim(self, level: int) -> None:
        print(f"Lights dimmed to {level}%")

    def on(self) -> None:
        print("Lights on")


# Facade
class HomeTheaterFacade:
    def __init__(self):
        self._amp       = Amplifier()
        self._dvd       = DVDPlayer()
        self._projector = Projector()
        self._lights    = Lights()

    def watch_movie(self, movie: str) -> None:
        print("-- Getting ready to watch a movie --")
        self._lights.dim(10)
        self._projector.on()
        self._projector.wide_screen_mode()
        self._amp.on()
        self._amp.set_volume(8)
        self._dvd.on()
        self._dvd.play(movie)

    def end_movie(self) -> None:
        print("\n-- Shutting down home theater --")
        self._dvd.stop()
        self._dvd.off()
        self._amp.off()
        self._projector.off()
        self._lights.on()


# Example usage
if __name__ == "__main__":
    theater = HomeTheaterFacade()
    theater.watch_movie("Inception")
    theater.end_movie()
    