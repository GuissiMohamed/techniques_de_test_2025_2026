"""
Fonctions utilitaires pour la représentation binaire de PointSet et Triangles.

Format PointSet :
- 4 octets : unsigned long (nombre de points)
- pour chaque point :
    - 4 octets : float32 X
    - 4 octets : float32 Y

Format Triangles :
- d'abord un PointSet (comme ci-dessus)
- puis :
    - 4 octets : unsigned long (nombre de triangles)
    - pour chaque triangle :
        - 3 x 4 octets : unsigned long (indices des sommets)
"""

import struct


def pointset_to_bytes(points):
    """
    Encode une liste de points (x, y) en format binaire PointSet.
    """
    nb_points = len(points)
    # unsigned long (4 octets)
    data = struct.pack(">I", nb_points)
    # chaque point : 2 floats (4 octets chacun)
    for x, y in points:
        data += struct.pack(">ff", float(x), float(y))
    return data


def bytes_to_pointset(data):
    """
    Décode des bytes au format PointSet vers une liste de tuples (x, y).
    """
    offset = 0
    (nb_points,) = struct.unpack_from(">I", data, offset)
    offset += 4

    points = []
    for _ in range(nb_points):
        x, y = struct.unpack_from(">ff", data, offset)
        points.append((x, y))
        offset += 8

    return points


def triangles_to_bytes(points, triangles):
    """
    Encode un ensemble de points + triangles au format binaire Triangles.
    """
    # Partie PointSet
    data = pointset_to_bytes(points)

    # Partie Triangles
    nb_triangles = len(triangles)
    data += struct.pack(">I", nb_triangles)
    for a, b, c in triangles:
        data += struct.pack(">III", int(a), int(b), int(c))

    return data


def bytes_to_triangles(data):
    """
    Décode des bytes au format Triangles vers (points, triangles).
    """
    points = bytes_to_pointset(data)

    # Offset après la partie PointSet
    offset = 4 + len(points) * 8

    (nb_triangles,) = struct.unpack_from(">I", data, offset)
    offset += 4

    triangles = []
    for _ in range(nb_triangles):
        a, b, c = struct.unpack_from(">III", data, offset)
        triangles.append((a, b, c))
        offset += 12

    return points, triangles
