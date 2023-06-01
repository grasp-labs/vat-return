"""Module for service utils."""
import urllib.parse
from datetime import datetime, timedelta, timezone

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
