import requests
import json
from .settings import api_url, headers, attachments_url




class Attachment:
    def new(self, attach_dict):
        if type(attach_dict) is dict:
            self.__dict__ = attach_dict
        else:
            print(f"The attachment object takes an argument of a dictionary defining the attachement. Check Attachment.help() for more information")
            return
        return


class Attachments:
    def __init__(self, token):
        self.token = token
        self.headers = headers
        self.headers["authorization"] = self.token.id_token

    def get_attachments(self):
        req = requests.get(api_url+attachments_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Error getting list of attachments. {req.reason}")
            return
        res = json.loads(req.text)
        self.attachments = []
        for r in res:
            a = Attachment()
            a.new(r)
            self.attachments.append(a)
        return