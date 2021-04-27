import {publishAward} from '@diplomas/blockchain';

export default async function handler(req, res) {
  const response = await publishAward(req.body)
  res.status(200).json(response)
}