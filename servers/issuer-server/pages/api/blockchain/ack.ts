import {publishAck} from '@diplomas/blockchain';

export default async function handler(req, res) {
  const response = await publishAck(req.body)
  res.status(200).json(response)
}