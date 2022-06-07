from email import header
from os import access
import requests
import json
from .settings import api_url, headers, auth_url


class Token:
    def __init__(self, access_token, expires, id_token, refresh_token, token_type):
        self.access_token = access_token
        self.expires = expires
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.tenant_token = ""

class Authentication:
    ttoken_url = "/tenant/token"
    def signin(self, email, password):
        req = requests.post(api_url+auth_url, data=json.dumps({'email': email, 'password': password}))
        if req.status_code != 200:
            return {"error": "Failed to sign in to API", "reason": req.reason}
        res = json.loads(req.text)
        tokens = Token(access_token=res["AccessToken"], expires=res["ExpiresIn"], id_token=res["IdToken"], refresh_token=res["RefreshToken"], token_type=res["TokenType"])
        headers["authorization"] = tokens.id_token
        req = requests.get(api_url+self.ttoken_url, headers=headers)
        if req.status_code != 200:
            return {"error": "Failed to get tenant token", "reason": req.reason}
        res = json.loads(req.text)
        tokens.tenant_token = res["AccessToken"]
        return tokens
