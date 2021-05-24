
import Issuer from "@diplomas/core/models/Issuer";
import loginFactory from "@diplomas/core/utils/loginFactory";
export default {
  post: loginFactory(Issuer)
}