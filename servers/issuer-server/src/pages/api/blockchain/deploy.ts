import {deployContract} from '@diplomas/blockchain';
import {account} from '@diplomas/blockchain/Ganache';

export default async function handler(req, res) {
  const newBody = {...req.body, accountIssuer: account}
  const response = await deployContract(newBody)
  res.status(200).json(response)
}