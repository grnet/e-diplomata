import auth from "@diplomas/core/middlewares/auth";
import { Issuer } from "@diplomas/core/models";
import Document from "@diplomas/core/models/Document";

export default {
    get: [auth(Issuer), async function (req: any, res: any) {
        const limits = parseInt(req.query.limit) || 10;
        const offsets = parseInt(req.query.offset) || 0;
        const skip = (offsets - 1) * limits;
        const searchValue = req.query.search || "";
        const { limit, offset, search, ...queries } = req.query;
        Document.createIndexes({ "$**": "text" });
        const counter = await Document.countDocuments(
            {
                ...queries,
                $text: { $search: searchValue }
            }
        );
        const docs = await Document.find({
            ...queries,
            $text: { $search: searchValue }
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