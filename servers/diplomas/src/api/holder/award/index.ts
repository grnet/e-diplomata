import { AwardedDocument, HolderUser } from "@diplomas/server/models"

export default {
  post: [
    async function(req:any,res:any){
      const holder = await HolderUser.findOne({publicKey: req.body.holderPub})
      console.log(req.body)
      if(!holder){
        res.status(500).json({error: 'Holder not found'})
      }
      delete req.body.id
      await AwardedDocument.create({
        ...req.body,
        holder: holder.id,
        documentId: req.body.id
      })
      res.json({ok:true})
    }
  ]
}