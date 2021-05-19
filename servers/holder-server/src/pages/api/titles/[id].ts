import db from "holder-server/lib/db";

export default async function handler(req, res) {
  let response = null;
  let statusTitle = null;
  db().findOne({ _id: req.query.id }, function (err, data) {
    err && console.log("error", err);
    const shouldUpdate = data.status === "pending" ? data.transactionTime + 10000 < Date.now() : false;
    if (!shouldUpdate) {
      response = res.status(200).json(data);
    } else {
      const status = ["success", "fail"];
      let randomIndex = Math.floor(Math.random() * status.length);
      data.status = status[randomIndex];
      statusTitle = data.status;
      update(statusTitle);
      response = res.status(200).json(data);
    }
    return response;
  });

  function update(statusTitl) {
    db().update({ _id: req.query.id }, { $set: { status: statusTitl } }, {}, function (err, data) {
      err && console.log("error", err);
      console.log(data);
    });
  }

}