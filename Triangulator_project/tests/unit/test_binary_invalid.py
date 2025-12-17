import pytest
import struct
from triangulator.binary import (
    pointset_to_bytes,
    bytes_to_pointset,
    triangles_to_bytes,
    bytes_to_triangles
)

def test_pointset_corrupted_header():
    data = b"\x00\x00\x00\x10"  # annonce 16 points mais pas de contenu
    with pytest.raises(Exception):
        bytes_to_pointset(data)

def test_pointset_too_short():
    data = struct.pack(">I", 2) + b"\x00" * 4   # manque 12 bytes
    with pytest.raises(Exception):
        bytes_to_pointset(data)

#def test_triangles_corrupted():
    #pts = [(0,0), (1,1)]
    #tris = [(0,1,1)]
    #data = triangles_to_bytes(pts, tris)
    #data = data[:-5]   # tronqué
    #with pytest.raises(Exception):
        #bytes_to_triangles(data)

def test_negative_header():
    with pytest.raises(Exception):
        bytes_to_pointset(struct.pack(">I", 999999999))
