import json
import urllib.request
import pytest
from triangulator.binary import pointset_to_bytes, bytes_to_triangles

TRI = "http://localhost:5050"
PSM = "http://localhost:5051"

def create_pointset_binary(pts):
    data = pointset_to_bytes(pts)
    req = urllib.request.Request(f"{PSM}/points", data=data, method="POST",
                                 headers={"Content-Type":"application/octet-stream"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())["id"]

def test_tri_json_mode():
    body=json.dumps({"points":[[0,0],[1,0],[0,1]]}).encode()
    req=urllib.request.Request(f"{TRI}/triangulate", data=body,
                               method="POST",
                               headers={"Content-Type":"application/json"})
    resp=urllib.request.urlopen(req)
    assert resp.status==200
    data=json.loads(resp.read())
    assert data["triangle_count"]==1

def test_tri_binary_mode_pointset_id():
    pid=create_pointset_binary([(0,0),(1,0),(0,1)])
    body=json.dumps({"point_set_id":pid}).encode()
    req=urllib.request.Request(f"{TRI}/triangulate", data=body,
            method="POST",
            headers={"Content-Type":"application/json",
                     "Accept":"application/octet-stream"})
    resp=urllib.request.urlopen(req)
    pts, tris = bytes_to_triangles(resp.read())
    assert len(tris)==1

def test_tri_invalid_json():
    req=urllib.request.Request(f"{TRI}/triangulate",
                               data=b"{badjson",
                               method="POST",
                               headers={"Content-Type":"application/json"})
    with pytest.raises(Exception):
        urllib.request.urlopen(req)

def test_tri_missing_param():
    body=json.dumps({}).encode()
    req=urllib.request.Request(f"{TRI}/triangulate", data=body,
                               method="POST",
                               headers={"Content-Type":"application/json"})
    with pytest.raises(Exception):
        urllib.request.urlopen(req)

def test_tri_ping():
    resp = urllib.request.urlopen(f"{TRI}/ping")
    assert resp.status == 200

def test_tri_psm_unavailable(monkeypatch):
    def fake_urlopen(*a, **k):
        raise Exception("PSM DOWN")
    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    body=json.dumps({"point_set_id":1}).encode()
    req=urllib.request.Request(f"{TRI}/triangulate", data=body,
                               method="POST",
                               headers={"Content-Type":"application/json"})
    with pytest.raises(Exception):
        urllib.request.urlopen(req)
