from email import header
from os import access
import requests
import json
from ..common.settings import api_url, get_headers, auth_url
from ..core.attachments import Attachments
from ..core.jobs import Jobs
from ..core.nodes import Nodes
from ..core.policies import Policies
from ..core.snapshots import Snapshots
from ..core.volumes import Volumes
from ..core.media import Medias


class Token:
    def __init__(self, access_token, expires, id_token, refresh_token, token_type):
        self.access_token = access_token
        self.expires = expires
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.token_type = token_type

class VolumezAPI:
    ttoken_url = "/tenant/token"
    def _initialize(self):
        self.attachements = Attachments(self.headers)
        self.jobs = Jobs(self.headers)
        self.medias = Medias(self.headers)
        self.nodes = Nodes(self.headers)
        self.volumes = Volumes(self.headers)
        self.policies = Policies(self.headers)
        self.snapshots = Snapshots(self.headers)

    def signin(self, email, password):
        req = requests.post(api_url+auth_url, data=json.dumps({'email': email, 'password': password}))
        if req.status_code != 200:
            return {"error": "Failed to sign in to API", "reason": req.reason}
        try:
            res = json.loads(req.text)
        except:
            print("Authentication succeeded but received an invalid response from the API. Unable to continue")
            return
        self.headers = get_headers(res["IdToken"])
        self._initialize()
        return