import { ethers } from 'ethers';
import { ProviderConfig } from './types';

export interface GetProviderInput {
  provider: ProviderConfig['provider'];
  network: ProviderConfig['network'];
  options?: ProviderConfig['options'];
}

export const getProvider = async ({
  provider,
  network,
  options,
}: GetProviderInput): Promise<
  ethers.providers.Provider | ethers.providers.JsonRpcProvider
> => {
  if (provider === 'ganache') {
    return new ethers.providers.JsonRpcProvider(network);
  } else if (provider === 'infura') {
    return ethers.getDefaultProvider(network, options);
  } else {
    throw new Error('Provider not supported');
  }
};
