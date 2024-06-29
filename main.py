# main.py

from direct.showbase.ShowBase import ShowBase
from ui import MenuUI
from camera import CameraController
from event_handle import HexagonSelector
from map import Hexagon
from panda3d.core import load_prc_file_data

load_prc_file_data('', 'load-display pandagl')


class HexagonGridApp(ShowBase):
    def __init__(self):
        super().__init__()  # Initialize the ShowBase class
        self.menu = MenuUI(self)  # Create menu instance
        self.camera_controller = CameraController(self)  # Set up camera controls
        self.hexagon_selector = HexagonSelector(self)  # Set up selector

    def create_hexagon_grid(self):
        Hexagon.create_hexagon_grid(self.render)  # Create hexagon grid


def run_hexagon_grid_app():
    app = HexagonGridApp()
    app.run()


if __name__ == "__main__":
    run_hexagon_grid_app()
