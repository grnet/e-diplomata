import { diplomas } from "./index";

export default async function handler(req, res) {
  return res
    .status(200)
    .json(diplomas.find((diploma) => diploma.id === req.query.id));
}
