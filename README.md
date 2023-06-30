# VAT Return Client
The VAT Return client, written in Python, serves as a practical demonstration
of how to streamline the VAT submission process with Skatteetaten 
(Norwegian Tax Administration) by leveraging their API. This client offers a 
codebase that enables connectivity to the Altinn API, allowing automated 
submission of VAT registration data on behalf of users. 
It takes care of the steps of authentication and authorization, ensuring that
the API requests are made with the appropriate requirements.
The client is intended as a building block that can be extended and integrated 
into other projects.

## Process
Firstly, if you are a developer who is testing the APIs to build your own 
codebase, please refer to the 'src/README.md' file for detailed instructions.

Additionally, it is advisable to initiate the following processes early 
as they may require a considerable amount of time to complete.

1. Start using ID-porten<br>
To begin using ID-porten, initiate the process by contacting DigDir to gain 
access to Samarbeidsportalen, where you can create integrations. This can be 
done by submitting an information schema to DigDir. Keep in mind that this 
process may take a few calendar days to complete, so it is good to start early.
You can find more information and start the process 
[here](https://samarbeid.digdir.no/id-porten/ta-i-bruk-id-porten/94).

2. Grant access to set up an integration.
- Log in to altinn.no with your credentials, you will need the role "Hovedadministrator."
- Choose the organization to represent.
- Go to "Profile."
- Select "Andre med rettigheter til virksomheten."
- Search for the person using their social security number and last name, whom you want to give access to.
- Search for "Maskinporten"; you should have three choices.
- Add (by clicking the + sign) "selvbetjening av integrasjoner i ID-porten/Maskinporten."
- Go to the next step -> Grant access -> complete.
- Continue to set up integration.

3. Set up integration<br>
Once you have access to Samarbeidsportalen, proceed with setting up the 
integration. In the setup for the VAT return, ensure that the following scopes 
are included in the Difi-tjeneste: API-klient.
- openid
- skatteetaten:mvameldingvalidering
- skatteetaten:mvameldinginnsending

If these scopes are not available, you will need to request them from 
mva-modernisering@skatteetaten.no, in the email, include the requested scopes 
for access and your organization number. Please note that obtaining these scopes
may also require additional calendar time.

- Log in at the top right [here](https://samarbeid.digdir.no/)
- Go to "integrations" tab -> self-service (Selvbetjening)
- Click on "integration" in the Production settings
- Log in again using credentials for the samarbeidsportalen.
- Log in again using "ID-porten." For Norwegian citizens, this typically
involves the "BankID" verification process. For non-Norwegian citizens,
this step is a black box.

See [here](https://skatteetaten.github.io/mva-meldingen/english/idportenauthentication/)
for official documentation on setting up integrations, and [here](https://learn.microsoft.com/en-us/dynamics365/business-central/localfunctionality/norway/norwegian-vat-reporting)
for an example given by Microsoft.

4. Use vat return client<br>
If the above steps are successful, you should be able to use and/or modify
the client provided. see src/README.md for more info on our assumptions.

## The OpenID Connect (OIDC) flow and its parties.
1. Client Registration (You + Samarbeidsportalen)<br>
The client application (This is you) need to be registered with the identity 
provider (IDP) providing the required detials such as *redirect uri*, and get 
a client id + client secret. This is done by creating an integration in 
Samarbeidsportalen.
2. Resource server (altinn)<br>
Altinn hosts protected resources that the client application wants to access
on behalf of end users. Before using the resources (VAT submission),
the client must exchange the access token from ID porten (see below)
with an access token from altinn.
3. Identity Provider / Authentication Server (ID porten login with BankID)<br>
ID porten acts as the authorization server responsible for handling the
authentication and authorization process. IT verifies the identity of the 
end user and issues access tokens and ID tokens to the client application.<br>
To begin with, ID-porten employs the /authorize endpoint to verify the user's 
identity and determine the client application being utilized. Upon successful 
verification, ID-porten generates a code for authorizing the subsequent request.
This code is used in the authorization process.<br>
Furhtermore, ID-porten employs the /token endpoint to determine whether the 
client application has the necessary authorization to access protected 
resources on behalf of the user.<br>
Upon successful evaluation, the authentication server (ID-porten) grants, among
other, access token and an id token to the client application. The access token
retrieved from ID-porten will be used in subsequent request for the VAT submission.<br>
This process is implemented in get_id_porten_token.py. Where verification on the 
request to the /authorize endpoint is compared with the one from the /token 
endpoint.
4. Access Control Provider (Skattettaten)<br>
Altinn is responsible for managing and granting access to specific resources 
within the resource server. It ensure that the client application and the end 
user have the necessary permissions to access the requested resources. (Scopes 
and end user's altinn roles)
5. Certificate Provider (Commfides or Bypass)<br>
Commfides or Bypass provides certificates that can be used by the client for 
authentication if this is chosen as the authentication process. The implementation of 
get_id_porten_token.py supports None and client_secret_post methods, which 
are determined during client registration in Samarbeidsportalen.
Certificates are named 'Enterprise certificate' in the altinn docs.

So in summary:
- Make sure your organization have made the scopes available for the Digdir
service 'API-klient'.
````text
- openid
- skatteetaten:mvameldingvalidering
- skatteetaten:mvameldinginnsending
````
- Grant access to set up an integration (if production).
- Set up the integration.
- Launch the Vat Return Client in the client application.
- The one who is starting the VAT Submission need one of the following Altinn roles:
````text
- Ansvarlig revisor
- Regnskapsmedarbeider
- Regnskapsfører uten signeringsrett
- Revisormedarbeider
````
- The user who completes the submission must have one of the following Altinn roles:
````text
- Begrenset signeringsrett
- Kontaktperson NUF (does not apply to tax return for VAT compensation)
- Regnskapsfører med signeringsrett
````
If there is any issues with the roles provided to the user, altinn will respond with 403 status code.
If there is an authentication failure, altinn will respond 401.


## The user process
This will vary depending on how you set this up, but following the general 
recommendation the process will be:

Supplier:
- The supplier set up an integration.
- Submission follows the given steps, take a note on the roles required there.
- When the supplier submit, it has to log-in using ID-porten.
- After log in, the supplier can start the process of submission.

Implementation guide is found [here](https://skatteetaten.github.io/mva-meldingen/english/implementationguide/#6-send-vat-return-to-the-tax-administrations-submission-api)

Customer:
- Delegate required permission to the supplier in altinn.
## References
In our development we have used these main pages for documentation:

[System Submission of VAT-report](https://skatteetaten.github.io/mva-meldingen/frontpage_eng/)
 Here is all the information needed, its in a hierarchy, and you will need to click 
your way down.

It all starts with ID porten, that is documented [here](https://skatteetaten.github.io/mva-meldingen/documentation/idportenautentisering/#bestilling-av-scopes)
for the VAT submission and technical docs are [here](https://docs.digdir.no/docs/idporten/idporten/idporten_overordnet.html)

This is the [Reference code](https://github.com/Skatteetaten/mva-meldingen/tree/master)
 we have used as inspiration.
