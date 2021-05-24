import db from "verifier-server/lib/db";

export default async function handler(req, res) {
    db().update({ _id: req.body.id }, { $set: { status: req.body.statusTitle } }, {}, function (err, data) {
        err && console.log("error", err);
        return res.status(200).json(data);
    });

}