
import Verifier from "@diplomas/server/models/Verifier";
import loginFactory from "@diplomas/server/utils/loginFactory";
export default {
  post: loginFactory(Verifier)
}