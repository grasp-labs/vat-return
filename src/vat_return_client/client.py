"""
The VAT Return Client.
Reference:
- API: https://skatteetaten.github.io/mva-meldingen/english/api/
- Swagger: https://skd.apps.tt02.altinn.no/skd/mva-melding-innsending-etm2/swagger/index.html
- Environment list: https://skatteetaten.github.io/mva-meldingen/kompensasjon_eng/test/
"""
import time
from typing import Union, Dict

import requests


class VatReturn:
    """
    Client code. Before use, log into id porten and get the 'Id porten
    access token'.
    Set the appropriate altinn environment, defaults to test environment.
    Set the appropriate id porten environment, defaults to test environment.
    Set the instance api url appropriate for the environment, test as default.

    Url patterns:
    instance = create_instance(...)
    instance_url = instance["selfLinks"]["apps"]
    instance_data_url = instance["data"][0]["selfLinks"]["apps"]
    """

    def __init__(
            self,
            id_porten_auth_headers: Dict,
            altinn_environment: str,
            id_porten_environment: str,
            instance_api_url: str,
    ):
        self.id_porten_auth_headers = id_porten_auth_headers
        self.altinn_environment = altinn_environment
        self.id_porten_environment = id_porten_environment
        self.instance_api_url = instance_api_url
        self._altinn_token = None

    @property
    def altinn_token(self) -> str:
        return self._altinn_token

    @altinn_token.setter
    def altinn_token(self, token: str):
        self._altinn_token = token

    def set_altinn_token(self):
        """
        Exchanges the ID-porten token to a Altinn token. Sets the attribute
        altinn_token.

        :return: Json response.
        """
        exchange_token_url = (
            f"{self.altinn_environment}/authentication/api/v1/exchange/id-porten"
        )
        headers = self.id_porten_auth_headers
        headers["content-type"] = "application/json"
        response = requests.get(exchange_token_url, headers=headers)
        self.altinn_token = response.content.decode("utf-8")

    def validate_tax_return(self, body: bytes,) -> str:
        """
        Validates the content of a tax return and returns a response with
        any errors, deviations, and warnings.
        Checks the message format, and control the content and composition
        of the elements in the VAT return.

        :param body: According to XSD: https://github.com/Skatteetaten/mva-meldingen/blob/master/docs/informasjonsmodell_filer/xsd/no.skatteetaten.fastsetting.avgift.mva.skattemeldingformerverdiavgift.v1.0.xsd
        :return: Validation result as xml byte string.
        """
        validate_tax_return_url = (
            f"https://{self.id_porten_environment}/api/mva/grensesnittstoette/mva-melding/valider"
        )
        headers = self.id_porten_auth_headers
        headers["Content-Type"] = "application/xml"

        validate_response = requests.post(
            validate_tax_return_url, headers=headers, data=body
        )
        return validate_response.content.decode("utf-8")

    def create_instance(self, organization_number: str) -> Dict:
        """
        Creates an instance object in altinn. The instance will be used to
        populate information such as uploaded data, confirm and feedback.

        :param organization_number: Organization number.
        :return: Instance as dict.
        """
        headers = {
            "Authorization": f"Bearer {self.altinn_token}",
            "content-type": "application/json"
        }

        body = {
            "instanceOwner": {
                "organisationNumber": f"{organization_number}"
                }
        }
        response = requests.post(
            self.instance_api_url, headers=headers, json=body
        )
        return response.json()

    def upload_vat_submission(
            self, instance_data_app_url: str, content: str
    ) -> Dict:
        """
        Upload VAT return submission by using the data api for the instance.

        :param instance_data_app_url: Url to the data of the instance.
        :param content: Vat submission.
        :return: Data instance as dict.
        """
        headers = {

            "Authorization": f"Bearer {self.altinn_token}",
            "content-type": "application/xml"
        }
        response = requests.put(
            instance_data_app_url, headers=headers, data=content
        )
        return response.json()

    def upload_vat_return(self, instance_url: str, content: bytes) -> Dict:
        """
        Upload VAT return xml document to the instance.
        :param instance_url: Url to the instance.
        :param content: Vat message.
        :return: Data instance as dict.
        """
        headers = {
            "Authorization": f"Bearer {self.altinn_token}",
            "content-type": "text/xml",
            "Content-Disposition": "attachment; filename=mvaMelding.xml",
        }
        url = f"{instance_url}/data?datatype=mvamelding"
        response = requests.post(
            url, headers=headers, data=content
        )
        return response.json()

    def upload_attachments(
            self,
            instance_url: str,
            content_type: str,
            file_name: str,
            content: bytes,
    ) -> Dict:
        """
        It is possible to upload from 0 to 57 attachments, with an individual
        size of 25MB.
        The following content types are allowed for attachments:
        - text/xml
        - application/pdf
        - application/vnd.oasis.opendocument.formula
        - application/vnd.oasis.opendocument.text
        - application/vnd.oasis.opendocument.spreadsheet
        - application/vnd.oasis.opendocument.presentation
        - application/vnd.oasis.opendocument.graphics
        - application/vnd.openxmlformats-officedocument.wordprocessingml.document
        - application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
        - application/vnd.openxmlformats-officedocument.presentationml.presentation
        - application/msword
        - application/vnd.ms-excel
        - application/vnd.ms-powerpoint
        - image/jpeg
        - image/png

        :param instance_url: Url to the instance.
        :param content_type: Attachment content-type.
        :param file_name: Attachment filename with suffix (.pdf, .xml, ...)
        :param content: Attachment as bytes.
        :return: Data instance as dict.
        """
        url = f"{instance_url}/data?datatype=binaerVedlegg"
        headers = {
            "Authorization": f"Bearer {self.altinn_token}",
            "content-type": content_type,
            "Content-Disposition": f"attachment; filename={file_name}",
        }
        response = requests.post(
            url, headers=headers, data=content
        )
        return response.json()

    def ship_to_next_process(self, instance_url: str) -> Union[Dict, str]:
        """
        Move the instance to the next step for VAT return filing in the
        application process.

        :param instance_url: Url to the instance.
        :return: Process description as dict.
        """
        url = f"{instance_url}/process/next"
        headers = {
            "Authorization": f"Bearer {self.altinn_token}",
            "content-type": "application/json",
        }
        response = requests.put(
            url, headers=headers,
        )
        if response.status_code != 200:
            print(response)
            context = response.content.decode("utf-8")
            print(context)
            return context
        return response.json()

    def retrieve_feedback(
            self, instance_url: str, max_retry: int = 5, wait_time: int = 2
    ) -> Dict:
        """
        Return the instance when the Tax Administration has given feedback.

        - End user is waiting on feedback.
        - After the status-endpoint has returned isFeedbackProvided : true

        :param instance_url: Url to the instance.
        :param max_retry: How many time to retry.
        :param wait_time: How long to wait between requests.
        :return: Feedback as dict.
        """
        url = f"{instance_url}/feedback"
        headers = {
            "Authorization": f"Bearer {self.altinn_token}",
            "content-type": "application/json",
        }

        def recursive_check(count: int = 0):
            print("---- Requesting Feedback Status -----")
            if count > max_retry:
                return
            status_response = requests.get(f"{url}/status", headers=headers)
            is_feedback_provided = status_response.json()["isFeedbackProvided"]
            if not is_feedback_provided:
                time.sleep(wait_time)
                count += 1
                recursive_check(count=count)

        recursive_check()
        response = requests.get(url, headers=headers)
        return response.json()

    def get_feedback_files(self, instance_data_app_url: str) -> bytes:
        """
        Once the Tax Administration has given feedback, the files for the
        feedback can be downloaded from the instance.
        :param instance_data_app_url: URl to the file data app url.
        :return: Files as bytes.
        """
        headers = {
            "Authorization": f"Bearer {self.altinn_token}",
        }

        response = requests.get(instance_data_app_url, headers=headers)
        return response.content
