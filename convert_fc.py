# File: stl_to_step_converter/convert_fc.py

import sys
import Part
import Mesh

stl_path = sys.argv[1]
step_path = sys.argv[2]

mesh = Mesh.Mesh(stl_path)
shape = Part.Shape()
shape.makeShapeFromMesh(mesh.Topology, 0.05)
solid = Part.makeSolid(shape)
Part.export([solid], step_path)
