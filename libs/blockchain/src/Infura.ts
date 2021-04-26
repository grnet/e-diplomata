import { ethers } from "ethers";
//require('dotenv').config()

const network = 'ropsten';
export const provider = ethers.getDefaultProvider(network, {
    infura: `https://ropsten.infura.io/v3/${process.env.INFURA_ID}`,
    // Or if using a project secret:
    // infura: {
    //   projectId: YOUR_INFURA_PROJECT_ID,
    //   projectSecret: YOUR_INFURA_PROJECT_SECRET,
    // },
});
export const signer = new ethers.Wallet(`${process.env.ServiceIssuerPrivateKey}`);
// for myaddress we set the Issuer, Holder, Verifier account
export const account = signer.connect(provider);
export const address = account.address;

