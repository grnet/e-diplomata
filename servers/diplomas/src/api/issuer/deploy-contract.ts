import authFactory from "@diplomas/server/middlewares/auth";
import { IssuerUser } from "@diplomas/server/models";

export default {
  post: [
    authFactory(IssuerUser),
    async function(req,res){
      const {
        
      } = req.body
    }
  ]
}