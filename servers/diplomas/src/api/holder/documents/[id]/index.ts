import auth from "@diplomas/core/middlewares/auth"
import {AwardedDocument, HolderUser} from "@diplomas/core/models";

export default {
  get: [
    auth(HolderUser), 
    async function (req: any, res: any) {
      const awardedDocument = await AwardedDocument
        .findById(req.params.id)
        .populate('holder', 'firstName lastName') as any;
      const issuer = await awardedDocument.issuer
      res.status(200).json({...awardedDocument.toJSON(), issuer});
    }
  ]
}
