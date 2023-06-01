"""Module to test and verify client.py"""
from unittest import TestCase
from vat_return_client import VatReturn, get_maskinporten_token, config


class VatReturnTestCase(TestCase):
    """Test case for VatRetrun class."""

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test_something(self):
        """Temp test to try out functionality."""
        id_porten_token = get_maskinporten_token(
            client_id=config.client_id,
            virksomhetssertifikat=config.virksomhetssertifikat,
            scope=config.scope_test,
            private_key=config.private_key,
        )
        client = VatReturn(
            id_porten_token=id_porten_token["access_token"],
            username=config.username,
            password=config.password
        )
        client.set_altinn_token()
