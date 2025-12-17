"""
Microservice PointSetManager
----------------------------
Enregistre et renvoie des ensembles de points 2D.
Stockage en mémoire (simple pour le TP).

Il supporte :
- JSON (pour la démo / compatibilité)
- Binaire (pour respecter le sujet sur PointSet)
"""

import os

from flask import Flask, request, jsonify, Response

# On importe les fonctions de conversion binaire du package triangulator
try:
    from triangulator.binary import pointset_to_bytes, bytes_to_pointset
except ImportError:
    # Fallback si le package n'est pas installé en mode package
    from ..triangulator.binary import pointset_to_bytes, bytes_to_pointset  # type: ignore[no-redef]

app = Flask(__name__)

# Stockage en mémoire : {id: {"points": [...]}}
point_sets = {}
next_id = 1


@app.route("/", methods=["GET"])
def root():
    return jsonify({"service": "PointSetManager", "status": "ok"}), 200


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "PointSetManager opérationnel ✅"}), 200


@app.route("/points", methods=["POST"])
def create_pointset():
    """
    Crée un PointSet.

    Deux modes :
    - JSON : body = {"points": [[x, y], ...]}
    - Binaire : body = PointSet (format binaire défini dans le sujet)

    Dans tous les cas, la réponse est en JSON : {"id": <int>}.
    """
    global next_id

    # 1) Si JSON fourni, on garde la compatibilité
    if request.is_json:
        data = request.get_json(silent=True) or {}
        if "points" not in data:
            return jsonify({"error": "Corps JSON invalide (clé 'points' requise)"}), 400
        points = data["points"]
    else:
        # 2) Sinon, on considère que le corps est binaire (PointSet)
        raw = request.get_data()
        if not raw:
            return jsonify({"error": "Corps vide : JSON ou binaire attendu"}), 400
        try:
            points = bytes_to_pointset(raw)
        except Exception:
            return jsonify({"error": "Format binaire PointSet invalide"}), 400

    point_sets[next_id] = {"points": points}
    result = {"id": next_id}
    next_id += 1
    return jsonify(result), 201


@app.route("/points/<int:point_set_id>", methods=["GET"])
def get_pointset_json(point_set_id):
    """
    Récupère un PointSet au format JSON (compatibilité).
    """
    if point_set_id not in point_sets:
        return jsonify({"error": "PointSetID inconnu"}), 404
    return jsonify(point_sets[point_set_id]), 200


@app.route("/points/<int:point_set_id>/binary", methods=["GET"])
def get_pointset_binary(point_set_id):
    """
    Récupère un PointSet au format binaire (PointSet).

    C'est cette route que le Triangulator utilisera pour respecter le sujet.
    """
    if point_set_id not in point_sets:
        return jsonify({"error": "PointSetID inconnu"}), 404

    points = point_sets[point_set_id]["points"]
    data = pointset_to_bytes(points)
    return Response(data, mimetype="application/octet-stream", status=200)


@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return resp


if __name__ == "__main__":
    # Par défaut 5051 (pour éviter les conflits avec macOS/AirPlay)
    port = int(os.getenv("PSM_PORT", "5051"))
    app.run(port=port)
