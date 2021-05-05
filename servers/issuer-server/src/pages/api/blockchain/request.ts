import {publishRequest} from '@diplomas/blockchain';
import {provider, account, address} from '@diplomas/blockchain/Ganache';

export default async function handler(req, res) {
  const newBody = {...req.body, 
    provider: provider,
    accountHolder: account,
    addressHolder: address}
  const response = await publishRequest(newBody)
  res.status(200).json(response)
}