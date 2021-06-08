import Holder from "@diplomas/core/models/Holder";
import signupFactory from "@diplomas/core/utils/signupFactory";

export default {
  post: signupFactory(Holder)
}