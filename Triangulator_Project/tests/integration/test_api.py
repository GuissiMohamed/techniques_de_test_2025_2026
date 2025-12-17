import time
from multiprocessing import Process

import pytest
import requests

from triangulator.app import app as triangulator_app
from pointset_manager.app import app as psm_app


def start_psm():
    # PointSetManager sur 5051
    psm_app.run(port=5051)


def start_triangulator():
    # Triangulator sur 5050
    triangulator_app.run(port=5050)


@pytest.fixture(scope="session", autouse=True)
def setup_servers():
    """
    Lance les deux microservices Flask dans des process séparés
    pour les tests d'intégration, puis les arrête à la fin.
    """
    p1 = Process(target=start_psm, daemon=True)
    p2 = Process(target=start_triangulator, daemon=True)
    p1.start()
    p2.start()
    # On laisse un peu de temps pour que les serveurs démarrent
    time.sleep(2)
    yield
    p1.terminate()
    p2.terminate()


def test_full_workflow():
    """
    Cas nominal : on crée un PointSet via le PointSetManager,
    puis on le triangule via le Triangulator en passant par point_set_id.
    """
    points = {"points": [[0, 0], [1, 0], [0, 1], [1, 1]]}
    r1 = requests.post("http://localhost:5051/points", json=points)
    assert r1.status_code == 201
    point_set_id = r1.json()["id"]

    r2 = requests.post(
        "http://localhost:5050/triangulate",
        json={"point_set_id": point_set_id},
    )
    assert r2.status_code == 200
    result = r2.json()
    assert "triangles" in result
    assert result["triangle_count"] > 0


def test_triangulate_direct_points():
    """
    Nouveau mode : le client envoie directement les points au Triangulator
    (le PSM est utilisé en interne, mais pas visible).
    """
    payload = {"points": [[0, 0], [1, 0], [0, 1], [1, 1]]}
    r = requests.post("http://localhost:5050/triangulate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "triangles" in data
    assert data["triangle_count"] > 0


def test_triangulate_missing_body():
    """
    Appel /triangulate sans body JSON -> doit renvoyer 400.
    """
    r = requests.post("http://localhost:5050/triangulate")
    assert r.status_code == 400
    data = r.json()
    assert "error" in data


def test_triangulate_unknown_pointset():
    """
    Demander une triangulation avec un point_set_id inconnu -> 502
    (car le PSM renvoie 404 et le Triangulator propage une erreur gateway).
    """
    r = requests.post(
        "http://localhost:5050/triangulate",
        json={"point_set_id": 999999},
    )
    # Notre implémentation actuelle renvoie 502 dans ce cas
    assert r.status_code == 502
    data = r.json()
    assert "error" in data
