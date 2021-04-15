# Blockchain Library

Typescript library for executing functions of a smart contract published in Ethereum blockchain network. The code structure of the smart contract should be like the smart contract in the file 'Certific.sol', contained in this project. The library uses ['ether.js']('https://github.com/ethers-io/ethers.js') to communicate with Ethereum blockchain. The methods of the smart contract are implemented for the Diplomata Protocol, so one should refer to the description of the protocol for more detailed explanation of the input parameters in the functions.

## Methods

The methods deployContract, publishAward, publishProof are used by the Issuer service and the methods publishRequest, PublishAck, PublishFail are used by the Holder and Verifier service.

### Methods used by the Issuer service
--------------------------------------
**deployContract**

Deploy an instance of 'Certific.sol' smart contract to Ethereum blockchain. The function executes the function deploy of the smart contract. After the transcaction is mined, the function returns the transactionHash and the Ethereum address of the smart contract instance. Every Issuer deploys an instance of 'Certific.sol' once and then refers to it using its Ethereum address.

**publishAward**

Publish an award request to Ethereum blockchain. The function executes the method award of the smart contract. The input parameters hashOfAwardFirstPart and hashOfAwardSecondPart hold the ElGamal encryption of the cryptographically secure hash of content  QUALIFICATION t. The parameter contractAddressUsedByIssuer holds the smart contract address that will refer to, in order to execute its method deploy. After the transcaction is mined, the function returns the transaction hash.

**publishProof**

Publish a proof request to Ethereum blockchain. The function executes the method proof of the smart contract. The input parameter sReq holds a value that indicates that an Ethereum address has signed and published a transaction to the blockchain. This transaction was produced when a publishRequest function was executed. So sReq is a transaction hash. The parameters c, c2 hold the ElGamal re-encryption of the cryptographically secure hash of content QUALIFICATION t. The parameter nirence hold, a non-interactive (Fiat-Shamir) proof of reencryption of ciphertext c to c' (for more information of c and c' one should refer to the refer to the protocol of the protocol Diplomata), using the Chaum-Pedersen protocol. The parameter v holds a value that it was previously produced from an encryption scheme wherein entities are identified by their ElGamal keys. The parameter contractAddressUsedByIssuer holds the smart contract address that will refer to, in order to execute its method proof. After the transcaction is mined, the function returns the transaction hash.

### Methods used by the Holder and Verifier service
---------------------------------------------------
In the following functions, there is no need to specify the smart contract address that will be used for interacting with the smart contract because the service interacts with only one contract that the Issuer had deployed to the Ethereum and uses.

**publishRequest**

Publish a request for proof to Ethereum blockchain. The function executes the method request of the smart contract and executes a transaction with the Blockchain. The input parameter sAwd holds a value that indicates that an Ethereum address has signed and published a transaction to the blockchain. This transaction was produced when a publishAward function was executed. So sAws is a transaction hash. The parameters VerifKeyPart1, VerifKeyPart2, VerifKeyPart3, VerifKeyPart4 hold the value of the ElGamal public key, which we suppose is 1024 bits long, by which the Verifier is specified. After the transcaction is mined, the function returns the transaction hash.

**publishAck**

Publish an acknowledgement to Ethereum blockchain that the Verifier has received and verified the certificate. The function executes the method ack of the smart contract and executes a transaction with the Blockchain. The input parameter sPrf holds a value that indicates that an Ethereum address has signed and published a transaction to the blockchain. This transaction was produced when a publishProof function was executed. So sPrf is a transaction hash. The parameter eI holds a value that it was previously produced from an encryption scheme wherein entities are identified by their ElGamal keys. After the transcaction is mined, the function returns the transaction hash.

**publishFail**

Publish an acknowledgement to Ethereum blockchain that the Verifier has failed to receive and verify the certificate. The function executes the method fail of the smart contract and executes a transaction with the Blockchain. The input parameter sPrf holds a value that indicates that an Ethereum address has signed and published a transaction to the blockchain. This transaction was produced when a publishProof function was executed. So sPrf is a transaction hash. After the transcaction is mined, the function returns the transaction hash.

## Running the tests

To run the tests you need a live blockchain network where the transactions will be published. To create one with ganache-cli open a terminal and execute the following commands:

```
cd ..\..\servers\issuer-server\
rushx ganache
```
Now that the blockchain network is set you can run the tests. Open a new terminal and execute the following commands:
```
rushx test
```