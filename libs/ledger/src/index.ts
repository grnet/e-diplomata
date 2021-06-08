export * from './contracts/Award';
export { default as deployContract } from './deployContract';
export { default as generateWallet } from './generateWallet';
export * from './getTransaction';
export * from './providers/Ganache';
export * from './providers/Infura';
export * from './publish';
export * from './types';

import {getTransaction} from './getTransaction';
import {publish} from './publish';
import {LedgerInterface} from '@diplomas/protocol'

class Ledger implements LedgerInterface {
  getTransaction(...args) {
    return getTransaction(...args)
  }  
  publish(...args) {
    return publish(...args)
  }  
}

export default Ledger