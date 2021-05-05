import { ethers } from 'ethers';
import {
  Bytecode,
  CERTIFICATE_ABI
} from './contracts/Certificv2';

const { Contract, utils, ContractFactory } = ethers;
export type ProviderConfig = {
  provider: ethers.providers.Provider | ethers.providers.JsonRpcProvider;
  account: ethers.Wallet | ethers.providers.JsonRpcSigner;
  address: string;
}

// deployContract
export interface DeployContractInputInterface {
  accountIssuer: ProviderConfig["account"];
}

export interface DeployContractOutputInterface {
  contractAddress: string;
  tranHash: string;
}

// publishAward
export interface PublishAwardInputInterface {
  hashOfAwardFirstPart: string;
  hashOfAwardSecondPart: string;
  contractAddressUsedByIssuer: string;
  provider: ProviderConfig["provider"];
  accountIssuer: ProviderConfig["account"];
  addressIssuer: ProviderConfig["address"];
}

/* publishProof
   the names of the variables are the same as the ones used in the protocol
   and are defined in d4.2
*/
export interface PublishProofInputInterface {
  contractAddressUsedByIssuer: string;
  sReq: string;
  c: string;
  c2: string;
  nirenc: string;
  ev: string;
  provider: ProviderConfig["provider"];
  accountIssuer: ProviderConfig["account"];
  addressIssuer: ProviderConfig["address"];
}

// publishAward and publishProof
export interface PublishAwardOutputInterface {
  transactionHash: string;
}

/* Holder-Verifier-Service
    publishRequest
    the variables VerifKeyPart1,VerifkeyPart2,VerifkeyPart3,VerifkeyPart4 hold
    the Verifier's ElGamal public key which we suppose is 1024bits
    Each variable in BC can hold up to 256bits so we need 4 
    variables to save the key
    the variable sawd is the one defined in d4.2
*/
export interface PublishRequestInputInterface {
  contractAddressUsedByIssuer: string;
  sAwd: string;
  VerifKeyPart1: string;
  VerifKeyPart2: string;
  VerifKeyPart3: string;
  VerifKeyPart4: string;
  provider: ProviderConfig["provider"];
  accountHolder: ProviderConfig["account"];
  addressHolder: ProviderConfig["address"];
}

export interface PublishAckInputInterface {
  contractAddressUsedByIssuer: string;
  sPrf: string;
  eI: string;
  provider: ProviderConfig["provider"];
  accountVerifier: ProviderConfig["account"];
  addressVerifier: ProviderConfig["address"];
}

export interface PublishFailInputInterface {
  contractAddressUsedByIssuer: string;
  sPrf: string;
  provider: ProviderConfig["provider"];
  accountVerifier: ProviderConfig["account"];
  addressVerifier: ProviderConfig["address"];
}

const deployContract = async (inputDeploy : DeployContractInputInterface) : Promise<DeployContractOutputInterface> => {
  let newContract = new ContractFactory(CERTIFICATE_ABI, Bytecode, inputDeploy.accountIssuer);
  const contract = await newContract.deploy();
  console.log('contract address', contract.address);
  /* wait for contract creation transaction to be mined
     Important
     what if we have an error? How much time should we await if not mined?
     maybe use try catch..
  */
  let receipt = await contract.deployTransaction.wait();
  return {
    contractAddress: receipt.contractAddress,
    tranHash: receipt.transactionHash
  };
}

const publishAward = async (inputAward: PublishAwardInputInterface)
  : Promise<PublishAwardOutputInterface> => {
  // pass a provider when initiating a contract for read only queries
  let conInstance = new Contract(
    inputAward.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputAward.provider
  );
  let contract_owner = await conInstance.getOwner();
  console.log(contract_owner);
  //Call award function
  let conInstanceAw = new Contract(
    inputAward.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputAward.accountIssuer
  );
  //estimateGas
  let gasPrice = utils.parseUnits('10', 'gwei').toNumber();
  let gas = await conInstanceAw.estimateGas.award(
    inputAward.hashOfAwardFirstPart,
    inputAward.hashOfAwardSecondPart
  );
  const options = {
    gasLimit: gas, 
    gasPrice: gasPrice,
    from: inputAward.addressIssuer
  }
  let tx = await conInstanceAw.award(
    inputAward.hashOfAwardFirstPart,
    inputAward.hashOfAwardSecondPart,
    options
  );
  // wait for the transaction to be mined
  const receipt = await tx.wait();
  return { transactionHash: receipt.transactionHash };
}

const publishProof = async (inputProof: PublishProofInputInterface)
  : Promise<PublishAwardOutputInterface> => {
  /*Important!!! To be implemented - We should check if cAdd is correct.
    Maybe the Service has stored this address after deployment
    so it is not necessary for the Issuer to submit it
  */
  let conInstance = new Contract(
    inputProof.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputProof.provider
  );
  let contract_owner = await conInstance.getOwner();
  console.log(contract_owner);
  //Call proof function
  let conInstancePr = new Contract(
    inputProof.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputProof.accountIssuer
  );
  //estimateGas
  let gasPrice = utils.parseUnits('10', 'gwei').toNumber();
  let gas = await conInstancePr.estimateGas.proof(
    inputProof.sReq, inputProof.c, inputProof.c2, inputProof.nirenc, inputProof.ev
  );
  let options = {
    gasLimit: gas, 
    gasPrice: gasPrice,
    from: inputProof.addressIssuer
  }
  let tx = await conInstancePr.proof(
    inputProof.sReq, inputProof.c, inputProof.c2, inputProof.nirenc, inputProof.ev,
    options
  );
  // wait for the transaction to be mined
  const receipt = await tx.wait();
  return { transactionHash: receipt.transactionHash };
}

//* Holder-Verifier Service
const publishRequest = async (inputRequest: PublishRequestInputInterface)
  : Promise<PublishAwardOutputInterface> => {
  let conInstance = new Contract(
    inputRequest.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputRequest.provider
  );
  let contract_owner = await conInstance.getOwner();
  console.log(contract_owner);
  //Call request function
  let conInstanceReq = new Contract(
    inputRequest.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputRequest.accountHolder
  );
  //estimateGas
  let gasPrice = utils.parseUnits('10', 'gwei').toNumber();
  let gas = await conInstanceReq.estimateGas.request(
    inputRequest.sAwd,
    inputRequest.VerifKeyPart1,
    inputRequest.VerifKeyPart2,
    inputRequest.VerifKeyPart3,
    inputRequest.VerifKeyPart4
  );
  let options = {
    gasLimit: gas, 
    gasPrice: gasPrice,
    from: inputRequest.addressHolder
  }
  let tx = await conInstanceReq.request(
    inputRequest.sAwd,
    inputRequest.VerifKeyPart1,
    inputRequest.VerifKeyPart2,
    inputRequest.VerifKeyPart3,
    inputRequest.VerifKeyPart4,
    options
  );
  // wait for the transaction to be mined
  const receipt = await tx.wait();
  return { transactionHash: receipt.transactionHash };
}

const publishAck = async (inputAck: PublishAckInputInterface)
  : Promise<PublishAwardOutputInterface> => {
  let conInstance = new Contract(
    inputAck.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputAck.provider
  );
  let contract_owner = await conInstance.getOwner();
  console.log(contract_owner);
  //Call ack function
  let conInstanceAck = new Contract(
    inputAck.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputAck.accountVerifier
  );
  //estimateGas
  let gasPrice = utils.parseUnits('10', 'gwei').toNumber();
  let gas = await conInstanceAck.estimateGas.ack(
    inputAck.sPrf,
    inputAck.eI
  );
  let options = {
    gasLimit: gas, 
    gasPrice: gasPrice,
    //from we should specify verifiers ethereum key
    from: inputAck.addressVerifier
  }
  let tx = await conInstanceAck.ack(
    inputAck.sPrf,
    inputAck.eI,
    options
  );
  // wait for the transaction to be mined
  const receipt = await tx.wait();
  return { transactionHash: receipt.transactionHash };
}

const publishFail = async (inputFail: PublishFailInputInterface)
  : Promise<PublishAwardOutputInterface> => {
  let conInstance = new Contract(
    inputFail.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputFail.provider
  );
  let contract_owner = await conInstance.getOwner();
  console.log(contract_owner);
  //Call fail function
  let conInstanceFail = new Contract(
    inputFail.contractAddressUsedByIssuer, CERTIFICATE_ABI, inputFail.accountVerifier
  );
  //estimateGas
  let gasPrice = utils.parseUnits('10', 'gwei').toNumber();
  let gas = await conInstanceFail.estimateGas.fail(
    inputFail.sPrf
  );
  let options = {
    gasLimit: gas,
    gasPrice: gasPrice,
    //from we should specify verifiers ethereum key
    from: inputFail.addressVerifier
  }
  let tx = await conInstanceFail.fail(
    inputFail.sPrf,
    options
  );
  // wait for the transaction to be mined
  const receipt = await tx.wait();
  return { transactionHash: receipt.transactionHash };
}

export {
  deployContract,
  publishProof,
  publishAward,
  publishRequest,
  publishAck,
  publishFail
}
