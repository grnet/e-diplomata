# ediplomas

This project is an implementation of the protocol Diplomata. The implementation consists of two services, one is used by the ISSUER and the other one is used by the HOLDER and VERIFIER.

## ediplomas folder structure

The folder "apps" contains the frontend implementation of the services. 
The folder "libs\blockchain" contains the library that it will be used to interact with the Blockchain network and execute transactions.
The folder "servers\issuer-server" contains the backend implementation of the services.

## add a package dependency and update packages

To update package.json files make the desired modifications to package.json and then execute the command rush update.