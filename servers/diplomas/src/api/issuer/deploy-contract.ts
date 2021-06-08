import authFactory from "@diplomas/core/middlewares/auth";
import { IssuerUser } from "@diplomas/core/models";

export default {
  post: [
    authFactory(IssuerUser),
    async function(req,res){
      const {
        
      } = req.body
    }
  ]
}