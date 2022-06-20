import requests
import json
from ..common.settings import policy_url, api_url, headers


class Policy:
    def new(self, policy_dict):
        if type(policy_dict) is dict:
            self.__dict__ = policy_dict
        else:
            print("The Policy object takes an agrument of a dictionary defining the policy. All items of the policy are required")
            return

    def __str__(self):
        return f"Policy {self.name}"

class Policies:
    def __init__(self, headers):
        self.headers = headers
        self.policy_list = self.get_policies()

    def get_policy(self, policy):
        req = requests.get(api_url+policy_url+f"/{policy}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get policy. {req.reqson}")
            return
        p = Policy()
        p.new(json.loads(req.text))
        return p
        
    def get_policies(self):
        req = requests.get(api_url+policy_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get policies. {req.reason}")
            return
        res = json.loads(req.text)
        policy_list = []
        for r in res:
            p = Policy()
            p.new(r)
            policy_list.append(p)
        return policy_list
    

    def create_policy(self, policy):
        req = requests.post(api_url+policy_url, headers=self.headers, data=json.dumps(policy.__dict__))
        if req.status_code != 200:
            print(f"Failed to create policy {policy.name}. {req.reason}")
            return
        print(f"Created policy {policy.name}")

    def delete_policy(self, policy):
        req = requests.delete(api_url+policy_url+"/"+policy.name, headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to delete policy. {req.reason}")
            return
        print(f"Deleted policy {policy.name}")

    def update_policy(self, policy):
        req = requests.patch(api_url+policy_url+"/"+policy.name, headers=self.headers, data=json.dumps(policy.__dict__))
        if req.status_code != 200:
            print(f"Error updating policy: {req.reason}")
            return
        print(f"Updated policy {policy.name}")

    def filter(self, policies=None, **kwargs):
        opers = {'eq': '==','gt': '>','lt': '<','gte': '>=','lte': '<=', 'neq':'!=' } 
        if not policies:
            policies = self.policy_list
        filtered_list = []
        oper_list = []
        for k, v in kwargs.items():
            try:
                key, oper = k.split("__")
                oper_list.append({'attribute': key, 'operator':opers[oper], 'value': v})
            except ValueError:
                oper_list.append({'attribute': k, 'operator':'==', 'value':v})
        for p in policies:
            if all(eval('val1%sval2' % (o['operator']), {'val1': getattr(p,o['attribute']), 'val2': o['value']} ) for o in oper_list):
                filtered_list.append(p)
        return filtered_list

    def __str__(self):
        return f"Volumez Policies"

