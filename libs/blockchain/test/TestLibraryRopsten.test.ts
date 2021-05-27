import { 
   // deployContract,
    publish,
    transactionReceiptInfo
} from '../src/index';

import { ethers } from 'ethers';
import { CERTIFICATE_ABI } from '../src/contracts/Award';
import { providerTest, accountTest, addressTest } from '../src/Infura';
jest.setTimeout(100000);
const dummyHash = '0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb';
// const dummyHash = '0x81c1eee27c3af6b85037b7f2198130b1abcefcfba489a9a2d489c9aa4ab1a76b';
// const dummyHash2 = '0x61faba9f8e8194846a70048a9ff1af8810a11981fc31411032fcf5e9a6c9b460';
// const dummyHash3 = '0x9a584ee3f09e9a0198ea5e1c75a04e8715b25af7a1418800d0cfa4205e4b1576';

describe('testing functions in index.ts ', () => {

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
    //   //check terminal to see transactionReceiptInfo of the deployed contract
    //   console.log(status.transactionReceiptInfo);
    // });

    it('use infura return transaction receipt from ethereum ropsten', async () => {
      let status = await transactionReceiptInfo({
        tHash: "0x2a54e28913fbfb6fa926f28e264ab395924720a0289be635a28ee18cbe78aa78",
        provider: providerTest
      });
      console.log(status.transactionReceiptInfo);
    });
//
    // it('should publish an s_*award to Ropsten and then check that the correct data where published', async () => {
    //     const transactionHashAward = await publish({
    //         s_1: dummyHash,
    //         s_2: dummyHash, 
    //         s_3: dummyHash,
    //         contractAddressUsedByIssuer: '0xc466220c018f76747a272d2416e93de8bbd37d6e',
    //         provider: providerTest,
    //         accountIssuer: accountTest,
    //         addressIssuer: addressTest
    //     });
    //     let status = await transactionReceiptInfo({
    //         tHash: transactionHashAward.transactionHash,
    //         provider: providerTest
    //     });
    //     while(status.status == "not mined yet"){
    //         status = await transactionReceiptInfo({
    //             tHash: transactionHashAward.transactionHash,
    //             provider: providerTest
    //         })
    //     }
    //     expect(status.status).toBe('mined');
    //     /*search the Blockchain to find the transaction receipt.
    //     the search is done using the transactionHash of a transaction
    //     */
    //     let data = status.transactionReceiptInfo?.data;
    //     console.log(data);
    //     let interf = new ethers.utils.Interface( CERTIFICATE_ABI );
    //     if(data){
    //         let txInfo = interf.parseTransaction({ data })
    //         console.log(txInfo.args);
    //         expect(txInfo.args[0]).toBe('0x81c1eee27c3af6b85037b7f2198130b1abcefcfba489a9a2d489c9aa4ab1a76b');
    //     }
    // });
    //
    it('test data ethereum Ropsten', async () => {
        let status = await transactionReceiptInfo({
            tHash: "0x30b90bddfa1a1dbb94feecaa5301c840f7015e028d4657ef354e272582095d64",
            provider: providerTest
        });
        console.log(status.transactionReceiptInfo?.data);
        let data = status.transactionReceiptInfo?.data;
        // //  //let data = '0x155c4a4eca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bbca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bbca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb';
        let interf = new ethers.utils.Interface( CERTIFICATE_ABI );
        if(data){
            const txInfo = interf.parseTransaction({ data })
            console.log(txInfo.args);
            expect(txInfo.args[0]).toBe('0xca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb');
        }
    });

});