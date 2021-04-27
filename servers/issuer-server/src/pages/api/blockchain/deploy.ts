import {deployContract} from '@diplomas/blockchain';

export default async function handler(req, res) {
  const response = await deployContract()
  res.status(200).json(response)
}