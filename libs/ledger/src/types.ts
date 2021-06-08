export interface Abi {
  inputs: Input[];
  name: string;
  outputs: any[];
  stateMutability: string;
  type: string;
}

export interface Input {
  internalType: string;
  name: string;
  type: string;
}

export type ProviderConfig = {
  provider: 'infura' | 'ganache';
  // if ganache provide the number of the account
  number: number;
  network: string;
  account: string;
  options: { etherscan?: string; infura?: any };
};

export type ContractConfig = {
  address: string;
  bytecode: string;
  abi: Abi[];
};
