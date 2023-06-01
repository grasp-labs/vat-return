# VAT Return Client
The VAT Return client, written in Python, serves as a practical demonstration
of how to streamline the VAT registration process with Skatteetaten 
(Norwegian Tax Administration) by leveraging their API. This client offers a 
codebase that enables connectivity to the Altinn API, allowing automated 
submission of VAT registration data on behalf of users. 
It takes care of the steps of authentication and authorization, ensuring that
the API requests are made with the appropriate requirements. Additionally, 
the client provides users with feedback on the registration status,
promptly displaying confirmation messages upon successful registration 
and promptly addressing any errors or issues with informative error messages. 
The client can also serve as a building block 
that can be extended and integrated into other projects.

## Process

1. Start using ID-porten<br>
To begin using ID-porten, initiate the process by contacting DigDir to gain 
access to Samarbeidsportalen, where you can create integrations. This can be 
done by submitting an information schema to DigDir. Keep in mind that this 
process may take a few calendar days to complete, so it is good to start early.
You can find more information and start the process 
[here](https://samarbeid.digdir.no/id-porten/ta-i-bruk-id-porten/94).

2. Set up integration<br>
Once you have access to Samarbeidsportalen, proceed with setting up the 
integration. In the setup for the VAT return, ensure that the following scopes 
are included in the Difi-tjeneste: API-klient:
- openid
- skatteetaten:mvameldingvalidering
- skatteetaten:mvameldinginnsending

If these scopes are not available, you will need to request them from 
mva-modernisering@skatteetaten.no. Please note that obtaining these scopes may 
also require additional calendar time.

3. Using Maskinporten as a login option<br>
Depending on your specific requirements, there are different login strategies 
available. One approach is to use Maskinporten to access the 
ID-porten token, which can then be exchanged for an Altinn token.

**Further guidance on best practices will be provided after completing the on-going
process with Skatteetaten.**
Based on our current understanding, it is recommended that you order a 
'virksomhetssertifikat' and grant permission to a user.
You can order the certificate from either Buypass or Comfides.
Remember you will need a test certificate and a production certificate.
4. Use client<br>
If the above steps are successful, you should be able to use and/or modify
the client provided.

We assume that structuring the messages to the 
[xsd](https://github.com/Skatteetaten/mva-meldingen/tree/master/docs/informasjonsmodell_filer/xsd)
models are in place from the source. Functionality to validate is in place.

## Usage
### Environemnt Variables
Set the following environment varialbes as paths to files:
````shell
SET VIRKSOMHETSSERTIFIKAT_KEY=C:\....pem
SET PRIVATE_KEY=C:\....pem
SET ENV_FILE=C:\...\.env
````

### The ENV FILE
To use the client directly, you will need to create a file named .env in a 
directory.
````text
USERNAME='value'
PASSWORD='value'
API_KEY='value'
CLIENT_ID='value'
SCOPE_TEST='value'
````
To configure the client correctly, open the .env file and replace 'value' with 
the actual value provided to you. Ensure that you remove any hyphens present 
and add the corresponding key for the variable. This file serves as a 
configuration file, storing the necessary environment variables for the client 
to function properly. 

### The Certificate and the private key
Create a private.pem file containing your private key.
````text
-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
````
Create a virksomhetssertifikat.pem containing your certificate.
````text
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
````
