import auth from "@diplomas/core/middlewares/auth"
import Document from "@diplomas/core/models/Document";
import Verifier from "@diplomas/core/models/Verifier";

export default {
    get: [
        auth(Verifier), async function (req: any, res: any) {
            const response = await Document.findOne({ _id: req.params.id });
            return res.status(200).json(response);
        }
    ]
}