import authFactory from "@diplomas/core/middlewares/auth";
import { AwardedDocument, Holder } from "@diplomas/core/models";

export default {
  get: [
    authFactory(Holder),
    async function (req:any,res:any){
      const limits = parseInt(req.query.limit) || 10;
      const offsets = parseInt(req.query.offset) || 0;
      const skip = (offsets - 1) * limits;
      // const searchValue = req.query.search || "";
      const { limit, offset, search, ...queries } = req.query;
      // Document.createIndexes({ "$**": "text" });
      const counter = await AwardedDocument.countDocuments(
          {
              ...queries,
              holder: req.user.id
          }
      );
      const docs = await AwardedDocument.find({
          ...queries,
          holder: req.user.id

      }).populate('document holder issuer')
          .skip(skip)
          .limit(limits)
          .exec();
      res.send({
          data: docs,
          meta: {
              total: counter / limits,
              count: counter,
          },
      });
    }
  ]
}