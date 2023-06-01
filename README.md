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

## Usage
### Setting secrets
To use the client directly, you will need to create a file named .env in the 
root directory with the following contents:
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

## Certificate and private key
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
