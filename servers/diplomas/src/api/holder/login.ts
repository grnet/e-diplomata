
import Holder from "@diplomas/core/models/Holder";
import loginFactory from "@diplomas/core/utils/loginFactory";
export default {
  post: loginFactory(Holder)
}