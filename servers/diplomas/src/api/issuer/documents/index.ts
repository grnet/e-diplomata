import auth from "@diplomas/server/middlewares/auth";
import { IssuerUser, Document } from "@diplomas/server/models";

export default {
    get: [
      auth(IssuerUser),
       async function (req: any, res: any) {
        const limits = parseInt(req.query.limit) || 10;
        const offsets = parseInt(req.query.offset) || 0;
        const skip = (offsets - 1) * limits;
        console.log(req.user)
        // const searchValue = req.query.search || "";
        const { limit, offset, search, ...queries } = req.query;
        // Document.createIndexes({ "$**": "text" });
        const counter = await Document.countDocuments(
            {
                ...queries,
                issuer: req.user.id
            }
        );
        const docs = await Document.find({
            ...queries,
            issuer: req.user.id

        })
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
    }]
}