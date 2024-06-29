# event_handling.py

from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionRay, CollisionNode, BitMask32

class HexagonSelector:
    def __init__(self, app):
        print("Initializing HexagonSelector")
        self.app = app
        self.selected_hex = None
        self.setup_collision_detection()

    def setup_collision_detection(self):
        print("Setting up collision detection")
        self.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerQueue()

        self.picker_ray = CollisionRay()
        self.picker_node = CollisionNode('mouseRay')
        self.picker_node.addSolid(self.picker_ray)
        self.picker_node.setFromCollideMask(BitMask32.bit(1))
        self.picker_node.setIntoCollideMask(BitMask32.allOff())
        self.picker_node_path = self.app.camera.attachNewNode(self.picker_node)
        self.cTrav.addCollider(self.picker_node_path, self.cHandler)

        self.app.accept('mouse1', self.select_hexagon)
        print("Collision detection setup complete")

    def select_hexagon(self):
        print("Mouse click detected")
        if self.app.mouseWatcherNode.hasMouse():
            mpos = self.app.mouseWatcherNode.getMouse()
            print(f"Mouse position: {mpos}")
            self.picker_ray.setFromLens(self.app.camNode, mpos.getX(), mpos.getY())

            self.cTrav.traverse(self.app.render)

            if self.cHandler.getNumEntries() > 0:
                print('Collision detected')
                self.cHandler.sortEntries()
                picked_obj = self.cHandler.getEntry(0).getIntoNodePath()
                print(f"Picked object: {picked_obj}")
                if picked_obj.hasNetTag('hex_id'):
                    hex_id = picked_obj.getNetTag('hex_id')
                    self.highlight_hexagon(picked_obj, hex_id)

    def highlight_hexagon(self, picked_obj, hex_id):
        print(f"Highlighting hexagon: {hex_id}")
        if self.selected_hex:
            print("Clearing previous selection highlight")
            self.selected_hex.clearColor()
        self.selected_hex = picked_obj
        picked_obj.setColor(1, 0, 0, 1)  # Highlight the selected hexagon with red color
        print(f"Selected Hexagon: {hex_id}")

