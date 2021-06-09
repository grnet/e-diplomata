import {IssuerUser} from "@diplomas/server/models";
import signupFactory from "@diplomas/server/utils/signupFactory";

export default {
  post: signupFactory(IssuerUser)
}