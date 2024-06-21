# display file starts

from direct.task import Task
from panda3d.core import load_prc_file_data
import tkinter as tk


def get_screen_resolution():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


def setup_camera(app):
    app.disableMouse()  # Disable the default mouse-based camera controls
    app.camera.setPos(0, 0, 100)  # Position the camera
    app.camera.lookAt(0, 0, 0)  # Make the camera look at the hexagon

    # Camera controller setup
    move_dir = [False, False, False, False]  # W, A, S, D

    def set_move_dir(index, value):
        move_dir[index] = value

    def move_camera(task):
        move_step = 1
        if move_dir[0]:  # W
            app.camera.setZ(app.camera, move_step)
        if move_dir[2]:  # S
            app.camera.setZ(app.camera, -move_step)
        if move_dir[1]:  # A
            app.camera.setX(app.camera, -move_step)
        if move_dir[3]:  # D
            app.camera.setX(app.camera, move_step)
        return Task.cont

    def zoom_camera(zoom_direction):
        zoom_step = 5
        app.camera.setY(app.camera, zoom_step * zoom_direction)

    # Accept keyboard controls
    app.accept('w', set_move_dir, [0, True])
    app.accept('w-up', set_move_dir, [0, False])
    app.accept('s', set_move_dir, [2, True])
    app.accept('s-up', set_move_dir, [2, False])
    app.accept('a', set_move_dir, [1, True])
    app.accept('a-up', set_move_dir, [1, False])
    app.accept('d', set_move_dir, [3, True])
    app.accept('d-up', set_move_dir, [3, False])
    app.accept('wheel_up', zoom_camera, [1])
    app.accept('wheel_down', zoom_camera, [-1])

    # Task for continuous camera movement
    app.taskMgr.add(move_camera, "MoveCameraTask")


# Set the window size to match the screen resolution
screen_width, screen_height = get_screen_resolution()
load_prc_file_data('', f'win-size {screen_width} {screen_height}')



# display file ends
