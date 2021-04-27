import db from "issuer-server/lib/db";

export default async function handler(req, res) {
  db.findOne({ id: req.query.id }, function (err, data) {
    return res.status(200).json(data);
  });
}
