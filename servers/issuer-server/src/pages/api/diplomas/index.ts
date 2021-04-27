import db from "issuer-server/lib/db";

export default async function handler(req, res) {
  let response = null;
  if (req.method === "POST") {
    // Process a POST request
    response = res.status(200).json({ ok: true });
  } else {
    let counter = 0;
    const limits = parseInt(req.query.limit) || 10;
    const offsets = parseInt(req.query.offset) || 0;
    const skip = (offsets - 1) * limits;
    const searchValue = req.query.search || "";
    const { limit, offset, search, ...queries } = req.query;
    db.count(
      {
        ...queries,
        $where: function () {
          return Object.values(this).join(" ").includes(searchValue);
        },
      },
      function (err, count) {
        counter = count;
      }
    );
    db.find({
      ...queries,
      $where: function () {
        return Object.values(this).join(" ").includes(searchValue);
      },
    })
      .skip(skip)
      .limit(limits)
      .exec(function (err, data) {
        response = res.send({
          data: data,
          meta: {
            total: counter / limits,
            count: counter,
          },
        });
      });
  }
  return response;
}
