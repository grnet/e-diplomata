import {publishProof} from '@diplomas/blockchain';
import {provider, account, address} from '@diplomas/blockchain/Ganache';

export default async function handler(req, res) {
  const newBody = {...req.body, 
    provider: provider,
    accountIssuer: account,
    addressIssuer: address}
  const response = await publishProof(newBody)
  res.status(200).json(response)
}