
import {IssuerUser} from "@diplomas/server/models";
import loginFactory from "@diplomas/server/utils/loginFactory";
export default {
  post: loginFactory(IssuerUser)
}