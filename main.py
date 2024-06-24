# main.py or HexagonGridApp

from direct.showbase.ShowBase import ShowBase
from ui import MenuUI
from event_handling import setup_camera_controls
from map import create_hexagon_grid
from panda3d.core import load_prc_file_data

load_prc_file_data('', 'load-display pandagl')

class HexagonGridApp(ShowBase):
    def __init__(self):
        super().__init__()  # Initialize the ShowBase class
        self.menu = MenuUI(self)  # Create menu instance
        setup_camera_controls(self)  # Set up camera controls

    def create_hexagon_grid(self):
        create_hexagon_grid(self.render)  # Create hexagon grid

def run_hexagon_grid_app():
    app = HexagonGridApp()
    app.run()

if __name__ == "__main__":
    run_hexagon_grid_app()
