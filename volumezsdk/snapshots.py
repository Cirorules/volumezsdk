import requests
import json
from .settings import snap_url, api_url, headers

class Snapshot:
    def new(self, snaps_dict):
        if type(snaps_dict) is dict:
            self.__dict__ = snaps_dict
        else:
            print(f"The snapshot object takes an argument of a dictionary defining the snapshot details")
    
    def get_snapshot(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.get(api_url+f"/volumes/{self.volumename}/snapshots/{self.name}", headers=heads)
        if req.status_code != 200:
            print(f"Failed to get properties of snapshot {self.snapshotid}. Check ID and try again")
            print(f"Reason: {req.reason}")
            return
        self.__dict__ = json.loads(req.text)
        return

    def create_snapshot(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.post(api_url+f"/volumes/{self.volumename}/snapshots", headers=heads)
        if req.status_code != 200:
            print(f"Failed to create snapshot for volume {self.volumename}. {req.reason}")
            return
        print(f"Created snapshot for volume {self.volumename}")
        return

    def delete_snapshot(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.delete(api_url+f"/volumes/{self.volumename}/snapshots/{self.name}", headers=heads)
        if req.status_code != 200:
            print(f"Failed to delete snapshot {self.snapshotid}. {req.reason}")
            return
        print(f"Deleted snapshot {self.snapshotid} on volume {self.volumename}")
        return

    def rollback_snapshot(self, token):
        heads = headers 
        heads["authorization"] = token.id_token
        req = requests.get(api_url+f"/volumes/{self.volumename}/snaphots/{self.name}/rollback", headers=heads)
        if req.status_code != 200:
            print(f"Failed to roll back snapshot {self.snapshotid} for volume {self.volumename}")
            return
        print(f"Successfully rolled back snapshot {self.snapshotid} for volume {self.volumename}")
        return

    def __str__(self):
        return f"Volumez Snapshot for Volume {self.volumename}"


class Snapshots:
    def __init__(self, token):
        self.token = token
        self.headers = headers
        self.headers["authorization"] = self.token.id_token

    def get_snapshots(self, vol=None):
        if vol:
            req_url = api_url+"/volumes/"+vol+snap_url
        else:
            req_url = api_url+snap_url
        req = requests.get(req_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get snapshots from API. {req.reason}")
            return
        res = json.loads(req.text)
        self.snapshots = []
        for r in res:
            s = Snapshot()
            s.new(r)
            self.snapshots.append(s)
        print(f"Got {len(self.snapshots)} snapshots from API")
        return

    def __str__(self):
        return f"Volumez Snapshots"