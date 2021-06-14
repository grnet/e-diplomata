import auth from "@diplomas/server/middlewares/auth"
import {Document, IssuerUser} from "@diplomas/server/models";

export default {
  get: [
    auth(IssuerUser), 
    async function (req: any, res: any) {
      // console.log(req.user, req.params)
      const document = await Document
        .findOne({_id: req.params.id, issuer: req.user._id})
        .populate('issuer','title') as any;
      const holder = await document.holder
      res.status(200).json({...document.toJSON(), holder});
    }
  ]
}
