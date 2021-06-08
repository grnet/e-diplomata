import { Profile } from "@diplomas/core/models";
import { findOneFactory } from "@diplomas/core/utils/findOne";

export default {
  get: [
    findOneFactory((req)=>(req.query), Profile)
  ],

}