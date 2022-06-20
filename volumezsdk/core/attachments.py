from gc import get_stats
import requests
import json
from ..common.settings import api_url, headers, attachments_url


class Attachment:
    def new(self, attach_dict):
        if type(attach_dict) is dict:
            self.__dict__ = attach_dict
        else:
            print(f"The attachment object takes an argument of a dictionary defining the attachement. Check Attachment.help() for more information")
            return
        return

    def __str__(self):
        if hasattr(self, "volumename"):
            return f"Volumez Attachment {self.volumename}"
        else:
            return f"New Volumez Attachment"

class Attachments:
    def __init__(self, headers):
        self.headers = headers
        self.attachment_list = self.get_attachments()
    class attachment(Attachment):
        def __init__(self):
            super().__init__(self)
            
    def get_attachment(self, volume, snap, node):
        req = requests.get(api_url+f"/volumes/{volume}/snapshots/{snap}/attachments/{node}", headers=self.headers)
        if req.status_code != 200:
            print(f"Error getting attachment. {req.reason}")
            return
        a = Attachment()
        a.new(json.loads(req.text))
        return a

    def get_attachments(self):
        req = requests.get(api_url+attachments_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Error getting list of attachments. {req.reason}")
            return
        res = json.loads(req.text)
        attachment_list = []
        for r in res:
            a = Attachment()
            a.new(r)
            attachment_list.append(a)
        return attachment_list

    def filter(self, attachment=None, **kwargs):
        opers = {'eq': '==','gt': '>','lt': '<','gte': '>=','lte': '<=', 'neq':'!=' } 
        if not attachment:
            attachment = self.attachment_list
        filtered_list = []
        oper_list = []
        for k, v in kwargs.items():
            try:
                key, oper = k.split("__")
                oper_list.append({'attribute': key, 'operator':opers[oper], 'value': v})
            except ValueError:
                oper_list.append({'attribute': k, 'operator':'==', 'value':v})
        for a in attachment:
            if all(eval('val1%sval2' % (o['operator']), {'val1': getattr(a,o['attribute']), 'val2': o['value']} ) for o in oper_list):
                filtered_list.append(a)
        return filtered_list

    def __str__(self):
        return f"Volumez Attachments"