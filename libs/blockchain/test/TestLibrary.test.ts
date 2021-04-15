import { 
  deployContract,
  publishProof,
  publishAward,
  publishRequest,
  publishAck,
  publishFail
} from '../src/index';

import { ethers } from "ethers";
import { eventsABI } from "../src/eventsABI";

const abiDecoder = require('abi-decoder');
const provider = new ethers.providers.JsonRpcProvider('http://localhost:8545');
let contractAddress = "";
  beforeAll( async() => {
    const result = await deployContract();
    contractAddress = result.contractAddress;
    const requestABI = eventsABI;
    /* use abiDecoder to decode the logs and find the parameters of the emited event
      when a function of the smart contract was executed successfully
    */
    abiDecoder.addABI(requestABI);  
    console.log(result);
    console.log("The address of the smart contract is" + result.contractAddress);
  });

describe('testing functions in index.ts ', () => {
  it('should publish an award and then check that the correct data where published', async () => {
    const transcactionHashAward = await publishAward({
      hashOfAwardFirstPart:"0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
      hashOfAwardSecondPart: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb", 
      contractAddressUsedByIssuer: contractAddress
    });
    console.log(transcactionHashAward);
    /*search the Blockchain to find the transaction receipt.
      the search is done using the transactionHash of a transaction
    */
    let receipt = await provider.getTransactionReceipt(transcactionHashAward.transactionHash);
    // console.log(receipt);
    
    const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
    // console.log(decodedLogs[0].events[0].value);
    expect(decodedLogs[0].events[0].value).toBe("0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb");
  });

  it('should publish a proof and then check that the correct data where published', async () => {
    const transactionHashProof = await publishProof({
      contractAddressUsedByIssuer: contractAddress,
      /* for test use a random transactionHash */
      sReq: "0x63d6709a4d465d1223c9247cd4fd6c54c29f9e209f627d307c1bbdaea3b9a776",
      c: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
      c2: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
      nirenc: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
      ev: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
    });
    console.log(transactionHashProof);
    /*search the Blockchain to find the transaction receipt.
      the search is done using the transactionHash of a transaction
    */
    let receipt = await provider.getTransactionReceipt(transactionHashProof.transactionHash);
    // console.log(receipt);
    

    const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
    // console.log(decodedLogs[0].events[0].value);
    expect(decodedLogs[0].events[0].value).toBe("0x63d6709a4d465d1223c9247cd4fd6c54c29f9e209f627d307c1bbdaea3b9a776");
  });

  it('should publish a request and then check that the correct data where published', async () => {
    const transactionHashRequest = await publishRequest({
      contractAddressUsedByIssuer: contractAddress,
      sAwd: "0x63d6709a4d465d1223c9247cd4fd6c54c29f9e209f627d307c1bbdaea3b9a776",
      VerifKeyPart1: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
      VerifKeyPart2: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
      VerifKeyPart3: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
      VerifKeyPart4: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
    });
    console.log(transactionHashRequest);
    /*search the Blockchain to find the transaction receipt.
      the search is done using the transactionHash of a transaction
    */
    let receipt = await provider.getTransactionReceipt(transactionHashRequest.transactionHash);
    // console.log(receipt);
    
    const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
    // console.log(decodedLogs[0].events[0].value);
    expect(decodedLogs[0].events[0].value).toBe("0x63d6709a4d465d1223c9247cd4fd6c54c29f9e209f627d307c1bbdaea3b9a776");
  });

  it('should publish an ack and then check that the correct data where published', async () => {
    const transactionHashAck = await publishAck({
      contractAddressUsedByIssuer: contractAddress,
      sPrf: "0x63d6709a4d465d1223c9247cd4fd6c54c29f9e209f627d307c1bbdaea3b9a776",
      eI: "0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
    });
    console.log(transactionHashAck);
    /*search the Blockchain to find the transaction receipt.
      the search is done using the transactionHash of a transaction
    */
    let receipt = await provider.getTransactionReceipt(transactionHashAck.transactionHash);
    // console.log(receipt);
    
    const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
    // console.log(decodedLogs[0].events[0].value);
    expect(decodedLogs[0].events[0].value).toBe("0x63d6709a4d465d1223c9247cd4fd6c54c29f9e209f627d307c1bbdaea3b9a776");
  });

  it('should publish a fail and then check that the correct data where published', async () => {
    const transactionHashFail = await publishFail({
      contractAddressUsedByIssuer: contractAddress,
      sPrf: "0x63d6709a4d465d1223c9247cd4fd6c54c29f9e209f627d307c1bbdaea3b9a776"
    });
    console.log(transactionHashFail);
    /*search the Blockchain to find the transaction receipt.
      the search is done using the transactionHash of a transaction
    */
    let receipt = await provider.getTransactionReceipt(transactionHashFail.transactionHash);
    // console.log(receipt);
    
    const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
    // console.log(decodedLogs[0].events[0].value);
    expect(decodedLogs[0].events[0].value).toBe("0x63d6709a4d465d1223c9247cd4fd6c54c29f9e209f627d307c1bbdaea3b9a776");
  });
});
