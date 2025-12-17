"""
Microservice Triangulator
-------------------------
- Reçoit soit un point_set_id, soit directement des points.
- Si des points sont fournis, il appelle le PointSetManager en interne
  pour enregistrer le PointSet (en binaire), puis calcule la triangulation.
- Peut répondre en JSON (par défaut) ou en binaire (Triangles) selon l'en-tête Accept.
"""

import json
import os
from urllib import request as http_request
from urllib import error as http_error

from flask import Flask, request, jsonify, make_response, Response

app = Flask(__name__)

# Import robuste des fonctions de logique et binaire
try:
    from .logic import triangulate, validate_points, format_response
    from .binary import pointset_to_bytes, bytes_to_pointset, triangles_to_bytes
except ImportError:
    from logic import triangulate, validate_points, format_response  # type: ignore[no-redef]
    from binary import pointset_to_bytes, bytes_to_pointset, triangles_to_bytes  # type: ignore[no-redef]

POINTSET_MANAGER_URL = os.getenv("POINTSET_MANAGER_URL", "http://localhost:5051")


@app.route("/", methods=["GET"])
def root():
    return jsonify({"service": "Triangulator", "status": "ok"}), 200


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Triangulator opérationnel ✅"}), 200


def _psm_post_points_binary(points):
    """
    Envoie un PointSet au PSM au format binaire.

    :param points: liste de points [(x, y), ...]
    :return: id du PointSet (int)
    :raises RuntimeError: si HTTP non 201 ou format réponse invalide
    """
    data = pointset_to_bytes(points)
    req = http_request.Request(
        f"{POINTSET_MANAGER_URL}/points",
        data=data,
        method="POST",
        headers={"Content-Type": "application/octet-stream"},
    )
    try:
        with http_request.urlopen(req, timeout=5) as resp:
            if resp.status != 201:
                raise RuntimeError(f"PSM refuse la création (HTTP {resp.status})")
            body = resp.read().decode("utf-8")
            payload = json.loads(body)
            return int(payload["id"])
    except (http_error.URLError, json.JSONDecodeError, KeyError, ValueError) as exc:
        raise RuntimeError(f"Erreur lors de la création du PointSet: {exc}") from exc


def _psm_get_points_binary(point_set_id):
    """
    Récupère les points d'un PointSet auprès du PSM au format binaire.

    :param point_set_id: identifiant du PointSet
    :return: liste de points [(x, y), ...]
    :raises RuntimeError: si non 200 ou erreur de format
    """
    url = f"{POINTSET_MANAGER_URL}/points/{point_set_id}/binary"
    req = http_request.Request(url, method="GET")
    try:
        with http_request.urlopen(req, timeout=5) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Impossible de récupérer les points (HTTP {resp.status})")
            data = resp.read()
            return bytes_to_pointset(data)
    except http_error.HTTPError as exc:
        if exc.code == 404:
            raise RuntimeError("PointSetID inconnu") from exc
        raise RuntimeError(f"Impossible de récupérer les points (HTTP {exc.code})") from exc
    except http_error.URLError as exc:
        raise RuntimeError(f"PointSetManager injoignable: {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Erreur de décodage du PointSet: {exc}") from exc


@app.route("/triangulate", methods=["POST", "OPTIONS"])
def triangulate_endpoint():
    """
    Accepte:
      - {"points": [[x,y], ...]}      -> mode utilisé par la démo HTML
      - {"point_set_id": <int>}       -> mode "officiel" avec le PointSetManager

    Réponse :
      - JSON par défaut
      - Binaire (Triangles) si l'en-tête Accept contient "application/octet-stream"
    """

    # Préflight CORS (OPTIONS)
    if request.method == "OPTIONS":
        resp = make_response("", 204)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return resp

    data = request.get_json(silent=True) or {}

    wants_binary = "application/octet-stream" in (request.headers.get("Accept") or "")

    try:
        # --- Cas 1 : points fournis directement ---
        if "points" in data:
            points = data["points"]
            validate_points(points)

            # On enregistre le PointSet en binaire auprès du PSM
            try:
                _psm_post_points_binary(points)
            except RuntimeError as exc:
                return jsonify({"error": str(exc)}), 502

            triangles = triangulate(points)

        # --- Cas 2 : identification par point_set_id ---
        elif "point_set_id" in data:
            point_set_id = data["point_set_id"]
            try:
                points = _psm_get_points_binary(point_set_id)
            except RuntimeError as exc:
                # On renvoie 502 pour distinguer les erreurs côté PSM
                return jsonify({"error": str(exc)}), 502

            validate_points(points)
            triangles = triangulate(points)

        else:
            # Rien de valide fourni
            return jsonify({"error": "Requête invalide: fournir 'points' OU 'point_set_id'"}), 400

        # Réponse selon Accept
        if wants_binary:
            binary = triangles_to_bytes(points, triangles)
            return Response(binary, mimetype="application/octet-stream", status=200)

        return jsonify(format_response(points, triangles)), 200

    except ValueError as exc:
        # Erreurs de validation des données
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:  # pragma: no cover - garde-fou
        return jsonify({"error": f"Erreur interne : {exc}"}), 500


@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return resp


if __name__ == "__main__":
    port = int(os.getenv("TRIANGULATOR_PORT", "5050"))
    app.run(port=port)
