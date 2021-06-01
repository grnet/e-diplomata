import auth from "@diplomas/core/middlewares/auth";
import { Verifier } from "@diplomas/core/models";
import Document from "@diplomas/core/models/Document";

export default {
    get: [auth(Verifier), async function (req: any, res: any) {
        const limits = parseInt(req.query.limit) || 10;
        const offsets = parseInt(req.query.offset) || 0;
        const skip = (offsets - 1) * limits;
        const searchValue = req.query.search || "";
        const { limit, offset, search, ...queries } = req.query;
        console.log(queries);
        queries.verifier = req.user.id;

        const counter = await Document.countDocuments({ ...queries }).where(
            {
                $or: [
                    { title: { $regex: new RegExp(searchValue, 'i') } },
                    { type: { $regex: new RegExp(searchValue, 'i') } },
                ]
            });
        const response = await Document.find({ ...queries }).where(
            {
                $or: [
                    { title: { $regex: new RegExp(searchValue, 'i') } },
                    { type: { $regex: new RegExp(searchValue, 'i') } },
                ]
            })
            .skip(skip)
            .limit(limits)
            .exec();
        return res.send({
            data: response,
            meta: {
                total: counter / limits,
                count: counter,
            },
        });
    }]
}