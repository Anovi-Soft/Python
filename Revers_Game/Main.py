from scene import SceneLogo, MainScene
from window import Window


def main():
    window = Window(scene=SceneLogo(1800000, MainScene()))
    window.set_caption(title="Revers 2.0")
    window.loop()


if __name__ == "__main__":
    main()
