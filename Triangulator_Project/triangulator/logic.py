"""
Logique du Triangulator :
- Validation des points
- Triangulation (algorithme simple "from scratch")
- Formatage de la réponse JSON
"""

from math import atan2


def validate_points(points):
    """
    Vérifie que la liste de points est bien formée : liste de couples (x, y) numériques.

    :param points: list[tuple|list[float, float]]
    :raises ValueError: si invalide
    """
    if not isinstance(points, list):
        raise ValueError("Les points doivent être une liste.")

    for p in points:
        if not (isinstance(p, (list, tuple)) and len(p) == 2):
            raise ValueError("Chaque point doit être une liste/tuple de 2 coordonnées.")
        x, y = p
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            raise ValueError("Les coordonnées doivent être numériques.")


def _normalize_and_deduplicate(points):
    """Convertit les points en tuples (float, float) et supprime les doublons."""
    seen = set()
    cleaned = []
    for x, y in points:
        p = (float(x), float(y))
        if p not in seen:
            seen.add(p)
            cleaned.append(p)
    return cleaned


def _all_colinear(points, eps=1e-9):
    """Retourne True si tous les points sont colinéaires (dans la limite d'eps)."""
    if len(points) < 3:
        return True
    (x0, y0) = points[0]
    (x1, y1) = points[1]
    for (x, y) in points[2:]:
        # Aire signée du triangle (p0, p1, p)
        area2 = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0)
        if abs(area2) > eps:
            return False
    return True


def triangulate(points):
    """
    Calcule une triangulation très simple d'un ensemble de points 2D.

    L'algorithme utilisé est volontairement basique ("fan" à partir d'un point),
    afin de respecter la contrainte du sujet (implémentation from scratch, sans SciPy/NumPy).

    - Si moins de 3 points utiles => []
    - Si les points sont colinéaires => []
    - Sinon, on renvoie des triangles de la forme (0, i, i+1).

    :param points: liste de tuples [(x, y), ...]
    :return: liste de triangles (chaque triangle = indices des sommets)
    """
    # On part du principe que validate_points a déjà été appelé en amont.
    cleaned = _normalize_and_deduplicate(points)

    if len(cleaned) < 3:
        return []

    if _all_colinear(cleaned):
        return []

    # Triangulation en "éventail" à partir du premier point
    triangles = []
    for i in range(1, len(cleaned) - 1):
        triangles.append((0, i, i + 1))
    return triangles


def format_response(points, triangles):
    """
    Formate la réponse JSON du Triangulator.

    :param points: liste de points [(x, y), ...]
    :param triangles: liste de triangles [(i1, i2, i3), ...]
    :return: dict sérialisable en JSON
    """
    return {
        "points": points,
        "triangles": triangles,
        "triangle_count": len(triangles),
    }
