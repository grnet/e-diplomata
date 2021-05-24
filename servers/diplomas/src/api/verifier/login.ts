
import Verifier from "@diplomas/core/models/Verifier";
import loginFactory from "@diplomas/core/utils/loginFactory";
export default {
  post: loginFactory(Verifier)
}