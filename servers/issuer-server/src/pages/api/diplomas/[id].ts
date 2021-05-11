import db from "issuer-server/lib/db";

/* export default async function handler(req, res) {
  db.findOne({ id: req.query.id }, function (err, data) {
    return res.status(200).json(data);
  });
} */

export default async function handler(req, res) {
  let response = null;
  let statusDiploma = null;
  db().findOne({ _id: req.query.id }, function (err, data) {
    err && console.log("error", err);
    const shouldUpdate = data.status === "pending" ? data.transactionTime + 10000 < Date.now() : false;
    if (!shouldUpdate) {
      response = res.status(200).json(data);
    } else {
      const status = ["success", "fail"];
        let randomIndex = Math.floor(Math.random() * status.length);
        data.status = status[randomIndex];
        statusDiploma = data.status;
        update(statusDiploma);
        response = res.status(200).json(data); 
     }
    return response;
  });

  function update(statusDip) {
    db().update({ _id: req.query.id }, { $set: { status: statusDip } }, {}, function (err, data) {
      err && console.log("error", err);
      console.log(data);
    });
  }

}