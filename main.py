# main file starts
from direct.showbase.ShowBase import ShowBase
from menu import Menu
import display
from panda3d.core import load_prc_file_data

load_prc_file_data('', 'load-display pandagl')


class HexagonGridApp(ShowBase):
    def __init__(self):
        super().__init__()  # Initialize the ShowBase class
        self.menu = Menu(self)  # Create menu instance
        display.setup_camera(self)

    def create_hexagon_grid(self):
        from map import create_hexagon_grid  # Import here to prevent circular import
        create_hexagon_grid(self.render)


def run_hexagon_grid_app():
    app = HexagonGridApp()
    app.run()


if __name__ == "__main__":
    run_hexagon_grid_app()


# main file ends