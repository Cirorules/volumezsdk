import requests
import json
from ..common.settings import api_url, headers, nodes_url


class Node:
    def new(self, nodes_dict=None):
        if nodes_dict:
            if type(nodes_dict) is dict:
                self.__dict__ = nodes_dict
            else:
                print("If provided, the Node object takes and argument of a dictionary defining the node attributes.")

    def __str__(self):
        return f"Volumez Node {self.name}"


class Nodes:
    def __init__(self, headers):
        self.headers = headers
        self.node_list = self.get_nodes()

    def get_node(self, node_name):
        req = requests.get(api_url+nodes_url+f"/{node_name}", headers=headers, data=json.dumps(self.__dict__))
        if req.status_code != 200:
            if req.status_code == 400:
                print(f"Invalid node name provided. Please check again")
            elif req.status_code == 404:
                print(f"Node not found. Please check again")
            else:
                print(f"Error getting properties of the node {req.status_code} status")
            return
        n = Node(self.headers)
        n.new(json.loads(req.text))
        return n

    def get_nodes(self):
        req = requests.get(api_url+nodes_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Error getting nodes: {req.reason}")
            return
        res = json.loads(req.text)
        node_list = []
        for r in res:
            n = Node()
            n.new(r)
            node_list.append(n)
        return node_list

    def filter(self, nodes=None, **kwargs):
        if not nodes:
            nodes = self.node_list
        filtered_list = []
        oper_list = []
        for k, v in kwargs.items():
            try:
                key, oper = k.split("__")
                oper_list.append({'attribute': key, 'operator':opers[oper], 'value': v})
            except ValueError:
                oper_list.append({'attribute': k, 'operator':'==', 'value':v})
        for n in nodes:
            if all(eval('val1%sval2' % (o['operator']), {'val1': getattr(n,o['attribute']), 'val2': o['value']} ) for o in oper_list):
                filtered_list.append(n)
        return filtered_list

    def __str__(self):
        return f"Volumez Nodes"