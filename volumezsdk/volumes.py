import requests
import json
from .settings import api_url, headers, volumes_url

volhelp = """
{

    "name": "vol1",
    "type": "file",
    "contentvolume": "string",
    "contentsnapshot": "string",
    "size": 10,
    "policy": "string",
    "consistencygroup": "string",
    "node": "string",
    "zone": "string",
    "zonereplica": "string",
    "controller": "string",
    "volumegroupname": "vg_1",
    "replicationnode": "string",
    "replicationcontroller": "string",
    "replicationvolumegroupname": "vg_1"

}
"""
class Volume:
    def help(self):
        print(f"Create a dictionary with the following values and pass to Volume.new() to instantiate a new Volume instance")
        print(f"{volhelp}")

    def new(self, vols_dict):
        if type(vols_dict) is dict:
            self.__dict__ = vols_dict
        else:
            print(f"The volume object takes an argument of a dictionary defining the volume details")
            return
        return
    
    def get_volume(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.get(api_url+volumes_url+"/"+self.volumeid, headers=heads)
        if req.status_code != 200:
            print(f"Failed to get volume properties for {self.volumeid}. {req.reason}")
            return
        self.__dict__ = json.loads(req.text)
        print("Volume state updated")
        return

    def create_volume(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.post(api_url+volumes_url, headers=heads, data=json.dumps(self.__dict__))
        if req.status_code != 200:
            print(f"Failed to create volume. {req.reason}")
            return
        print(f"Created volume {self.volumename}")

    def delete_volume(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.delete(api_url+volumes_url+"/"+self.volumeid, headers=heads)
        if req.status_code != 200:
            print(f"Failed to delete volume {self.volumeid}. {req.reason}")
            return
        print(f"Deleted volume {self.volumeid}")
        return

    def __str__(self):
        return f"Volumez Volume {self.voluemid}"


class Volumes:
    def __init__(self, token):
        self.token = token
        self.headers = headers
        self.headers["authorization"] = self.token.id_token

    def get_volumes(self):
        req = requests.get(api_url+volumes_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Error getting a list of volumes. {req.reason}")
            return
        res = json.loads(req.text)
        self.volumes = []
        for r in res:
            v = Volume()
            v.new(r)
            self.volumes.append(v)
        return