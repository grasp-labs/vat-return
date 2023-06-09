"""
Module to store settings required for the program to run.
ref: https://skatteetaten.github.io/mva-meldingen/kompensasjon_eng/test/
"""
import os

BUILDING_MODE = os.environ.get("BUILDING_MODE", "test")

# Environments / Domains
ID_PORTEN_BASE = "oidc.difi.no" if BUILDING_MODE == "prod" else "oidc-ver2.difi.no"
ID_PORTEN = "idporten.no" if BUILDING_MODE == "prod" else "test.idporten.no"  # To be changed with ID_PORTEN_BASE.
ALTINN_BASE = "https://platform.altinn.no" if BUILDING_MODE == "prod" else "https://platform.tt02.altinn.no"
VAT_BASE = "skd.apps.altinn.no" if BUILDING_MODE == "prod" else "skd.apps.tt02.altinn.no"
VALIDATION_BASE = "idporten.api.skatteetaten.no" if BUILDING_MODE == "prod" else "idporten-api-sbstest.sits.no"
SUBMISSION_PATH_ENV = "v1" if BUILDING_MODE == "prod" else "etm2"

# URLS
ID_PORTEN_AUTH_DOMAIN = f"{ID_PORTEN_BASE}/idporten-oidc-provider"
ID_PORTEN_JWK_URL = f"https://{ID_PORTEN_BASE}/.well-known/openid-configuration"
VALIDATION_SERVICE = f"https://{VALIDATION_BASE}/api/mva/grensesnittstoette/mva-melding/valider"
ALTINN_TOKEN_EXCHANGE_URL = f"{ALTINN_BASE}/authentication/api/v1/exchange/id-porten"
SUBMISSION_SERVICE = f"https://{VAT_BASE}/skd/mva-melding-innsending-{SUBMISSION_PATH_ENV}"
INSTANCE_API_URL = f"{SUBMISSION_SERVICE}/instances"

# Settings for get_id_porten_token.py
# The following attributes are decided by your integration setup.
ID_PORTEN_CLIENT_ID = os.environ.get("CLIENT_ID", "23cc2587-ea4e-4a5f-aa5c-dfce3d6c5f09")
ID_PORTEN_CLIENT_SECRET = os.environ.get("CLIENT_SECRET", None)
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:12345/token")
SERVER_PORT = int(os.environ.get("SERVER_PORT", 12345))
CLIENT_AUTHENTICATION_METHOD = os.environ.get("CLIENT_AUTHENTICATION_METHOD", None)
SERVER_TIMEOUT = os.environ.get("SERVER_TIMEOUT", 1000)

# These are constants and should not be changed.
ALGORITHMS = ["RS256"]
SCOPES = "openid skatteetaten:mvameldingvalidering " \
         "skatteetaten:mvameldinginnsending "

# Settings for example_mva_innsending.py
ORG_NUMBER = os.environ.get("ORG_NUMBER", "310332313")
