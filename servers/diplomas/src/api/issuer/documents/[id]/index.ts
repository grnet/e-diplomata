import auth from "@diplomas/core/middlewares/auth"
import Document from "@diplomas/core/models/Document";
import Issuer from "@diplomas/core/models/Issuer";

export default {
    get: [
        auth(Issuer), async function (req: any, res: any) {
           const data = await Document.findOne({ _id: req.query.id });
            res.status(200).json(data);
        }
    ]
}
