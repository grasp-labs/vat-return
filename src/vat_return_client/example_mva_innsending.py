import os

from client import VatReturn
from get_id_porten_token import get_id_token

ORG_NUMMER = "310332313"  # The org number for our test user.


def get_example_files(file_name: str):
    from pathlib import Path
    path = Path(__file__).parent / "example_files" / file_name
    with open(path, "r", encoding="UTF-8") as file:
        melding = file.read()
        vat = melding.replace("\n", "")

    return vat


def get_appendix(file_name: str):
    from pathlib import Path
    path = Path(__file__).parent / "example_files" / file_name
    with open(path, "rb") as file:
        return file.read()


def vat_return_process():
    token = os.environ.get("ID_PORTEN_TOKEN", None)
    if token:
        id_porten_token_header = {"Authorization": token}
    else:
        id_porten_token_header = get_id_token()

    vat_client = VatReturn(
        id_porten_auth_headers=id_porten_token_header
    )
    vat_client.set_altinn_token()
    vat_message_delivery_filename = "message/compensation_vat_message.xml"
    mva_message = get_appendix(file_name=vat_message_delivery_filename)
    print("---- Validating -----")
    validation = vat_client.validate_tax_return(body=mva_message)
    print(validation)

    print("---- Creating Instance -----")
    instance = vat_client.create_instance(organization_number=ORG_NUMMER)
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
    vat_appendix = get_appendix("appendix/vat_appendix.xml")
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
    vat_return_process()
