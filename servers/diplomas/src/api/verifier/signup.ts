import Verifier from "@diplomas/core/models/Verifier";
import signupFactory from "@diplomas/core/utils/signupFactory";

export default {
  post: signupFactory(Verifier)
}