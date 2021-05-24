// publishRequest

import authFactory from "@diplomas/core/middlewares/auth";
import Holder from "@diplomas/core/models/Holder";

// list requests
export default {
  get: [
    authFactory(Holder),
    async function (){}
  ],
  post: [
    authFactory(Holder),
    async function (){}
  ]
}