import Holder from "@diplomas/server/models/Holder";
import signupFactory from "@diplomas/server/utils/signupFactory";

export default {
  post: signupFactory(Holder)
}