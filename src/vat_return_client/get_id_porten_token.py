"""
Module for getting the token from ID porten.
ref: https://skatteetaten.github.io/mva-meldingen/documentation/idportenautentisering/#konfigurere-applikasjonen-til-%C3%A5-bruke-integrasjonen-fra-samarbeidsportalen
"""
import base64
import json
import secrets
import sys
import time
import webbrowser
from base64 import urlsafe_b64decode, urlsafe_b64encode
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode

import jwt
import requests
from cryptography import x509

from settings import (
    ID_PORTEN_CLIENT_ID,
    SERVER_PORT,
    REDIRECT_URI,
    ID_PORTEN_AUTH_DOMAIN,
    ALGORITHMS,
    SCOPES,
)


class BrowserRedirectHandler(BaseHTTPRequestHandler):
    """
    A simple web server hosted locally.

    This class provides a custom request handler for HTTP GET requests.
    When a GET request is received, the server responds with a 200 status code
    and a simple HTML page that informs the user about the completion of the
    authentication process.

    Class Attributes:
        timeout (int): The timeout value for the server connection.
        result: Holds the result of the request handling process.

    Methods:
        do_GET(): Handles the HTTP GET request.
    """
    result = None

    def do_GET(self):
        """Handle HTTP GET request."""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authentication complete</title>
        </head>
        <body>
            <h1>Authentication complete</h1>
            <p>You may close this page. (Test page for redirect)</p>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())
        BrowserRedirectHandler.result = self


def random_bytes(n: int) -> bytes:
    """
    Generate a cryptographically secure random byte array of length n.
    """
    return secrets.token_bytes(n)


def base64_response(encoded_string: str, encoding: str) -> str:
    """
    Decode a Base64-encoded string using the specified encoding.

    :param encoded_string: The Base64-encoded string to decode.
    :param encoding: The encoding used for decoding the string.
    :return: The decoded string.
    """
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_str = decoded_bytes.decode(encoding)
    return decoded_str


def decode_dokument(dokument: dict) -> dict:
    """
    Decode the content of a document dictionary using Base64 decoding.

    :param dokument: The document dictionary containing "content" and
    "encoding" keys.
    :return: Modified dict with decoded content.
    """
    original_content = dokument["content"]
    encoding = dokument["encoding"]
    dokument["content"] = base64_response(original_content, encoding)
    return dokument


def get_jwks() -> dict:
    """
    Retrieve the JSON Web Key Set (JWKS) from id porten.

    :returns: The JWKS as a dictionary.
    """
    response = requests.get(
        f"https://{ID_PORTEN_AUTH_DOMAIN}/.well-known/openid-configuration"
    )
    jwks_uri = response.json()["jwks_uri"]
    jwks_response = requests.get(jwks_uri)
    jwks = jwks_response.json()
    return jwks


def load_public_certs(x5c: list) -> list:
    """Loads public certificates from x5c header."""
    return [
        x509.load_der_x509_certificate(
            base64.b64decode(cert),
        ) for cert in x5c
    ]


def get_id_token(
        client_id: str = ID_PORTEN_CLIENT_ID,
        scope: str = SCOPES,
        auth_domain: str = ID_PORTEN_AUTH_DOMAIN,
        server_port: int = SERVER_PORT,
        redirect_uri: str = REDIRECT_URI,
        server_timeout: int = 1000,
) -> dict:
    """
    Perform authentication and retrieve the ID token.
    Default attributes are towards test environments.

    :param client_id: Client id for the integration.
    :param scope: Scopes, default is the ones that is required.
    :param auth_domain: Environment specific auth domain.
    :param server_port: Port for the server.
    :param redirect_uri: The redirect uri specified in the integration.
    :param server_timeout: How long a person use to log-in via ID porten.
    :return: Authorization headers as dict.
    """
    # Clean to ensure a clean state before handling the auth process.
    BrowserRedirectHandler.result = None

    # Public clients need state parameter and PKCE challenge
    # https://tools.ietf.org/html/draft-ietf-oauth-browser-based-apps-00
    state = urlsafe_b64encode(random_bytes(16)).decode().rstrip("=")
    pkce_secret = urlsafe_b64encode(
        random_bytes(32),
    ).decode().rstrip("=").encode()
    pkce_challenge = urlsafe_b64encode(sha256(pkce_secret).digest()).decode()
    nonce = str(int(time.time() * 1e6))

    print("state:", state)
    print("pkce_secret:", pkce_secret.decode("utf-8"))
    print("pkce_challenge:", pkce_challenge)
    print("nonce:", nonce)

    authorize_query_params = {
        "scope": scope,
        "acr_values": "Level3",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "state": state,
        "nonce": nonce,
        "code_challenge": pkce_challenge,
        "code_challenge_method": "S256",
        "ui_locales": "nb"
    }
    encoded_params = urlencode(authorize_query_params, safe="?&=_")
    # Connecting to the /authorize endpoint.
    authorize_uri = f"https://{auth_domain}/authorize?{encoded_params}"

    # Starts the test server
    server = HTTPServer(("127.0.0.1", server_port), BrowserRedirectHandler)

    # Open web browser to get ID-porten authorization token.
    webbrowser.open(authorize_uri)

    # Wait for callback from ID-porten
    server.timeout = server_timeout
    start_time = time.time()
    while not hasattr(BrowserRedirectHandler.result, "path"):
        server.handle_request()
        if time.time() - start_time > server.timeout:
            server.server_close()
            sys.exit("Wrong identity towards id porten.")

    # Free the port, no more callbacks expected
    server.server_close()
    print("Authorization token received")

    # result.path is now "/token?code=...&state=...".
    # We must verify that state is identical to what we sent.
    # ref: https://tools.ietf.org/html/rfc7636
    parsed_response = urlparse(BrowserRedirectHandler.result.path)
    query_string = parsed_response.query
    query_state = parse_qs(query_string)

    print("State was " + state)
    print(f"Query state length is {len(query_state['state'])}")
    print(f"Query state is {query_state['state'][0]}")
    assert len(query_state["state"]) == 1 and query_state["state"][0] == state

    # Use the authorization code to get access and id token from /token
    payload = {
        "grant_type": "authorization_code",
        "code_verifier": pkce_secret,
        "code": query_state["code"][0],
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "scope": scope,
    }
    headers = {"Accept": "application/json"}

    # Connecting to the /token endpoint.
    response = requests.post(
        f"https://{auth_domain}/token", headers=headers, data=payload
    )
    if response.status_code != 200:
        print(response.status_code)
        print(response.json())
        response.raise_for_status()
    auth_result = response.json()
    access_token = auth_result["access_token"]
    id_token = auth_result["id_token"]
    assert auth_result["token_type"] == "Bearer"

    # Get the jwks from id porten (for token verification later)
    jwks = get_jwks()
    public_certs = load_public_certs(jwks["keys"][0]["x5c"])
    public_key = public_certs[0].public_key()

    # Validate tokens, ref: https://tools.ietf.org/html/rfc7519#section-7.2
    jwt.decode(
        auth_result["id_token"],
        public_key,
        algorithms=ALGORITHMS,
        issuer=f"https://{auth_domain}/",
        audience=client_id,
        access_token=access_token,
    )
    id_token_encoded = id_token.split(".")[1]
    id_token_decoded = json.loads(
        urlsafe_b64decode(id_token_encoded + "==").decode()
    )
    assert id_token_decoded["nonce"] == nonce

    # Validate the access token, this is what we have to pass on to the APIs.
    jwt.decode(
        access_token,
        public_key,
        algorithms=ALGORITHMS,
        issuer=f"https://{auth_domain}/",
    )

    access_token_encoded = access_token.split(".", 3)[1]
    access_token_decoded = json.loads(
        urlsafe_b64decode(access_token_encoded + "==").decode()
    )

    # Validations for access token
    assert access_token_decoded["client_id"] == client_id
    assert access_token_decoded["token_type"] == "Bearer"
    assert access_token_decoded["acr"] in ["Level3", "Level4"]

    token_expiration = access_token_decoded["exp"] - int(time.time())
    print(f"Token validated, expires in {token_expiration} seconds.")
    print(f"\nBearer {access_token}\n")

    return {"Authorization": f"Bearer {access_token}"}
