import { ethers } from 'ethers';
//require('dotenv').config()

const network = 'ropsten';
// export const providerTest = ethers.getDefaultProvider(network, {
//     infura: `https://ropsten.infura.io/v3/${process.env.INFURA_ID}`,
//     // Or if using a project secret:
//     // infura: {
//     //   projectId: YOUR_INFURA_PROJECT_ID,
//     //   projectSecret: YOUR_INFURA_PROJECT_SECRET,
//     // },
// });
// export const signerTest = new ethers.Wallet(`${process.env.ServiceIssuerPrivateKey}`);
// // for myaddress we set the Issuer, Holder, Verifier account
// export const accountTest = signerTest.connect(providerTest);
// export const addressTest = accountTest.address;
export const providerTest = ethers.getDefaultProvider(network, {
  infura: `https://ropsten.infura.io/v3/bb87948463a54b10817d6cc48a48ebf7`,
  // Or if using a project secret:
  // infura: {
  //   projectId: YOUR_INFURA_PROJECT_ID,
  //   projectSecret: YOUR_INFURA_PROJECT_SECRET,
  // },
});
export const signerTest = new ethers.Wallet(
  `365c49f1e59341446c9b648505ee9fb5c538276ea6e42be0b53b76309aad27df`
);
// for myaddress we set the Issuer, Holder, Verifier account
export const accountTest = signerTest.connect(providerTest);
export const addressTest = accountTest.address;
