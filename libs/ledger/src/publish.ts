import { ethers } from 'ethers';
import { ProviderConfig, ContractConfig } from '@diplomas/ledger/types';
import { getProvider } from './getProvider';

const { Contract, utils } = ethers;

export interface PublishInput {
  signature: string;
  provider: ProviderConfig['provider'];
  network: ProviderConfig['network'];
  providerOptions?: ProviderConfig['options'];
  //an valw optional to account den leitourgei
  account: ProviderConfig['account'];
  abi: ContractConfig['abi'];
  address: ContractConfig['address'];
}

export interface PublishOutput {
  hash?: string;
  error?: string;
}

export const publish = async ({
  abi,
  address,
  provider,
  signature,
  account,
  network,
  providerOptions,
}: PublishInput): Promise<PublishOutput> => {
  let etherAddress = '';
  let etherAccount: ethers.Wallet | ethers.providers.JsonRpcSigner;
  const etherProvider = await getProvider({
    provider,
    network,
    options: providerOptions,
  });
  if (provider === 'ganache') {
    etherAccount = (etherProvider as ethers.providers.JsonRpcProvider).getSigner(
      parseInt(account)
    );
    etherAddress = etherAccount._address;
  } else if (provider === 'infura') {
    let signer = new ethers.Wallet(account);
    etherAccount = signer.connect(etherProvider);
    etherAddress = etherAccount.address;
  } else {
    return {
      error: 'Provider not supported',
    };
  }
  const s1 = `0x${signature.substring(0, 64)}`;
  const s2 = `0x${signature.substring(64, 128)}`;
  const s3 = `0x${signature.substring(128, 192)}`;
  let conInstance = new Contract(address, abi, etherAccount);
  //estimateGas
  let gasPrice = utils.parseUnits('10', 'gwei').toNumber();
  let gas;
  try {
    gas = await conInstance.estimateGas.publish(s1, s2, s3);
  } catch (err) {
    return {
      error: err.error.message,
    };
  }
  const options = {
    gasLimit: gas,
    gasPrice: gasPrice,
    from: etherAddress,
  };
  let receipt = await conInstance.publish(s1, s2, s3, options);
  return {
    hash: receipt.hash,
  };
};
