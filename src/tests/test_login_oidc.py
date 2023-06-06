from unittest import TestCase
import os

from vat_return_client._utils import oidc_authorize, QueryParamsAuthorize


class OidcTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        authorize_params = {
            "client_id": os.environ.get("_CLIENT_ID"),
            "redirect_uri": "https://www.skatteetaten.no",  # TODO: This one is defined in the integration and need to be ther ERP's desired landing.
            "response_type": "code",
            "code_challenge": os.environ.get("_CODE_CHALLENGE"),
        }
        cls.auth_model = QueryParamsAuthorize(**authorize_params)

    def test_login(self):
        print(self.auth_model.get_query_params())
        login = oidc_authorize(
            authorize_params=self.auth_model
        )
