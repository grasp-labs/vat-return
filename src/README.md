# How to use the code
This is a guide on how to use the code provided.
````text
vat_return_client
    - example_files (Files used in example_mva_innsending.py)
    - client.py (The client code towards Vat return)
    - example_mva_innsending.py (Example script of the process meant for testing with test users)
    - get_id_porten_token.py (Log-in process with id-porten)
    - settings.py (Defining urls for requests in the code base)
````
## How to use example_mva_innsending.py
The example_mva_innsending.py is just an example of using the vat client,
it cant be runned towards prod environment directly.

### Overview:
If testing:
- Configure test user, make a note of its organization number and the user id.
- Set Environment variables
````shell
set ORG_NUMBER=...
````
- Update the example_files for envelope and message to have correct org number.

If you don't, you will encounter a validation error. 
If you are curious about the outcome, you may choose to proceed without changes,
or add mistakes to the files.
- Run the program.

### Creating a test user
Information is found [here](https://skatteetaten.github.io/mva-meldingen/mvameldingen_eng/test/)

The guide for Tenor test users are [here](https://github.com/Skatteetaten/mva-meldingen/blob/master/docs/mvameldingen_eng/test/User_Guide_Tenor_testdata.pdf)

You have to login to ID porten using your own credentials. It's a free and open
service protected by the login. You dont need any roles etc. to do this.

Following the guide and given that you have a Norwegian ID you can start [here](https://www.skatteetaten.no/skjema/testdata/)

If you don't have a Norwegian ID you will start [here](https://docs.digdir.no/docs/idporten/idporten/idporten_testbrukere.html)

It's all covered in the guide for Tenor test users.

### Running the program
````shell
cd vat-return
pipenv install --dev
cd src/vat_return_client
pipenv run python example_mva_innsending.py
````

## How to run it in production
Make your own version of the script in example_mva_innsending.py
that have the correct files for submission set up.

Set environment variables.
This will modify settings.py to point toward prod endpoints.
````shell
set BUILDING_MODE=prod
set CLIENT_ID=...
set REDIRECT_URI=...
set SERVER_PORT=...
set ORG_NUMBER=...
````

Run your script.

In production, remove the print statements in get_id_porten_token.py
