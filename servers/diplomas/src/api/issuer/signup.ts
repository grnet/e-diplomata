import Issuer from "@diplomas/core/models/Issuer";
import signupFactory from "@diplomas/core/utils/signupFactory";

export default {
  post: signupFactory(Issuer)
}