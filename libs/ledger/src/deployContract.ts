import { ethers } from 'ethers';
import { ProviderConfig, ContractConfig } from '@diplomas/ledger/types';
import { getProvider } from './getProvider';

const { ContractFactory } = ethers;

export interface DeployContractInput {
  provider: ProviderConfig['provider'];
  network: ProviderConfig['network'];
  providerOptions?: ProviderConfig['options'];
  account: ProviderConfig['account'];
  bytecode: ContractConfig['bytecode'];
  abi: ContractConfig['abi'];
}

export interface DeployContractOutput {
  address?: ContractConfig['address'];
  hash?: string;
  error?: string;
}

export const deployContract = async ({
  provider,
  account,
  abi,
  bytecode,
  network,
  providerOptions,
}: DeployContractInput): Promise<DeployContractOutput> => {
  try {
    let etherAccount: ethers.Wallet | ethers.providers.JsonRpcSigner;
    if (!account) {
      return {
        error: 'An account is required',
      };
    }
    const etherProvider = await getProvider({
      network,
      provider,
      options: providerOptions,
    });
    if (provider === 'ganache') {
      etherAccount = (etherProvider as ethers.providers.JsonRpcProvider).getSigner(
        parseInt(account)
      );
    } else if (provider === 'infura') {
      let signer = new ethers.Wallet(account);
      etherAccount = signer.connect(etherProvider);
    } else {
      return {
        error: 'Provider not supported',
      };
    }
    let newContract = new ContractFactory(abi, bytecode, etherAccount);
    const contract = await newContract.deploy();
    let receipt = contract.deployTransaction;
    return {
      address: contract.address,
      hash: receipt.hash,
    };
  } catch (err) {
    return {
      error: err,
    };
  }
};

export default deployContract;
