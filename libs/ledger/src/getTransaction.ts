import { ethers } from 'ethers';
import { ProviderConfig, ContractConfig } from '@diplomas/ledger/types';
import { getProvider } from './getProvider';

export interface GetTransactionInput {
  hash: string;
  provider: ProviderConfig['provider'];
  network: ProviderConfig['network'];
  providerOptions?: ProviderConfig['options'];
  abi?: ContractConfig['abi'];
  minConfirmations?: number;
}

export interface GetTransactionOutput {
  data?: string;
  status: 'pending' | 'confirmed' | 'fail';
}

// returns the content of a transaction and informs whether it is mined
export const getTransaction = async ({
  abi,
  hash,
  provider,
  network,
  providerOptions,
  minConfirmations = 10,
}: GetTransactionInput): Promise<GetTransactionOutput> => {
  const etherProvider = await getProvider({
    provider,
    network,
    options: providerOptions,
  });
  let receiptR = await etherProvider.getTransactionReceipt(hash);
  if (receiptR == null) {
    return {
      status: 'pending',
    };
  } else {
    let receipt = await etherProvider.getTransaction(hash);
    if (receipt.confirmations >= minConfirmations) {
      if (abi) {
        let interf = new ethers.utils.Interface(abi);
        const txInfo = interf.parseTransaction({ data: receipt.data });
        let data = txInfo.args
          .map((arg: string) => arg.replace(/^0x/, ''))
          .join('');
        return {
          data: data,
          status: 'confirmed',
        };
      }
      return {
        status: 'confirmed',
      };
    } else {
      return {
        status: 'pending',
      };
    }
  }
};

const delay = (time: number) => new Promise(res => setTimeout(res, time));

export const getTransactionSync = async (
  input: GetTransactionInput
): Promise<GetTransactionOutput> => {
  let tx = { status: 'pending' } as GetTransactionOutput;
  while (tx.status === 'pending') {
    await delay(1000);
    tx = await getTransaction(input);
  }
  return tx;
};

export default getTransaction;
