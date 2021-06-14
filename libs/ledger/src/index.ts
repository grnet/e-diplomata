export * from './contracts/Award';
export { default as deployContract } from './deployContract';
export { default as generateWallet } from './generateWallet';
export * from './getTransaction';
export * from './providers/Ganache';
export * from './providers/Infura';
export * from './publish';
export * from './types';
import generateWallet, { GenerateWalletInput } from './generateWallet'
import { getTransaction, getTransactionSync } from './getTransaction';
import { publish } from './publish';
import { LedgerConstructorInterface, LedgerInterface } from '@diplomas/protocol'

class Ledger implements LedgerInterface {
  config: LedgerConstructorInterface;

  constructor(props: LedgerConstructorInterface) {
    this.config = props
  }
  static generateWallet(input: GenerateWalletInput){
    return generateWallet(input)
  }
  getTransaction(
    hash: string,
    minConfirmations?: number
  ) {
    return getTransaction({
      ...this.config,
      hash,
      minConfirmations
    })
  }
  getTransactionSync(
    hash: string,
    minConfirmations?: number
  ) {
    return getTransactionSync({
      ...this.config,
      hash,
      minConfirmations
    })
  }
  publish(signature: string) {
    return publish({ ...this.config, signature })
  }
}

export default Ledger