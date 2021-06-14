// publishRequest

import authFactory from "@diplomas/server/middlewares/auth";
import ledgerMiddleware from "@diplomas/server/middlewares/ledger";
import {HolderUser} from "@diplomas/server/models";

// list requests
export default {
  // get: [
  //   authFactory(HolderUser),
  //   async function (req, res){
      
  //   }
  // ],
  post: [
    authFactory(HolderUser),
    ledgerMiddleware,
    async function (req, res){
      const protocol = req.ctx
      console.log(req.params)
      await protocol.request(req.params.id, req.body.verifier)
      res.json({ok: true})
    }
  ]
}