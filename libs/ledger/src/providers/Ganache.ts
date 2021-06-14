import { ethers } from 'ethers';

export const provider = new ethers.providers.JsonRpcProvider(
  'http://localhost:8545'
);
// for myaddress we set the Issuer, Holder, Verifier account
export const account = provider.getSigner(0);
export const address = account._address;
export const accountNotIssuer = provider.getSigner(1);
export const addressNotIssuer = accountNotIssuer._address;
