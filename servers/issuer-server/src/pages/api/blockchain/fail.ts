import {publishFail} from '@diplomas/blockchain';

export default async function handler(req, res) {
  const response = await publishFail(req.body)
  res.status(200).json(response)
}