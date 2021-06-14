import { ProtocolInterface } from "@diplomas/protocol/Protocol";
import authFactory from "@diplomas/server/middlewares/auth";
import ledgerMiddleware from "@diplomas/server/middlewares/ledger";
import {  IssuerUser } from "@diplomas/server/models";

export default {
  post: [
    authFactory(IssuerUser),
    ledgerMiddleware,
    async function(req: any, res: any){
      // console.log(DiplomasCrypto)
      // console.log(req.user, req.params.id)
      console.log('awarding')
      const protocol = req.ctx as ProtocolInterface
      console.log(protocol)
      protocol.award(req.params.id, req.user.keys.crypto.private)
      res.json({ok: true})

      // const document = await Document
      //     .findById(req.params.id) as any
      // const preDocument = {...document}
      // const issuer = await Issuer.findById(document.issuer) as any
      // console.log(issuer)
      // if(issuer.id !== req.user.id){
      //   return res.status(404).json({
      //     error: 'Issuer does not own document'
      //   })
      // }
      // const title = JSON.stringify(document)
      // const {s_awd, c, r} = await DiplomasCrypto.publish_award(title, issuer.keys.crypto.private)
      // const issuedDocument = await IssuedDocument.create({
      //   document: document.id,
      //   holderPub: document.holderPub,
      //   issuer: document.issuer,
      //   c,
      //   r,
      //   signature: s_awd,
      //   status: 'pending'
      // }) as any
      // // issuedDocument.status = 'pending'
      // issuedDocument.c = c;
      // issuedDocument.r = r;
      // issuedDocument.save()

      // req.publish(s_awd).then(async (transactionHashAward)=>{
        
      //   const receiptHash = transactionHashAward.hash;
      //   const receipt = await req.getTransaction(receiptHash)
      //   let data = receipt.data;
      //   console.assert(data === s_awd, s_awd, data)
      //   issuedDocument.transaction =  receiptHash
      //   issuedDocument.status = receipt.status
      //   issuedDocument.save()
      //   const holder = await getProfile(document.holderPub)
      //   const award = await fetch(`${holder.service}/api/holder/award/`, {
      //     method: 'POST',
      //     body: JSON.stringify({
      //       ...preDocument,
      //       transaction: receiptHash,
      //       signature: s_awd,
      //       c,
      //       issuerPub: issuer.publicKey
      //     }),
      //     headers: { 'Content-Type': 'application/json' },
      //   })

      //   console.log('updated Award', award)
      // })
    }
  ]
}