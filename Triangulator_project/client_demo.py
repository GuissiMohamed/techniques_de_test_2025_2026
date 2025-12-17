import requests

PSM = "http://localhost:5051"
TRI = "http://localhost:5050"

def main():
    # 1) créer un point set
    points = {"points": [[0,0],[1,0],[0,1],[1,1]]}
    r = requests.post(f"{PSM}/points", json=points)
    r.raise_for_status()
    pid = r.json()["id"]
    print(f"PointSetID créé: {pid}")

    # 2) demander la triangulation
    r = requests.post(f"{TRI}/triangulate", json={"point_set_id": pid})
    r.raise_for_status()
    data = r.json()
    print("\n== Résultat ==")
    print("Points:", data["points"])
    print("Triangles (indices):", data["triangles"])
    print("Nombre de triangles:", data["triangle_count"])

if __name__ == "__main__":
    main()
