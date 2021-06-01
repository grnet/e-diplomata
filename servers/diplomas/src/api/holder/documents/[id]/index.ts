import auth from "@diplomas/core/middlewares/auth"
import Document from "@diplomas/core/models/Document";
import Holder from "@diplomas/core/models/Holder";

export default {
    get: [
        auth(Holder), async function (req: any, res: any) {
            const response = await Document.findOne({ _id: req.params.id });
            return res.status(200).json(response);
        }
    ]
}