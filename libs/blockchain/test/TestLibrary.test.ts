import { 
  deployContract,
  publish,
  transactionReceiptInfo,
  generateWallet
} from '../src/index';
import { eventsABI } from '../src/eventsABI';
/*Uncomment one of the following depending on the provider*/
//gia ganache topika
import { provider, account, address} from '../src/Ganache';
//provider.getUncheckedSigner(0);
//gia INFURA
//import { providerTest, accountTest } from '../src/Infura';
jest.setTimeout(30000);
const abiDecoder = require('abi-decoder');
const dummyHash = '0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb';

let contractAddress = '';
let receiptHash = '';

   beforeAll( async() => {
     const result = await deployContract({accountIssuer: account});
     contractAddress = result.contractAddress;
     let status = await transactionReceiptInfo({
       tHash: result.tranHash,
       provider: provider
     });
     while(status.status == "not mined yet"){
       status = await transactionReceiptInfo({
         tHash: result.tranHash,
         provider: provider
       })
     }
     const requestABI = eventsABI;
     /* use abiDecoder to decode the logs and find the parameters of the emited event
       when a function of the smart contract was executed successfully
     */
     abiDecoder.addABI(requestABI);
   });

  describe('testing functions in index.ts ', () => {

    // //
    // it('should deploy new contract to Ropsten', async () => {
    //   const resultRopsten = await deployContract({accountIssuer: accountTest});
    //   let contractAddressRopsten = resultRopsten.contractAddress;
    //   console.log(contractAddressRopsten);
    //   let status = await transactionReceiptInfo({
    //     tHash: resultRopsten.tranHash,
    //     provider: providerTest
    //   });
    //   console.log(status.status);
    //   while(status.status == "not mined yet"){
    //     status = await transactionReceiptInfo({
    //       tHash: resultRopsten.tranHash,
    //       provider: providerTest
    //     })
    //   }
    //   console.log(status.transactionReceiptInfo);
    // });
  
    
    it('should return transaction hash before it is mined', async () => {
      const transactionHashAward = await publish({
        s_1: dummyHash,
        s_2: dummyHash,
        s_3: dummyHash, 
        contractAddressUsedByIssuer: contractAddress,
        provider: provider,
        accountIssuer: account,
        addressIssuer: address
      });
      let status = await transactionReceiptInfo({
        tHash: transactionHashAward.transactionHash,
        provider: provider
      });
      expect(status.status).toBe('not mined yet');
    });

    // it('use infura return transaction receipt from ethereum ropsten', async () => {
    //   let status = await transactionReceiptInfo({
    //     tHash: "0x2a54e28913fbfb6fa926f28e264ab395924720a0289be635a28ee18cbe78aa78",
    //     provider: providerTest
    //   });
    //   console.log("mm"+ status.status);
    //   console.log(status.transactionReceiptInfo);
    // });
  
     it('should generate accounts', async () => {
       let accountHolder = generateWallet({
         networkType: 'infura',
         party: 'Holder'
       });
       console.log(accountHolder.newWalletAddress);
     });
  
    it('should publish an s_*award and then check that the correct data where published', async () => {
      const transactionHashAward = await publish({
        s_1: dummyHash,
        s_2: dummyHash, 
        s_3: dummyHash,
        contractAddressUsedByIssuer: contractAddress,
        provider: provider,
        accountIssuer: account,
        addressIssuer: address
      });
      let status = await transactionReceiptInfo({
        tHash: transactionHashAward.transactionHash,
        provider: provider
      });
      while(status.status == "not mined yet"){
        status = await transactionReceiptInfo({
          tHash: transactionHashAward.transactionHash,
          provider: provider
        })
      }
      expect(status.status).toBe('mined');
      /*search the Blockchain to find the transaction receipt.
        the search is done using the transactionHash of a transaction
      */
      let receipt = await provider.getTransactionReceipt(transactionHashAward.transactionHash);
      console.log(receipt);
      receiptHash = receipt.transactionHash;
      console.log(receiptHash);
      const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
      expect(decodedLogs[0].events[0].value).toBe(dummyHash);
    });

    it('return transaction receipt retrieved in the previous step', async () => {
      let status = await transactionReceiptInfo({
        tHash: receiptHash,
        provider: provider
      });
      console.log(status.transactionReceiptInfo);
    });
});  

//older Code 
// import { 
//   deployContract,
//   publishProof,
//   publishAward,
//   publishRequest,
//   publishAck,
//   publishFail
// } from '../src/index';
// import { eventsABI } from '../src/eventsABI';
// /*Uncomment one of the following depending on the provider*/
// //gia ganache topika
// import { provider, account, address, accountNotIssuer, addressNotIssuer } from '../src/Ganache';
// //gia INFURA
// //import { provider, myaccount, myaddress } from '../src/Infura';

// const abiDecoder = require('abi-decoder');
// const dummyTxHash = '0x63d6709a4d465d1223c9247cd4fd6c54c29f9e209f627d307c1bbdaea3b9a776';
// const dummyHash = '0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb';

// let contractAddress = '';
//   beforeAll( async() => {
//     const result = await deployContract({accountIssuer: account});
//     contractAddress = result.contractAddress;
//     const requestABI = eventsABI;
//     /* use abiDecoder to decode the logs and find the parameters of the emited event
//       when a function of the smart contract was executed successfully
//     */
//     abiDecoder.addABI(requestABI);
//   });

// describe('testing functions in index.ts ', () => {
//   it('should publish an award and then check that the correct data where published', async () => {
//     const transcactionHashAward = await publishAward({
//       hashOfAwardFirstPart: dummyHash,
//       hashOfAwardSecondPart: dummyHash, 
//       contractAddressUsedByIssuer: contractAddress,
//       provider: provider,
//       accountIssuer: account,
//       addressIssuer: address
//     });
//     /*search the Blockchain to find the transaction receipt.
//       the search is done using the transactionHash of a transaction
//     */
//     const receipt = await provider.getTransactionReceipt(transcactionHashAward.transactionHash);
//     const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
//     expect(decodedLogs[0].events[0].value).toBe(dummyHash);
//   });

//   it('should fail to publish an award because an account different than Issuer is used', async () => {
//     const transcactionHashAward = await publishAward({
//       hashOfAwardFirstPart: dummyHash,
//       hashOfAwardSecondPart: dummyHash, 
//       contractAddressUsedByIssuer: contractAddress,
//       provider: provider,
//       accountIssuer: accountNotIssuer,
//       addressIssuer: addressNotIssuer
//     });
//     expect(transcactionHashAward.error).toBe('VM Exception while processing transaction: revert Caller is not owner');
//   });

//   it('should publish a proof and then check that the correct data where published', async () => {
//     const transactionHashProof = await publishProof({
//       contractAddressUsedByIssuer: contractAddress,
//       /* for test use a random transactionHash */
//       sReq: dummyTxHash,
//       c: dummyHash,
//       c2: dummyHash,
//       nirenc: dummyHash,
//       ev: dummyHash,
//       provider: provider,
//       accountIssuer: account,
//       addressIssuer: address
//     });
//     /*search the Blockchain to find the transaction receipt.
//       the search is done using the transactionHash of a transaction
//     */
//     const receipt = await provider.getTransactionReceipt(transactionHashProof.transactionHash);
//     const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
//     expect(decodedLogs[0].events[0].value).toBe(dummyTxHash);
//   });

//   it('should fail to publish a proof because an account different than Issuer is used', async () => {
//     const transactionHashProof = await publishProof({
//       contractAddressUsedByIssuer: contractAddress,
//       /* for test use a random transactionHash */
//       sReq: dummyTxHash,
//       c: dummyHash,
//       c2: dummyHash,
//       nirenc: dummyHash,
//       ev: dummyHash,
//       provider: provider,
//       accountIssuer: accountNotIssuer,
//       addressIssuer: addressNotIssuer
//     });
//     /*search the Blockchain to find the transaction receipt.
//       the search is done using the transactionHash of a transaction
//     */
//       expect(transactionHashProof.error).toBe('VM Exception while processing transaction: revert Caller is not owner');
//   });

//   it('should publish a request and then check that the correct data where published', async () => {
//     const transactionHashRequest = await publishRequest({
//       contractAddressUsedByIssuer: contractAddress,
//       sAwd: dummyTxHash,
//       VerifKeyPart1: dummyHash,
//       VerifKeyPart2: dummyHash,
//       VerifKeyPart3: dummyHash,
//       VerifKeyPart4: dummyHash,
//       provider: provider,
//       accountHolder: account,
//       addressHolder: address
//     });
//     /*search the Blockchain to find the transaction receipt.
//       the search is done using the transactionHash of a transaction
//     */
//     const receipt = await provider.getTransactionReceipt(transactionHashRequest.transactionHash);
//     const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
//     expect(decodedLogs[0].events[0].value).toBe(dummyTxHash);
//   });

//   it('should publish an ack and then check that the correct data where published', async () => {
//     const transactionHashAck = await publishAck({
//       contractAddressUsedByIssuer: contractAddress,
//       sPrf: dummyTxHash,
//       eI: dummyHash,
//       provider: provider,
//       accountVerifier: account,
//       addressVerifier: address
//     });
//     /*search the Blockchain to find the transaction receipt.
//       the search is done using the transactionHash of a transaction
//     */
//     const receipt = await provider.getTransactionReceipt(transactionHashAck.transactionHash);    
//     const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
//     expect(decodedLogs[0].events[0].value).toBe(dummyTxHash);
//   });

//   it('should publish a fail and then check that the correct data where published', async () => {
//     const transactionHashFail = await publishFail({
//       contractAddressUsedByIssuer: contractAddress,
//       sPrf: dummyTxHash,
//       provider: provider,
//       accountVerifier: account,
//       addressVerifier: address
//     });
//     /*search the Blockchain to find the transaction receipt.
//       the search is done using the transactionHash of a transaction
//     */
//     const receipt = await provider.getTransactionReceipt(transactionHashFail.transactionHash);    
//     const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
//     expect(decodedLogs[0].events[0].value).toBe(dummyTxHash);
//   });
// });
