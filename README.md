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
First of all, if you are a developer that is testing the API's to develop
your own codebase, redirect to src/README.md.
Still, it's smart to start the following processes as they can take some
calendar time.

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

See [here](https://skatteetaten.github.io/mva-meldingen/english/idportenauthentication/)
for official documentation on setting up integrations, and [here](https://learn.microsoft.com/en-us/dynamics365/business-central/localfunctionality/norway/norwegian-vat-reporting)
for an example given by Microsoft.

4. Use vat return client<br>
If the above steps are successful, you should be able to use and/or modify
the client provided. see src/README.md for more info on our assumptions.

## The user process
This will vary depending on how you set this up, but following the general 
recommendation the process will be:

Supplier:
- The supplier set up an integration.
- Submission follows [these] steps, take a note on the roles required there.
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
for the VAT submission
and technical docs are [here](https://docs.digdir.no/docs/idporten/idporten/idporten_overordnet.html)

This is the [Reference code](https://github.com/Skatteetaten/mva-meldingen/tree/master)
 we have used as inspiration.
