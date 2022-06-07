import requests
import json
from .settings import policy_url, api_url, headers


class Policy:
    def new(self, policy_dict):
        if type(policy_dict) is dict:
            self.__dict__ = policy_dict
        else:
            print("The Policy object takes an agrument of a dictionary defining the policy. All items of the policy are required")
            return

    def create_policy(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.post(api_url+policy_url, headers=heads, data=json.dumps(self.__dict__))
        if req.status_code != 200:
            print(f"Failed to create policy {self.name}. {req.reason}")
            return
        print(f"Created policy {self.name}")

    def delete_policy(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.delete(api_url+policy_url+"/"+self.name, headers=heads)
        if req.status_code != 200:
            print(f"Failed to delete policy. {req.reason}")
            return
        print(f"Deleted policy {self.name}")

    def update_policy(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.patch(api_url+policy_url+"/"+self.name, headers=heads, data=json.dumps(self.__dict__))
        if req.status_code != 200:
            print(f"Error updating policy: {req.reason}")
            return
        print(f"Updated policy {self.name}")

    def __str__(self):
        return f"Policy {self.name}"

class Policies:
    def __init__(self, token):
        self.token = token
        self.headers = headers
        self.headers["authorization"] = self.token.id_token

    def get_policies(self):
        req = requests.get(api_url+policy_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get policies. {req.reason}")
            return
        res = json.loads(req.text)
        self.policies = []
        for r in res:
            p = Policy()
            p.new(r)
            self.policies.append(p)
        return {"success": f"Got {len(res)} policies from the API"}

    def __str__(self):
        return f"Volumez Policies"

