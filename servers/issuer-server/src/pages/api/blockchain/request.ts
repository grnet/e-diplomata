import {publishRequest} from '@diplomas/blockchain';

export default async function handler(req, res) {
  const response = await publishRequest(req.body)
  res.status(200).json(response)
}