import requests
import json

from ..common.settings import api_url, headers, volumes_url
from .snapshots import Snapshot
from .attachments import Attachment, Attachments

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

snaphelp = """
    {
        'consistency': 'crash', 
        'consistencygroup': False, 
        'policy': False, 
        'name': 'snap-name', 
        'targetsecret': '', 
        'time': '', 
        'used': 0, 
    }
"""
class Volume:
    
    def new(self, vols_dict=None):
        if vols_dict:
            if type(vols_dict) is dict:
                self.__dict__ = vols_dict
            else:
                print(f"The volume object takes an argument of a dictionary defining the volume details")
                return
        return
    
    def __str__(self):
        return f"Volumez Volume {self.volumeid} {self.name}"


class Volumes:
    def __init__(self, headers):
        self.headers = headers
        self.volume_list = self.get_volumes()

    def get_volume(self, volume):
        req = requests.get(api_url+volumes_url+f"/{volume}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get volume properties for {volume}. {req.reason}")
            return
        n = Volume()
        n.new(json.loads(req.text))
        return n
        
    def get_volumes(self):
        req = requests.get(api_url+volumes_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Error getting a list of volumes. {req.reason}")
            return
        res = json.loads(req.text)
        volume_list = []
        for r in res:
            v = Volume()
            v.new(r)
            volume_list.append(v)
        return volume_list


    def create_volume(self, volume):
        req = requests.post(api_url+volumes_url, headers=self.headers, data=json.dumps(volume.__dict__))
        if req.status_code != 200:
            print(f"Failed to create volume. {req.reason}")
            return
        print(f"Created volume {self.name}")
        return

    def delete_volume(self, volume):
        req = requests.delete(api_url+volumes_url+"/"+volume.volumeid, headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to delete volume {volume.volumeid}. {req.reason}")
            return
        print(f"Deleted volume {volume.volumeid}")
        return

    def get_snapshot(self, volume, snapshot):
        req = requests.get(api_url+f"/volumes/{volume.name}/snapshots/{snapshot.name}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get properties of snapshot {snapshot.name}. Check ID and try again")
            print(f"Reason: {req.reason}")
            return
        s = Snapshot()
        s.__dict__ = json.loads(req.text)
        return s

    def get_snapshots(self, volume):
        req = requests.get(api_url+f"/volumes/{volume.name}/snapshots", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get snapshots from API for volume {self.name}")
            return
        res = json.loads(req.text)
        snapshots = []
        for r in res:
            s = Snapshot()
            s.new(r)
            snapshots.append(s)
        return snapshots

    def create_snapshot(self, snap_dict):
        req = requests.post(api_url+f"/volumes/{self.name}/snapshots", headers=self.headers, data=json.dumps(snap_dict))
        if req.status_code != 200:
            print(f"Failed to create snapshot for volume {self.name}. {req.reason}")
            return
        print(f"Created snapshot for volume {self.name}")
        return

    def delete_snapshot(self, volume, snapshot):
        req = requests.delete(api_url+f"/volumes/{volume.name}/snapshots/{snapshot}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to delete snapshot {snapshot}. {req.reason}")
            return
        print(f"Deleted snapshot {snapshot} on volume {volume.name}")
        return

    def rollback_snapshot(self, volume, snapshot):
        req = requests.get(api_url+f"/volumes/{volume.name}/snaphots/{snapshot}/rollback", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to roll back snapshot {snapshot} for volume {volume.name}")
            return
        print(f"Successfully rolled back snapshot {snapshot} for volume {volume.name}")
        return

    def get_attachments(self, volume, snapshot=None):
        if not snapshot:
            snapshot='top'
        url = f"{api_url}{volumes_url}/{volume.name}/snapshots/{snapshot}/attachments"
        req = requests.get(url, headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get attachments for snapshot {snapshot}. {req.reason}")
            return
        res = json.loads(req.text)
        attachments = []
        for r in res:
            a = Attachment(self.headers)
            a.new(r)
            attachments.append(a)
        return attachments

    def create_attachment(self, volume, node, proto, snapshot=None, mountpoint=None):
        if not snapshot:
            snapshot='top'
        payload = {'volumename': volume.name, 'snapshotname':snapshot, 'node':node, 'protocol': proto }
        if mountpoint:
            payload['mountpoint'] = mountpoint
        url = f"{api_url}{volumes_url}/{volume.name}/snapshots/{snapshot}/attachments"
        req = requests.post(url, headers=self.headers, data=json.dumps(payload))
        if req.status_code != 200:
            print(f"Error creating attachment: {req.reason}")
            return
        print(f"Created attachment for volume {volume.name} on node {node}")
        return

    def filter(self, volumes=None, **kwargs):
        opers = {'eq': '==','gt': '>','lt': '<','gte': '>=','lte': '<=', 'neq':'!=' } 
        if not volumes:
            volumes = self.volume_list
        filtered_list = []
        oper_list = []
        for k, v in kwargs.items():
            try:
                key, oper = k.split("__")
                oper_list.append({'attribute': key, 'operator':opers[oper], 'value': v})
            except ValueError:
                oper_list.append({'attribute': k, 'operator':'==', 'value':v})
        for v in volumes:
            if all(eval('val1%sval2' % (o['operator']), {'val1': getattr(v,o['attribute']), 'val2': o['value']} ) for o in oper_list):
                filtered_list.append(v)
        return filtered_list

    def __str__(self):
        return f"Volumez Volume"