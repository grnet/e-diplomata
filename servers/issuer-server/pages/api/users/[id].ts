import { users } from "./index";

export default async function handler(req, res) {
  return res.status(200).json(users.find((user) => user.id === req.params.id));
}
