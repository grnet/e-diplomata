import {publishProof} from '@diplomas/blockchain';

export default async function handler(req, res) {
  const response = await publishProof(req.body)
  res.status(200).json(response)
}