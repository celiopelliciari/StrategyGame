from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter
from panda3d.core import Geom, GeomTriangles, GeomNode
import math
import json
import os


class Hexagon:
    def __init__(self, hex_id):
        self.hex_id = hex_id
        self.name = None  # Placeholder for name attribute
        self.is_land = None  # Placeholder for land attribute
        self.terrain = None  # Placeholder for terrain attribute
        self.population = None  # Placeholder for population attribute
        self.infrastructure = None  # Placeholder for infrastructure attribute

    def set_attributes(self, is_land, name, terrain, population, infrastructure):
        self.is_land = is_land
        self.name = name
        self.terrain = terrain
        self.population = population
        self.infrastructure = infrastructure

    def to_dict(self):
        return {
            'hex_id': self.hex_id,
            'is_land': self.is_land,
            'name': self.name,
            'terrain': self.terrain,
            'population': self.population,
            'infrastructure': self.infrastructure
        }

    def save_to_json(self, province):
        data = {
            'Province': province,
            'hexagons': self.to_dict()
        }
        with open('hexagon_data.json', 'a') as f:
            json.dump(data, f)
            f.write('\n')


def create_hexagon_grid(parent_node, rows=40, cols=100, size=1.0):
    vertex_format = GeomVertexFormat.getV3()

    if os.path.exists('hexagon_data.json'):
        os.remove('hexagon_data.json')

    province_data = {}

    for row in range(rows):
        for col in range(cols):
            hex_id = f'{row}_{col}'
            hexagon = Hexagon(hex_id)  # Create Hexagon instance
            hexagon.set_attributes(None, None, None, None, None)  # Initialize attributes as None

            vertex_data = GeomVertexData('hexagon', vertex_format, Geom.UHStatic)
            vertex_writer = GeomVertexWriter(vertex_data, 'vertex')

            # Calculate the position offset for each hexagon
            x_offset = col * 3 / 2 * size
            y_offset = row * math.sqrt(3) * size - (col % 2) * math.sqrt(3) / 2 * size

            # Define hexagon vertices with flat top
            angle_offset = 0  # No offset needed for flat-top hexagons
            vertices = [
                (size * math.cos(angle_offset + i * math.pi / 3) + x_offset,
                 size * math.sin(angle_offset + i * math.pi / 3) + y_offset,
                 0)
                for i in range(6)
            ]

            # Add the vertices to the writer
            for vertex in vertices:
                vertex_writer.addData3(*vertex)

            # Define the triangles to form the hexagon
            triangles = GeomTriangles(Geom.UHStatic)
            for i in range(4):
                triangles.addVertices(0, i + 1, i + 2)
            triangles.addVertices(0, 5, 1)  # Last triangle to complete the hexagon

            # Create the hexagon geometry
            geom = Geom(vertex_data)
            geom.addPrimitive(triangles)

            # Create a GeomNode to hold the hexagon geometry
            geom_node = GeomNode(hex_id)
            geom_node.addGeom(geom)

            # Attach the hexagon to the render tree
            hex_node = parent_node.attachNewNode(geom_node)
            hex_node.setColor(0, 1, 0, 1)  # Set color to green

            # Save hexagon attributes to JSON file
            province_key = f'Province_{row}_{col}'
            if province_key not in province_data:
                province_data[province_key] = []
            hexagon.save_to_json(province_key)
            province_data[province_key].append(hexagon.to_dict())

    # Save all province data to JSON file
    with open('hexagon_data.json', 'w') as f:
        json.dump(province_data, f, indent=4)
