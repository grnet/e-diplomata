import Ledger, {deployContract} from '@diplomas/ledger'
import Crypto from '@diplomas/crypto'
import Protocol from '@diplomas/protocol'
import Messaging from '@diplomas/messaging'
import Storage from '@diplomas/storage'
import mongoose from 'mongoose'
import { Bytecode, CERTIFICATE_ABI } from '../config/certificate'
const contract: any = {
  abi: CERTIFICATE_ABI,
  provider: 'ganache',
  network: process.env.GANACHEURI || 'http://localhost:8545',
}

export default async function ledgerMiddleware(req: any, _res: any, next: any) {
  if(!contract.address){
    console.log('deploying contract', req.user.keys.wallet.private)
    const result = await deployContract(
      {
        ...contract,
        bytecode: Bytecode,
        account: req.user.keys.wallet.private
      }
    )
    contract.address = result.address
    console.log(result, 'contract response')
  }
  console.log('contract address', contract.address)
  console.log('creating protocol instance')
  req.ctx = new Protocol(
    {
      storage: new Storage(mongoose),
      ledger: new Ledger({
        ...contract,
        account: req.user.keys.wallet.private 
      }),
      messaging: new Messaging(),
      crypto: new Crypto(),
      user: req.user
    }
  )

  next();
}