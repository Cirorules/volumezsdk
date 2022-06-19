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
    def __init__(self, token):
        self.token=token

    def help(self, command=None):
        if command:
            if command == 'new':
                print("The new function instantiates a new Volume object.")
                print("The new function takes one argument, a dictionary describinng the Volume.")
                print(f"{volhelp}")
            if command == 'get_volume':
                print("get_volume retrives the properties of a single volume from the API using a Volume object.")
                print("The command requires the Authentication.tokens object as a parameter")
            if command == 'create_volume':
                print("Create a volume with the parameters configured in the Volume instance. Authentication.tokens is a required parameter")
            if command == 'delete_volume':
                print("Deletes the volume by name. Authentication.tokens is required.")
            if command == 'get_snapshot':
                print("Get a snapshot for this volume by the snapshot name. Authentication.tokens and the name of the snapshot are required.")
                print("Returns a Snapshot object.")
            if command == 'get_snapshots':
                print("Get all the snapshots for the configured volume. Returns an array of Snapshot objects.")
            if command == 'create_snapshot':
                print("Creates a snapshot for the Volume instance. Requires Authentication.tokens and a dict defining the snapshot as arguments. ")
                print(f"{snaphelp}")
        else:
            print("get_volume        - Get volume properties and populate this Volume instance. Usage: Volume.get_volume(auth.tokens, 'dbvol-u01')")
            print("create_volume     - Create a new volume using the properties of this Volume instance. Usage: Volume.create_volume(auth.tokens)")
            print("delete_volume     - Delete the volume with the name of this Volume.name instance. This is not recoverable, use caution.")
            print("get_snapshot      - Authentication.tokens and snapshot name are required. Returns a Snapshot() instance. Usage: Volume.get_snapshot(auth.tokens, 'u01-snap-Fridy').")
            print("get_snapshots     - Get all the snapshots for the volume. Returns an array of Snapshot() instances. Usage: Volume.get_snapshots(auth.tokens)")
            print("create_snapshot   - Create a snapshot for this Volume instance. See command help for usage.")
            print("delete_snapshot   - Delete the snapshot by name for this volume. Usage: Volume.delete_snapshot(auth.tokens, 'name-of-snap'")
            print("rollback_snapshot - Return the state of the volume to the snapshot provided. Usage: Volume.rollback_snapshot(auth.tokens, 'name-of-snap'")

    def new(self, vols_dict):
        if type(vols_dict) is dict:
            self.__dict__ = vols_dict
        else:
            print(f"The volume object takes an argument of a dictionary defining the volume details")
            return
        return
    
    def get_volume(self, token, vol_name=None):
        heads = headers
        heads["authorization"] = token.id_token
        if vol_name:
            get_vol = vol_name
        else:
            get_vol = self.name
        req = requests.get(api_url+volumes_url+"/"+get_vol, headers=heads)
        if req.status_code != 200:
            print(f"Failed to get volume properties for {get_vol}. {req.reason}")
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
        print(f"Created volume {self.name}")
        return

    def delete_volume(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.delete(api_url+volumes_url+"/"+self.volumeid, headers=heads)
        if req.status_code != 200:
            print(f"Failed to delete volume {self.volumeid}. {req.reason}")
            return
        print(f"Deleted volume {self.volumeid}")
        return

    def get_snapshot(self, token, snapshot):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.get(api_url+f"/volumes/{self.name}/snapshots/{snapshot}", headers=heads)
        if req.status_code != 200:
            print(f"Failed to get properties of snapshot {snapshot}. Check ID and try again")
            print(f"Reason: {req.reason}")
            return
        s = Snapshot()
        s.__dict__ = json.loads(req.text)
        return s

    def get_snapshots(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.get(api_url+f"/volumes/{self.name}/snapshots", headers=heads)
        if req.status_code != 200:
            print(f"Failed to get snapshots from API for volume {self.name}")
            return
        res = json.loads(req.text)
        snapshots = []
        for r in res:
            s = Snapshot(self.token)
            s.new(r)
            snapshots.append(s)
        return snapshots

    def create_snapshot(self, token, snap_dict):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.post(api_url+f"/volumes/{self.name}/snapshots", headers=heads, data=json.dumps(snap_dict))
        if req.status_code != 200:
            print(f"Failed to create snapshot for volume {self.name}. {req.reason}")
            return
        print(f"Created snapshot for volume {self.name}")
        return

    def delete_snapshot(self, token, snapshot):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.delete(api_url+f"/volumes/{self.name}/snapshots/{snapshot}", headers=heads)
        if req.status_code != 200:
            print(f"Failed to delete snapshot {snapshot}. {req.reason}")
            return
        print(f"Deleted snapshot {snapshot} on volume {self.name}")
        return

    def rollback_snapshot(self, token, snapshot):
        heads = headers 
        heads["authorization"] = token.id_token
        req = requests.get(api_url+f"/volumes/{self.name}/snaphots/{snapshot}/rollback", headers=heads)
        if req.status_code != 200:
            print(f"Failed to roll back snapshot {snapshot} for volume {self.name}")
            return
        print(f"Successfully rolled back snapshot {snapshot} for volume {self.name}")
        return

    def get_attachments(self, token, snapshot=None):
        if not snapshot:
            snapshot='top'
        heads = headers
        heads["authorization"] = token.id_token
        url = f"{api_url}{volumes_url}/{self.name}/snapshots/{snapshot}/attachments"
        req = requests.get(url, headers=heads)
        if req.status_code != 200:
            print(f"Failed to get attachments for snapshot {snapshot}. {req.reason}")
            return
        res = json.loads(req.text)
        attachments = []
        for r in res:
            a = Attachment(self.token)
            a.new(r)
            attachments.append(a)
        return attachments

    def create_attachment(self, token, node, proto, snapshot=None, mountpoint=None):
        if not snapshot:
            snapshot='top'
        heads = headers
        heads["authorization"] = token.id_token
        payload = {'volumename': self.name, 'snapshotname':snapshot, 'node':node, 'protocol': proto }
        if mountpoint:
            payload['mountpoint'] = mountpoint
        url = f"{api_url}{volumes_url}/{self.name}/snapshots/{snapshot}/attachments"
        req = requests.post(url, headers=heads, data=json.dumps(payload))
        if req.status_code != 200:
            print(f"Error creating attachment: {req.reason}")
            return
        print(f"Created attachment for volume {self.name} on node {node}")
        return


    def __str__(self):
        return f"Volumez Volume {self.volumeid} {self.name}"


class Volumes:
    def __init__(self, token):
        self.token = token
        self.headers = headers
        self.headers["authorization"] = self.token
        self.volume_list = self.get_volumes()

    def get_volume(self, volume):
        req = requests.get(api_url+volumes_url+f"/{volume}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get volume properties for {volume}. {req.reason}")
            return
        n = Volume(self.token)
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
            v = Volume(self.token)
            v.new(r)
            volume_list.append(v)
        return volume_list

    def filter(self, volumes=None, **kwargs):
        if not volumes:
            volumes = self.volume_list
        filtered_list = []
        for n in volumes:
            if all(eval('"%s"=="%s"' % (getattr(n,k), v)) for k, v in kwargs.items()):
                filtered_list.append(n)
        return filtered_list

    def __str__(self):
        return f"Volumez Volume"