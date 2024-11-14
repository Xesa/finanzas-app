import requests
import json
import random
import string
import hashlib
import base64
import urllib.parse
from config import Constants



class AuthService:

    def __init__(self):

        self.scopes = 'AIS'
        self.state = self.generateState()
        self.codeVerifier = self.generateCodeVerifier()
        self.codeChallenge = self.generateCodeChallenge(self.codeVerifier)
        self.codeChallengeMethod = 'S256'

        self.authorizationUri = Constants.get("production-auth") + "/authorize"
        self.redsysClient = Constants.get("redsys-client")
        self.redirectUri = Constants.get("serveo-domain") + "/token"

        self.authorizationUrl = f"{urllib.parse.quote(self.authorizationUri)}/authorize" \
                            f"?response_type=code" \
                            f"&client_id={urllib.parse.quote(self.redsysClient)}" \
                            f"&scope={urllib.parse.quote(self.scopes)}" \
                            f"&state={urllib.parse.quote(self.state)}" \
                            f"&redirect_uri={urllib.parse.quote(self.redirectUri)}" \
                            f"&code_challenge={urllib.parse.quote(self.codeChallenge)}" \
                            f"&code_challenge_method={urllib.parse.quote(self.codeChallengeMethod)}"


    def generateState(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

    def generateCodeVerifier(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(43))

    def generateCodeChallenge(self, codeVerifier):
        sha256 = hashlib.sha256(codeVerifier.encode()).digest()
        codeChallenge = base64.urlsafe_b64encode(sha256).rstrip(b'=').decode('utf-8')
        return codeChallenge

print(AuthService().authorizationUrl)