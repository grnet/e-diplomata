# Verifier-server app

Backend server that communicates with two services, the one created for the Verifier and the other one created for Verifier and Verifier.
The backend server interacts with the blockchain using the library in the folder [libs\blockchain](https://gitlab.grnet.gr/devs/priviledge/ediplomas/-/tree/master/libs/blockchain).
Ganache-cli is used to create a local blockchain network. The application can be adjusted to interact with a public testnet blockchain, like the Ethereum Ropsten Testnet.
For now in the following section "Getting started" you can find information on how to start a local blockchain network with ganache-cli, that can be used during the development stage of the server.

## Verifier-server folder structure

The folder path 'pages/api' contains the pages for the api request that one can send to the server. In pages/api/blockchain one can request and execute the
corresponding functions in "index.ts", inside the folder [libs\blockchain](https://gitlab.grnet.gr/devs/priviledge/ediplomas/-/blob/master/libs/blockchain/src/index.ts).

## Getting started

We start Verifier-server server:

```
rushx dev
```

and then in a new terminal we start ganache

```
rushx ganache
```

and then access the service by posting an api request to a page in localhost:4000.

## Code Example

An example of an api call to execute the deploy function of the smart contract is by accessing the following request url
"http://localhost:4000/api/blockchain/deploy/".