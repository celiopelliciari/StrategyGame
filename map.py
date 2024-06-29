# map.py

from panda3d.core import (
    GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom, GeomTriangles,
    GeomNode, BitMask32, CollisionNode, CollisionPolygon
)
import math
import json
import os

class Hexagon:
    # Define the vertex format once for all hexagons
    vertex_format = GeomVertexFormat.getV3t2()

    def __init__(self, hex_id, is_land, name, terrain, population, infrastructure):
        # Initialize hexagon attributes
        self.attributes = {
            'hex_id': hex_id,
            'is_land': is_land,
            'name': name,
            'terrain': terrain,
            'population': population,
            'infrastructure': infrastructure
        }
        print(f"Created Hexagon: {self.attributes}")

    def save_to_json(self, file_path):
        # Save hexagon data to JSON file
        with open(file_path, 'a') as f:
            json.dump(self.attributes, f)
            f.write('\n')
        print(f"Saved hexagon {self.attributes['hex_id']} to JSON")

    @staticmethod
    def is_land(row, col):
        # Determine if the hexagon is land based on its position
        return 16 <= row <= 40 and 64 <= col <= 160

    @staticmethod
    def generate_hexagon_vertices(x_offset, y_offset, size):
        # Generate vertices for a hexagon
        angle_offset = 0
        vertices = [
            (size * math.cos(angle_offset + i * math.pi / 3) + x_offset,
             size * math.sin(angle_offset + i * math.pi / 3) + y_offset,
             0)
            for i in range(6)
        ]
        print(f"Generated vertices: {vertices}")
        return vertices

    @staticmethod
    def generate_texcoords(angle_offset=0):
        # Generate texture coordinates for a hexagon
        texcoords = [
            (0.5 + 0.5 * math.cos(angle_offset + i * math.pi / 3),
             0.5 + 0.5 * math.sin(angle_offset + i * math.pi / 3))
            for i in range(6)
        ]
        print(f"Generated texcoords: {texcoords}")
        return texcoords

    @classmethod
    def create_hexagon_geom(cls, vertices, texcoords):
        # Create the geometry for a hexagon
        vertex_data = GeomVertexData('hexagon', cls.vertex_format, Geom.UHStatic)
        vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
        texcoord_writer = GeomVertexWriter(vertex_data, 'texcoord')

        for vertex, texcoord in zip(vertices, texcoords):
            vertex_writer.addData3(*vertex)
            texcoord_writer.addData2(*texcoord)

        triangles = GeomTriangles(Geom.UHStatic)
        for i in range(4):
            triangles.addVertices(0, i + 1, i + 2)
        triangles.addVertices(0, 5, 1)

        geom = Geom(vertex_data)
        geom.addPrimitive(triangles)

        print(f"Created geometry for hexagon")
        return geom

    @staticmethod
    def create_collision_polygon(vertices):
        # Create collision polygons for a hexagon
        collision_node = CollisionNode('collision')
        collision_polygon1 = CollisionPolygon(*vertices[:3])
        collision_polygon2 = CollisionPolygon(*vertices[3:])
        collision_node.addSolid(collision_polygon1)
        collision_node.addSolid(collision_polygon2)

        collision_node.setFromCollideMask(BitMask32.bit(1))
        collision_node.setIntoCollideMask(BitMask32.allOff())

        print(f"Created collision polygon")
        return collision_node

    @classmethod
    def create_hexagon_grid(cls, parent_node, rows=40, cols=100, size=1.0):
        # Create a grid of hexagons
        if os.path.exists('hexagon_data.json'):
            os.remove('hexagon_data.json')

        province_data = {}

        for row in range(rows):
            for col in range(cols):
                hex_id = f'{row}_{col}'
                is_land = cls.is_land(row, col)
                hexagon = Hexagon(hex_id, is_land, f'Hexagon {row}_{col}', 'Plains', 100, 'Road')
                hexagon.save_to_json('hexagon_data.json')

                x_offset = col * 3 / 2 * size
                y_offset = row * math.sqrt(3) * size - (col % 2) * math.sqrt(3) / 2 * size

                vertices = cls.generate_hexagon_vertices(x_offset, y_offset, size)
                texcoords = cls.generate_texcoords()

                geom = cls.create_hexagon_geom(vertices, texcoords)
                geom_node = GeomNode(hex_id)
                geom_node.addGeom(geom)
                hex_node = parent_node.attachNewNode(geom_node)

                # Set color instead of texture
                if is_land:
                    hex_node.setColor(0, 1, 0, 1)  # Green for land
                else:
                    hex_node.setColor(0, 0, 1, 1)  # Blue for water

                # Add collision polygon
                collision_node = cls.create_collision_polygon(vertices)
                collision_node_path = hex_node.attachNewNode(collision_node)
                collision_node_path.setTag('hex_id', hex_id)

                province_key = f'Province_{row}_{col}'
                if province_key not in province_data:
                    province_data[province_key] = []
                province_data[province_key].append(hexagon.attributes)

        with open('hexagon_data.json', 'w') as f:
            json.dump(province_data, f, indent=4)
        print("Created hexagon grid and saved to JSON")
