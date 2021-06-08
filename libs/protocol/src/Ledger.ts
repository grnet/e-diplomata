

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

export interface LedgerConstructorInterface {
  provider: 'infura' | 'ganache';
  network: string;
  account: string;
  options: { etherscan?: string; infura?: any };
  address: string;
  bytecode: string;
  abi: Abi[];
}
export interface LedgerInterface {
  constructor: (
    props: LedgerConstructorInterface
  ) => LedgerInterface;
  publish: (
    signature: string
  ) => { hash?: string, error?: string }
  getTransaction: (
    transactionHash: string, 
    minConfirmations?: number
  ) => Promise<{ 
    hash: string;
    error?: string;
    status: 'confirmed' | 'pending' | 'fail';
    data?: string;
  }>
  getTransactionSync: (
    transactionHash: string, 
    minConfirmations?: number
  ) => Promise<{ 
    hash: string;
    error?: string;
    status: 'confirmed' | 'pending' | 'fail';
    data: string;
  }>
}
