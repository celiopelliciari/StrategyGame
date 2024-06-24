# ui.py

from direct.gui.DirectGui import DirectFrame, DirectButton, OnscreenImage
from panda3d.core import TransparencyAttrib

class MenuUI:
    def __init__(self, base):
        self.base = base
        self.setup_menu()

    def setup_menu(self):
        # Create a frame for the menu
        self.menu_frame = DirectFrame(frameSize=(-1, 1, -1, 1),
                                      frameColor=(0, 0, 0, 0.5),
                                      parent=self.base.aspect2d)

        # Add background image
        self.background_image = OnscreenImage(parent=self.menu_frame,
                                              image='assets/menu_background.jpg',  # Path to your background image
                                              scale=(1.33, 1, 1))  # Adjust the scale as needed
        self.background_image.setTransparency(TransparencyAttrib.MAlpha)

        # Create a start button
        self.start_button = DirectButton(text="Start Game",
                                         scale=0.1,
                                         pos=(0, 0, -0.2),
                                         command=self.start_game,
                                         parent=self.menu_frame)

        # Create an exit button
        self.exit_button = DirectButton(text="Exit",
                                        scale=0.1,
                                        pos=(0, 0, -0.4),
                                        command=self.exit_game,
                                        parent=self.menu_frame)

    def start_game(self):
        # Remove the menu frame and start the game
        self.menu_frame.destroy()
        self.base.create_hexagon_grid()  # Assuming create_hexagon_grid is a method in your main app

    def exit_game(self):
        self.base.userExit()  # Close the game