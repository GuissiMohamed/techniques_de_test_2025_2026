import multiprocessing
import time
import json
import urllib.request
import pytest

from triangulator.binary import (
    pointset_to_bytes,
    bytes_to_pointset,
    triangles_to_bytes,
    bytes_to_triangles,
)

PSM_URL = "http://localhost:5051"
TRI_URL = "http://localhost:5050"


def start_psm():
    import pointset_manager.app as p
    p.app.run(port=5051)


def start_triangulator():
    import triangulator.app as t
    t.app.run(port=5050)


@pytest.fixture(scope="module", autouse=True)
def setup_services():
    """
    Démarre les deux microservices dans des processus séparés
    puis les stoppe à la fin.
    """
    psm_proc = multiprocessing.Process(target=start_psm)
    tri_proc = multiprocessing.Process(target=start_triangulator)

    psm_proc.start()
    tri_proc.start()
    time.sleep(1.5)  # temps de démarrage

    yield

    psm_proc.terminate()
    tri_proc.terminate()


def test_binary_pointset_roundtrip():
    """
    Test : envoie un PointSet en BINAIRE au PSM, puis le relit en BINAIRE.
    """
    points = [(0, 0), (1, 0), (0, 1)]
    data = pointset_to_bytes(points)

    # --- POST binaire vers /points ---
    req = urllib.request.Request(
        f"{PSM_URL}/points",
        data=data,
        method="POST",
        headers={"Content-Type": "application/octet-stream"},
    )

    with urllib.request.urlopen(req) as resp:
        assert resp.status == 201
        payload = json.loads(resp.read())
        point_set_id = payload["id"]

    # --- GET binaire vers /points/<id>/binary ---
    with urllib.request.urlopen(f"{PSM_URL}/points/{point_set_id}/binary") as resp:
        assert resp.status == 200
        returned = bytes_to_pointset(resp.read())

    assert returned == pytest.approx(points)


def test_triangulator_binary_response():
    """
    Test : envoie un PointSet en binaire, triangule en binaire,
    vérifie que la sortie est correcte.
    """
    points = [(0, 0), (1, 0), (0, 1)]
    data = pointset_to_bytes(points)

    # --- Création du pointset ---
    req = urllib.request.Request(
        f"{PSM_URL}/points",
        data=data,
        method="POST",
        headers={"Content-Type": "application/octet-stream"},
    )
    with urllib.request.urlopen(req) as resp:
        payload = json.loads(resp.read())
        point_set_id = payload["id"]

    # --- Triangulation en binaire ---
    body = json.dumps({"point_set_id": point_set_id}).encode()
    req2 = urllib.request.Request(
        f"{TRI_URL}/triangulate",
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/octet-stream",
        },
    )

    with urllib.request.urlopen(req2) as resp:
        assert resp.status == 200
        points2, triangles2 = bytes_to_triangles(resp.read())

    # --- Vérifications ---
    assert points2 == pytest.approx(points)
    assert triangles2 == [(0, 1, 2)]
