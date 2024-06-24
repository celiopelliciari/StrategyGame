# map.py

from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom, GeomTriangles, GeomNode, TexturePool
import math
import json
import os


class Hexagon:
    def __init__(self, hex_id):
        self.hex_id = hex_id
        self.name = None
        self.is_land = None
        self.terrain = None
        self.population = None
        self.infrastructure = None

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

    def save_to_json(self, file_path):
        with open(file_path, 'a') as f:
            json.dump(self.to_dict(), f)
            f.write('\n')

    def set_is_land(self, row, col):
        if 16 <= row <= 40 and 64 <= col <= 160:
            self.is_land = True
        else:
            self.is_land = False


def create_hexagon_grid(parent_node, rows=40, cols=100, size=1.0):
    vertex_format = GeomVertexFormat.getV3t2()

    water_texture = TexturePool.load_texture("water_texture.jpg")
    terrain_texture = TexturePool.load_texture("terrain_texture.jpg")

    if os.path.exists('hexagon_data.json'):
        os.remove('hexagon_data.json')

    province_data = {}

    for row in range(rows):
        for col in range(cols):
            hex_id = f'{row}_{col}'
            hexagon = Hexagon(hex_id)
            hexagon.set_is_land(row, col)
            hexagon.set_attributes(hexagon.is_land, f'Hexagon {row}_{col}', 'Plains', 100, 'Road')

            vertex_data = GeomVertexData('hexagon', vertex_format, Geom.UHStatic)
            vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
            texcoord_writer = GeomVertexWriter(vertex_data, 'texcoord')

            x_offset = col * 3 / 2 * size
            y_offset = row * math.sqrt(3) * size - (col % 2) * math.sqrt(3) / 2 * size

            angle_offset = 0
            vertices = [
                (size * math.cos(angle_offset + i * math.pi / 3) + x_offset,
                 size * math.sin(angle_offset + i * math.pi / 3) + y_offset,
                 0)
                for i in range(6)
            ]

            texcoords = [
                (0.5 + 0.5 * math.cos(angle_offset + i * math.pi / 3),
                 0.5 + 0.5 * math.sin(angle_offset + i * math.pi / 3))
                for i in range(6)
            ]

            for vertex, texcoord in zip(vertices, texcoords):
                vertex_writer.addData3(*vertex)
                texcoord_writer.addData2(*texcoord)

            triangles = GeomTriangles(Geom.UHStatic)
            for i in range(4):
                triangles.addVertices(0, i + 1, i + 2)
            triangles.addVertices(0, 5, 1)

            geom = Geom(vertex_data)
            geom.addPrimitive(triangles)

            geom_node = GeomNode(hex_id)
            geom_node.addGeom(geom)

            hex_node = parent_node.attachNewNode(geom_node)

            if hexagon.is_land:
                hex_node.setTexture(terrain_texture)
            else:
                hex_node.setTexture(water_texture)

            province_key = f'Province_{row}_{col}'
            if province_key not in province_data:
                province_data[province_key] = []
            hexagon.save_to_json('hexagon_data.json')
            province_data[province_key].append(hexagon.to_dict())

    with open('hexagon_data.json', 'w') as f:
        json.dump(province_data, f, indent=4)
