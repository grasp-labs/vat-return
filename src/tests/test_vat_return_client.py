"""Config test module."""
from unittest import TestCase, mock

import vat_return_client as vrc


class Client(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test_login(self):
        token = vrc.get_id_token(
            client_id=vrc.config.client_id,
            scope=vrc.config.scope,
        )
        print(token)



