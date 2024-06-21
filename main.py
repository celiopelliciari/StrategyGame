from direct.showbase.ShowBase import ShowBase
from map import create_hexagon_grid
import display
from panda3d.core import load_prc_file_data

load_prc_file_data('', 'load-display pandagl')


class SingleHexagonApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.create_hexagon_grid()
        display.setup_camera(self)

    def create_hexagon_grid(self):
        create_hexagon_grid(self.render)


def main():
    app = SingleHexagonApp()
    app.run()


if __name__ == "__main__":
    main()
