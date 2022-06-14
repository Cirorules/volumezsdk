import requests
import json
from .settings import api_url, headers, nodes_url


class Node:
    def new(self, nodes_dict):
        if type(nodes_dict) is dict:
            self.__dict__ = nodes_dict
        else:
            print("The Node object takes and argument of a dictionary defining the node attributes.")

    def get_properties(self, token):
        headers["authorization"] = token.id_token
        req = requests.get(api_url+nodes_url, headers=headers, data=json.dumps(self.__dict__))
        if req.status_code != 200:
            if req.status_code == 400:
                print(f"Invalid node name provided. Please check again")
            elif req.status_code == 404:
                print(f"Node not found. Please check again")
            else:
                print(f"Error getting properties of the node {req.status_code} status")
            return
        res = json.loads(req.text)
        self.new(res)
        print(f"Retrived node properties")
        return

    def __str__(self):
        return f"Volumez Node {self.name}"


class Nodes:
    def __init__(self, token):
        self.token = token
        self.headers = headers
        self.headers["authorization"] = self.token.id_token

    def get_nodes(self):
        req = requests.get(api_url+nodes_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Error getting nodes: {req.reason}")
            return
        res = json.loads(req.text)
        self.nodes = []
        for r in res:
            n = Node()
            n.new(r)
            self.nodes.append(n)
        print(f"Got {len(self.nodes)} nodes from the API and stored in Nodes.nodes")

    def filter(self, node_name):
        if not hasattr(self, 'nodes'):
            self.get_nodes()
        for node in self.nodes:
            if node.name == node_name:
                return node
        print(f"Node {node_name} not found.")

    def __str__(self):
        return f"Volumez Nodes"