import Issuer from "@diplomas/core/models/Issuer";
import meFactory from '@diplomas/core/utils/meFactory';

export default {
  get: meFactory(Issuer)
}