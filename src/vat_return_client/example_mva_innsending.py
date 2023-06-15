"""
This is an example on how to run the vat submission process.
We have created a test user (required to do):
- Organization number: 310332313
- Test-id: 04815398780 (Used to log in to id-porten)

Ref:
Create test users - https://skatteetaten.github.io/mva-meldingen/kompensasjon_eng/test/
"""
import os

from client import VatReturn
from get_id_porten_token import get_id_token
from settings import (
    ALTINN_BASE,
    VALIDATION_BASE,
    INSTANCE_API_URL,
    ORG_NUMBER,
)


def get_example_files(file_name: str, read_bytes: bool = False):
    from pathlib import Path
    path = Path(__file__).parent / "example_files" / file_name
    if read_bytes:
        with open(path, "rb") as file:
            return file.read()

    with open(path, "r", encoding="UTF-8") as file:
        melding = file.read()
        return melding.replace("\n", "")


def vat_return_process(org_number: str):
    token = os.environ.get("ID_PORTEN_TOKEN", None)
    if token:
        id_porten_token_header = {"Authorization": token}
    else:
        id_porten_token_header = get_id_token()

    vat_client = VatReturn(
        id_porten_auth_headers=id_porten_token_header,
        altinn_environment=ALTINN_BASE,
        id_porten_environment=VALIDATION_BASE,
        instance_api_url=INSTANCE_API_URL,
    )
    vat_client.set_altinn_token()
    vat_message_delivery_filename = "message/compensation_vat_message.xml"
    mva_message = get_example_files(file_name=vat_message_delivery_filename, read_bytes=True)
    print("---- Validating -----")
    validation = vat_client.validate_tax_return(body=mva_message)
    print(validation)

    print("---- Creating Instance -----")
    instance = vat_client.create_instance(organization_number=org_number)
    instance_url = instance["selfLinks"]["apps"]
    instance_data_url = instance["data"][0]["selfLinks"]["apps"]

    print("---- Update Vat Submission -----")
    vat_message_delivery_filename = "envelope/compensation_vat_envelope.xml"
    envelope = get_example_files(file_name=vat_message_delivery_filename)
    upload_vat_submission = vat_client.upload_vat_submission(
        instance_data_app_url=instance_data_url, content=envelope
    )
    print("---- Update Vat Message -----")
    upload_vat_return = vat_client.upload_vat_return(
        instance_url=instance_url, content=mva_message
    )

    print("---- Upload Attachments -----")
    vat_appendix = get_example_files("appendix/vat_appendix.xml", read_bytes=True)
    upload_attachment = vat_client.upload_attachments(
        instance_url=instance_url,
        content_type="text/xml",
        file_name="vat_appendix.xml",
        content=vat_appendix,
    )
    print("---- Complete Data Filling -----")
    complete_data_filling = vat_client.ship_to_next_process(
        instance_url=instance_url
    )

    print("---- Complete Vat Submission -----")
    complete_vat_submission = vat_client.ship_to_next_process(
        instance_url=instance_url
    )

    print("---- Check Feedback Status -----")
    feedback = vat_client.retrieve_feedback(instance_url=instance_url)
    print(feedback)


if __name__ == "__main__":
    """
    Running the process of Vat Return.
    If you want to avoid logging in to id porten, set the environment
    variable ID_PORTEN_TOKEN=Bearer <id porten token>.
    """
    vat_return_process(org_number=ORG_NUMBER)
