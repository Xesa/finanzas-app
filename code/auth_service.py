import http.client
import random
import string
import hashlib
import base64
import urllib.parse
import requests
import json

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import WebApplicationClient
from config import Constants



class AuthService:

    def __init__(self):

        self.scopes = 'AIS'
        self.state = self.generateState()
        self.codeVerifier = self.generateCodeVerifier()
        self.codeChallenge = self.generateCodeChallenge(self.codeVerifier)
        self.codeChallengeMethod = 'S256'

        self.authorizationBaseUrl = Constants.get("production-auth") + "/authorize"
        self.tokenBaseUrl = Constants.get("production-auth") + "/token"

        self.redsysClient = Constants.get("redsys-client")
        self.redirectUri = Constants.get("serveo-domain") + "/token"
        self.grantType = "authorization_code"
        self.authorizationCode = None

        self.authorizationUrl = f"{urllib.parse.quote(self.authorizationBaseUrl)}" \
                            f"?response_type=code" \
                            f"&client_id={urllib.parse.quote(self.redsysClient)}" \
                            f"&scope={urllib.parse.quote(self.scopes)}" \
                            f"&state={urllib.parse.quote(self.state)}" \
                            f"&redirect_uri={urllib.parse.quote(self.redirectUri)}" \
                            f"&code_challenge={urllib.parse.quote(self.codeChallenge)}" \
                            f"&code_challenge_method={urllib.parse.quote(self.codeChallengeMethod)}"

        self.tokenUrl = None
        self.token = None

        self.oauth = OAuth2Session(
            client_id = self.redsysClient,
            scope = self.scopes,
            redirect_uri = self.redirectUri)

        self.client = WebApplicationClient(self.redsysClient)




    def getAuthorizationUrl(self):
        return urllib.parse.unquote(self.authorizationUrl)

    def getToken(self, authorizationCode, state):

        self.authorizationCode = authorizationCode

        conn = http.client.HTTPSConnection("hubpsd2.redsys.es")

        data = {
            'grant_type' : 'authorization_code',
            'client_id' : self.redsysClient,
            'code' : self.authorizationCode,
            'redirect_uri' : self.redirectUri,
            'code_challenge' : self.codeVerifier
        }

        encodedData = urllib.parse.urlencode(data)

        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        conn.request("POST",
                     "/api-oauth-xs2a/services/rest/BancSabadell/token",
                     body=encodedData,
                     headers=headers)

        response = conn.getresponse()
        responseData = response.read().decode()
        responseJson = json.loads(responseData)

        print(response)
        print(responseData)
        print(responseJson)
        self.token = responseJson


        self.tokenUrl = f"{urllib.parse.quote(self.grantType)}" \
                        f"&client_id={urllib.parse.quote(self.redsysClient)}" \
                        f"&code={urllib.parse.quote(self.authorizationCode)}" \
                        f"&redirect_uri={urllib.parse.quote(self.redirectUri)}" \
                        f"&code_challenge={urllib.parse.quote(self.codeVerifier)}"

        return self.token




    def generateState(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

    def generateCodeVerifier(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(43))

    def generateCodeChallenge(self, codeVerifier):
        sha256 = hashlib.sha256(codeVerifier.encode()).digest()
        codeChallenge = base64.urlsafe_b64encode(sha256).rstrip(b'=').decode('utf-8')
        return codeChallenge