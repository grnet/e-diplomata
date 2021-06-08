
import {IssuerUser} from "@diplomas/core/models";
import loginFactory from "@diplomas/core/utils/loginFactory";
export default {
  post: loginFactory(IssuerUser)
}