"""Module for service utils."""
from typing import Optional
import urllib.parse
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

import jwt
import requests
from cryptography.hazmat.primitives import serialization


def get_maskinporten_token(
        client_id: str,
        virksomhetssertifikat: str,
        scope: str,
        private_key: str,

):
    """
    Logging in using maskinporten to get the ID-Porten token.
    The ID-porten token is later exchanged to a altinn token that contains
    more information.

    :param client_id: Client id for the integration.
    :param virksomhetssertifikat: Virksomhetssertifikat /the public certificate.
    :param scope: Scope for the integration.
    :param private_key: Private key in .pem format.
    :return:ID-porten token as str.
    """
    url = "https://maskinporten.no/token"
    now = datetime.now(tz=timezone.utc)

    private_key_obj = serialization.load_pem_private_key(
        data=bytes(private_key, "utf-8"), password=None
    )

    jwt_headers = {
        "alg": "RS256",
        "x5c": [virksomhetssertifikat],  # public key
    }
    jwt_body = {
        "aud": "https://maskinporten.no/",
        "iss": client_id,
        "scope": scope,
        "iat": now.timestamp(),
        "exp": (now + timedelta(seconds=120)).timestamp(),
        "resource": "https://www.altinn.no/",
    }
    jwt_token = jwt.encode(
        payload=jwt_body,
        headers=jwt_headers,
        key=private_key_obj,
        algorithm="RS256",
    )

    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {jwt_token}",

    }
    body_attrs = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token,
    }

    encoded_data = urllib.parse.urlencode(body_attrs)
    form_data = encoded_data.encode("utf-8")

    response = requests.post(url, data=form_data, headers=headers)
    return response.json()


@dataclass
class QueryParamsAuthorize:
    client_id: str
    redirect_uri: str
    response_type: str
    code_challenge: str
    acr_value: Optional[str] = None
    response_mode: Optional[str] = None
    ui_locales: Optional[str] = None
    prompt: Optional[str] = None
    state: Optional[str] = None  # Recommended
    nonce: Optional[str] = None  # Recommended
    scope: str = "openid"
    code_challenge_method: str = "S256"

    def get_query_params(self):
        data = {k: v for k, v in self.__dict__.items() if v is not None}
        return urllib.parse.urlencode(data)


@dataclass
class QueryParamsToken:
    client_id: str
    grant_type: str
    code: str
    redirect_uri: str
    code_verifier: str


def oidc_authorize(authorize_params: QueryParamsAuthorize):
    """
    Authorize with Id-porten.
    :return:
    """
    base_url = "https://login.idporten.no/authorize?"  # TODO: This is not up and running.
    url = base_url + authorize_params.get_query_params()
    r = requests.get(url)
    print(r.status_code)
    print(r.content)
    # with open("page.html", "w") as file:
    #     file.write(r.text)
    return r
