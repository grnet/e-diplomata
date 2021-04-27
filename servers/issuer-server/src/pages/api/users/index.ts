export const users = [
  {
    id: "1",
    username: "Robin Wierdo",
  },
  {
    id: "3",
    username: "Bobin Marlein",
  },
];

export default async function handler(req, res) {
  return res.status(200).json(users);
}
