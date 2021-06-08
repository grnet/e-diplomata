// publishRequest

import authFactory from "@diplomas/core/middlewares/auth";
import {HolderUser} from "@diplomas/core/models";

// list requests
export default {
  get: [
    authFactory(HolderUser),
    async function (req, res){
      
    }
  ],
  post: [
    authFactory(HolderUser),
    async function (){}
  ]
}