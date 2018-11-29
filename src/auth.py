import json
import time
import logging

import urllib
import httplib2

import google.auth.crypt
import google.auth.jwt

from . import gcs_ext

_logger = logging.getLogger("drepin-service")


def get_bearer_token(headers):
    authorization = headers.get("Authorization")
    if authorization and authorization[0:7] == "Bearer ":
        token = authorization[7:]
        return token
    else:
        return None


class AuthInfo(object):
    def __init__(self, token, expires, key_file_path, kms_project_id):
        self.token = token
        self.expires = expires
        self.key_file_path = key_file_path
        self.kms_project_id = kms_project_id


class AuthToken(object):

    _auth_info_dict = dict()

    def __init__(self, name, key_file_path, kms_project_id):
        self.name = name
        auth_info = AuthToken._auth_info_dict.get(self.name)
        if not auth_info:
            # This is the first time such an AuthToken object with such name was instantiated
            auth_info = AuthInfo("", 0, key_file_path, kms_project_id)
            AuthToken._auth_info_dict[self.name] = auth_info
        else:
            if auth_info.key_file_path != key_file_path or auth_info.kms_project_id != kms_project_id:
                raise TypeError(
                    "AuthToken with such name, but different attributes, has already been created")

    @staticmethod
    def _generate_jwt(iat, exp, key_file_path, kms_project_id, target_audience):
        """Generates a signed JSON Web Token using a Google API Service Account."""

        key_content = gcs_ext.get_gcs_encrypted_file_as_string(
            key_file_path, kms_project_id)
        service_account_key = json.loads(key_content)

        client_email = service_account_key['client_email']

        signer = google.auth.crypt.RSASigner.from_service_account_info(
            service_account_key)

        header = {"type": "JWT", "alg": "RS256"}
        payload = {
            'iat': iat,
            "exp": exp,
            "iss": client_email,
            "target_audience": target_audience,
            "aud": "https://www.googleapis.com/oauth2/v4/token"
        }

        jwt = google.auth.jwt.encode(
            signer=signer, payload=payload, header=header)
        return jwt

    def get_auth_info(self):

        iat = int(time.time())
        exp = iat + 3600  # One hour in seconds
        auth_info = AuthToken._auth_info_dict.get(self.name)
        if auth_info.expires > iat + 4:
            return auth_info

        # Using the key file-signed JWT
        #  API -> Credentials -> OAuth 2.0 client IDs: drepin-service: Client ID
        audience = "783663625239-XXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com"

        jwt = AuthToken._generate_jwt(
            iat, exp, auth_info.key_file_path, auth_info.kms_project_id, audience)

        # send a request to the Google Token endpoints https://www.googleapis.com/oauth2/v4/token
        # to get a Google ID to use with your API request:
        params = urllib.parse.urlencode({'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                                         'assertion': jwt})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn = httplib2.Http()
        (rest, content) = conn.request("https://www.googleapis.com/oauth2/v4/token",
                                       method="POST", body=params, headers=headers)
        if rest.status != 200:
            print("Request to sign tocken '{}' failed: \n{}".format(self.name, rest))
            exit(-1)

        res = json.loads(content.decode('utf-8'))

        new_token = res['id_token']
        new_auth_info = AuthInfo(
            new_token, exp, auth_info.key_file_path, auth_info.kms_project_id)
        AuthToken._auth_info_dict[self.name] = new_auth_info

        _logger.debug("Generated a new '%s' token", self.name)

        return new_auth_info

    def get_auth_token(self):
        auth_info = self.get_auth_info()
        return auth_info.token
