import { Profile } from "@diplomas/server/models";
import { findOneFactory } from "@diplomas/server/utils/findOne";

export default {
  get: [
    findOneFactory((req)=>(req.query), Profile)
  ],

}