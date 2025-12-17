import json
import urllib.request
from triangulator.binary import pointset_to_bytes, bytes_to_triangles

PSM = "http://localhost:5051"
TRI = "http://localhost:5050"

def test_full_chain():
    pts=[(0,0),(1,0),(0,1)]
    data=pointset_to_bytes(pts)
    req=urllib.request.Request(f"{PSM}/points",data=data,method="POST",
                               headers={"Content-Type":"application/octet-stream"})
    resp=urllib.request.urlopen(req)
    pid=json.loads(resp.read())["id"]

    body=json.dumps({"point_set_id":pid}).encode()
    req2=urllib.request.Request(f"{TRI}/triangulate",data=body,method="POST",
                                headers={"Content-Type":"application/json",
                                         "Accept":"application/octet-stream"})
    resp2=urllib.request.urlopen(req2)
    pts2,tris2=bytes_to_triangles(resp2.read())
    assert len(tris2)==1

def test_multiple_calls():
    for _ in range(10):
        test_full_chain()

def test_large_dataset():
    pts=[(i*0.1,i*0.2) for i in range(200)]
    data=pointset_to_bytes(pts)
    req=urllib.request.Request(f"{PSM}/points",data=data,method="POST",
                               headers={"Content-Type":"application/octet-stream"})
    resp=urllib.request.urlopen(req)
    pid=json.loads(resp.read())["id"]

    body=json.dumps({"point_set_id":pid}).encode()
    req2=urllib.request.Request(f"{TRI}/triangulate",data=body,method="POST",
                                headers={"Content-Type":"application/json",
                                         "Accept":"application/octet-stream"})
    resp2=urllib.request.urlopen(req2)
    pts2,tris2=bytes_to_triangles(resp2.read())
    assert len(pts2)==200
