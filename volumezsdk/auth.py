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

class Authentication:
    ttoken_url = "/tenant/token"
    def signin(self, email, password):
        req = requests.post(api_url+auth_url, data=json.dumps({'email': email, 'password': password}))
        if req.status_code != 200:
            return {"error": "Failed to sign in to API", "reason": req.reason}
        try:
            res = json.loads(req.text)
        except:
            print("Authentication succeeded but received an invalid response from the API. Unable to continue")
            return
        try:
            tokens = Token(access_token=res["AccessToken"], expires=res["ExpiresIn"], id_token=res["IdToken"], refresh_token=res["RefreshToken"], token_type=res["TokenType"])
        except Exception as e:
            print(f"Unable to create token object. Please try again. Exception: {str(e)}")
        
        self.tokens = tokens
        return
