import { ethers } from 'ethers';

export interface GenerateWalletInput {
  networkType: string;
  party: 'Issuer' | 'Holder' | 'Verifier';
}

export interface GenerateWalletOutput {
  //if ganache privkey is a number stored in string
  //if infura privkey is the private key
  private?: string;
  public?: string;
  error?: string;
}

export const generateWallet = async function({
  networkType,
  party,
}: GenerateWalletInput): Promise<GenerateWalletOutput> {
  if (networkType === 'ganache') {
    let provider = new ethers.providers.JsonRpcProvider(
      'http://localhost:8545'
    );
    if (party === 'Issuer') {
      let accountIssuer = provider.getSigner(0);
      return { private: '0', public: await accountIssuer.getAddress() };
    } else if (party === 'Holder') {
      let accountHolder = provider.getSigner(1);
      return { private: '1', public: await accountHolder.getAddress() };
    } else if (party === 'Verifier') {
      let accountVerifier = provider.getSigner(2);
      return { private: '2', public: await accountVerifier.getAddress() };
    } else {
      return { error: 'wrong string party' };
    }
  } else {
    let newWallet = ethers.Wallet.createRandom();
    return { private: newWallet.privateKey, public: newWallet.address };
  }
};
export default generateWallet;
