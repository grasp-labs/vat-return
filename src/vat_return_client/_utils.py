"""Module for service utils."""
import requests

import vat_return_client.constants as constants


def _get_id_token(client_id: str, scope: str) -> str:
    response = requests.get(
        f"https://{constants.AUTH_DOMAIN}/.well-known/openid-configuration"
    ).json()["jwks_uri"]
    jwks = requests.get(response).json()
    return jwks

