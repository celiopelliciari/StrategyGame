from direct.task import Task


class CameraController:
    def __init__(self, app):
        self.app = app
        self.move_dir = [False, False, False, False]  # W, A, S, D
        self.setup_camera()
        self.setup_controls()

    def setup_camera(self):
        self.app.disableMouse()  # Disable the default mouse-based camera controls
        self.app.camera.setPos(0, 0, 100)  # Position the camera
        self.app.camera.lookAt(0, 0, 0)  # Make the camera look at the hexagon

    def setup_controls(self):
        def set_move_dir(index, value):
            self.move_dir[index] = value

        def move_camera(task):
            move_step = 1
            if self.move_dir[0]:  # W
                self.app.camera.setZ(self.app.camera, move_step)
            if self.move_dir[2]:  # S
                self.app.camera.setZ(self.app.camera, -move_step)
            if self.move_dir[1]:  # A
                self.app.camera.setX(self.app.camera, -move_step)
            if self.move_dir[3]:  # D
                self.app.camera.setX(self.app.camera, move_step)
            return Task.cont

        def zoom_camera(zoom_direction):
            zoom_step = 5
            self.app.camera.setY(self.app.camera, zoom_step * zoom_direction)

        # Accept keyboard controls
        self.app.accept('w', set_move_dir, [0, True])
        self.app.accept('w-up', set_move_dir, [0, False])
        self.app.accept('s', set_move_dir, [2, True])
        self.app.accept('s-up', set_move_dir, [2, False])
        self.app.accept('a', set_move_dir, [1, True])
        self.app.accept('a-up', set_move_dir, [1, False])
        self.app.accept('d', set_move_dir, [3, True])
        self.app.accept('d-up', set_move_dir, [3, False])
        self.app.accept('wheel_up', zoom_camera, [1])
        self.app.accept('wheel_down', zoom_camera, [-1])

        # Task for continuous camera movement
        self.app.taskMgr.add(move_camera, "MoveCameraTask")
