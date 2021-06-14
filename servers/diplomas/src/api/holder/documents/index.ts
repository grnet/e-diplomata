import authFactory from "@diplomas/server/middlewares/auth";
import { AwardedDocument, HolderUser } from "@diplomas/server/models";

export default {
  get: [
    authFactory(HolderUser),
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

      })
          .skip(skip||0)
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