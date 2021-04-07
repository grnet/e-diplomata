import { ethers } from "ethers";
import {
  Bytecode,
  CERTIFICATE_ABI
} from "./contracts/Certificv2";

const { Contract, utils, ContractFactory } = ethers;
//gia ganache topika
const provider = new ethers.providers.JsonRpcProvider('http://localhost:8545');

/*
//gia INFURA
const network = "ropsten";
const provider = ethers.getDefaultProvider(network, {
    infura: `https://ropsten.infura.io/v3/${process.env.INFURA_ID}`,
    // Or if using a project secret:
    // infura: {
    //   projectId: YOUR_INFURA_PROJECT_ID,
    //   projectSecret: YOUR_INFURA_PROJECT_SECRET,
    // },
});
//const provider = new ethers.providers.InfuraProvider('ropsten');
const mysigner = new ethers.Wallet(`${process.env.ServiceIssuerPrivateKey}`);
const myaccount = mysigner.connect(provider);
*/

// deployContract
export interface DeployContractInterface {
  contractAddress: string;
  tranHash: string;
}
// publishAward
export interface PublishAwardInputInterface {
  hashOfAwardFirstPart: string;
  hashOfAwardSecondPart: string;
  contractAddressUsedByIssuer: string;
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
}
// publishAward and publishProof
export interface PublishAwardOutputInterface {
  transactionHash: string;
}

const deployContract = async (): Promise<DeployContractInterface> => {
  //If we use local Ganache local blockchain
  let myaccount = provider.getSigner(0);

  console.log(myaccount);
  // let gas = utils.hexlify(6721975);
  // let gasPrice = utils.parseUnits('10' , "gwei").toNumber();
  let newContract = new ContractFactory(CERTIFICATE_ABI, Bytecode, myaccount);
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
  //If we use local Ganache local blockchain
  let myaccount = provider.getSigner(0);
  console.log(myaccount);
  // pass a provider when initiating a contract for read only queries
  let conInstance = new Contract(
    inputAward.contractAddressUsedByIssuer, CERTIFICATE_ABI, provider
  );
  let contract_owner = await conInstance.getOwner();
  console.log(contract_owner);
  //Call award function
  let conInstanceAw = new Contract(
    inputAward.contractAddressUsedByIssuer, CERTIFICATE_ABI, myaccount
  );
  //estimateGas
  let gasPrice = utils.parseUnits('10', "gwei").toNumber();
  let gas = await conInstanceAw.estimateGas.award(
    inputAward.hashOfAwardFirstPart,
    inputAward.hashOfAwardSecondPart
  );
  console.log(gasPrice);
  let options = {
    gasLimit: gas, // Raise the gas limit to a much higher amount
    gasPrice: gasPrice,
    from: myaccount._address
    //from: myaccount.address //gia infura
  }
  let tx = await conInstanceAw.award(
    inputAward.hashOfAwardFirstPart,
    inputAward.hashOfAwardSecondPart,
    options
  );
  // wait for the transaction to be mined
  const receipt = await tx.wait();
  console.log(receipt);
  return { transactionHash: receipt.transactionHash };
}

const publishProof = async (inputProof: PublishProofInputInterface)
  : Promise<PublishAwardOutputInterface | string> => {
  /*Important!!! To be implemented - We should check if cAdd is correct.
    Maybe the Service has stored this address after deployment
    so it is not necessary for the Issuer to submit it
  */
  //If we use local Ganache local blockchain
  let myaccount = provider.getSigner(0);
  // pass a provider when initiating a contract for read only queries
  let conInstance = new Contract(
    inputProof.contractAddressUsedByIssuer, CERTIFICATE_ABI, provider
  );
  let contract_owner = await conInstance.getOwner();
  console.log(contract_owner);
  //Call award function
  let conInstancePr = new Contract(
    inputProof.contractAddressUsedByIssuer, CERTIFICATE_ABI, myaccount
  );
  //estimateGas
  let gasPrice = utils.parseUnits('10', "gwei").toNumber();
  let gas = await conInstancePr.estimateGas.proof(
    inputProof.sReq, inputProof.c, inputProof.c2, inputProof.nirenc, inputProof.ev
  );
  console.log(gas);
  let options = {
    gasLimit: gas, // Raise the gas limit to a much higher amount
    gasPrice: gasPrice,
    from: myaccount._address
    //from: myaccount.address
  }
  let tx = await conInstancePr.proof(
    inputProof.sReq, inputProof.c, inputProof.c2, inputProof.nirenc, inputProof.ev,
    options
  );
  // wait for the transaction to be mined
  const receipt = await tx.wait();
  console.log(receipt);
  return { transactionHash: receipt.transactionHash };
}

export {
  deployContract,
  publishProof,
  publishAward
}
