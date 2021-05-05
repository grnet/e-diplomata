import {publishFail} from '@diplomas/blockchain';
import {provider, account, address} from '@diplomas/blockchain/Ganache';

export default async function handler(req, res) {
  const newBody = {...req.body, 
    provider: provider,
    accountVerifier: account,
    addressVerifier: address}
  const response = await publishFail(newBody)
  res.status(200).json(response)
}