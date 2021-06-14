import Verifier from "@diplomas/server/models/Verifier";
import signupFactory from "@diplomas/server/utils/signupFactory";

export default {
  post: signupFactory(Verifier)
}