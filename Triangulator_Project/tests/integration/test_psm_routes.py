import json
import urllib.request
import pytest
from triangulator.binary import pointset_to_bytes

PSM = "http://localhost:5051"

def test_psm_post_binary_ok():
    pts = [(0,0),(1,1)]
    data = pointset_to_bytes(pts)
    req = urllib.request.Request(f"{PSM}/points", data=data,
                                 method="POST",
                                 headers={"Content-Type":"application/octet-stream"})
    resp = urllib.request.urlopen(req)
    assert resp.status == 201

def test_psm_get_binary_ok():
    pts = [(0,0),(1,1)]
    data = pointset_to_bytes(pts)
    req = urllib.request.Request(f"{PSM}/points", data=data, method="POST",
                                 headers={"Content-Type":"application/octet-stream"})
    r = urllib.request.urlopen(req)
    pid = json.loads(r.read())["id"]
    r2 = urllib.request.urlopen(f"{PSM}/points/{pid}/binary")
    assert r2.status == 200

def test_psm_missing_id():
    with pytest.raises(Exception):
        urllib.request.urlopen(f"{PSM}/points/999999/binary")

def test_psm_json_input():
    body=json.dumps({"points":[[0,0],[1,1]]}).encode()
    req=urllib.request.Request(f"{PSM}/points",data=body,method="POST",
                              headers={"Content-Type":"application/json"})
    resp=urllib.request.urlopen(req)
    assert resp.status==201

def test_psm_invalid_binary():
    req=urllib.request.Request(f"{PSM}/points",data=b"abc",
                              method="POST",
                              headers={"Content-Type":"application/octet-stream"})
    with pytest.raises(Exception):
        urllib.request.urlopen(req)

def test_psm_ping():
    resp = urllib.request.urlopen(f"{PSM}/ping")
    assert resp.status == 200
