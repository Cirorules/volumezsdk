import requests
import json
from ..common.settings import snap_url, api_url, headers

class Snapshot:
    def new(self, snaps_dict=None):
        if snaps_dict:
            if type(snaps_dict) is dict:
                self.__dict__ = snaps_dict
            else:
                print(f"If provided, Snapshot requires the argument to be a dictionary defining the Snapshot instance")
        return
    
    def __str__(self):
        return f"Volumez Snapshot {self.snapshotid} for Volume {self.volumename}"


class Snapshots:
    def __init__(self, headers):
        self.headers = headers
        self.snapshot_list = self.get_snapshots()

    def get_snapshot(self, volume, snapshot):
        req = requests.get(api_url+f"/volumes/{volume}/snapshots/{snapshot}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get properties of snapshot {snapshot}. Check snapshot name and try again")
            print(f"Reason: {req.reason}")
            return
        snap = Snapshot()
        snap.new(json.loads(req.text))
        return snap

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
        snapshot_list = []
        for r in res:
            s = Snapshot()
            s.new(r)
            snapshot_list.append(s)
        return snapshot_list

    def get_snapshot(self, volume=None, snapshot=None):
        if not volume or not snapshot:
            print("Required parameters: volume='volume_name', snapshot='snapshot_name'")
            return
        req = requests.get(api_url+f"/volumes/{volume}/snapshots/{snapshot}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get properties of snapshot {snapshot}. Check ID and try again")
            print(f"Reason: {req.reason}")
            return
        snap = Snapshot()
        snap.new(json.loads(req.text))
        return snap

    def create_snapshot(self, volume=None):
        if not volume:
            print("Required parameter: volume='volume_name'")
            return
        req = requests.post(api_url+f"/volumes/{volume}/snapshots", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to create snapshot for volume {volume}. {req.reason}")
            return
        print(f"Created snapshot for volume {volume}")
        return

    def delete_snapshot(self, volume=None, snapshot=None):
        if not volume or not snapshot:
            print("Required parameters: volume='volume_name, snapshot='snapshot_name'")
        req = requests.delete(api_url+f"/volumes/{volume}/snapshots/{snapshot}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to delete snapshot {snapshot}. {req.reason}")
            return
        print(f"Deleted snapshot {snapshot} on volume {volume}")
        return

    def rollback_snapshot(self, token):
        req = requests.get(api_url+f"/volumes/{self.volumename}/snaphots/{self.name}/rollback", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to roll back snapshot {self.snapshotid} for volume {self.volumename}")
            return
        print(f"Successfully rolled back snapshot {self.snapshotid} for volume {self.volumename}")
        return

    def filter(self, snapshots=None, **kwargs):
        opers = {'eq': '==','gt': '>','lt': '<','gte': '>=','lte': '<=', 'neq':'!=' } 
        if not snapshots:
            snapshots = self.snapshot_list
        filtered_list = []
        oper_list = []
        for k, v in kwargs.items():
            try:
                key, oper = k.split("__")
                oper_list.append({'attribute': key, 'operator':opers[oper], 'value': v})
            except ValueError:
                oper_list.append({'attribute': k, 'operator':'==', 'value':v})
        for s in snapshots:
            if all(eval('val1%sval2' % (o['operator']), {'val1': getattr(s,o['attribute']), 'val2': o['value']} ) for o in oper_list):
                filtered_list.append(s)
        return filtered_list

    def __str__(self):
        return f"Volumez Snapshots"