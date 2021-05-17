import db from "holder-server/lib/db";

export default async function handler(req, res) {
  db().findOne({ _id: req.query.id }, function (err, data) {
    return res.status(200).json(data);
  });
}