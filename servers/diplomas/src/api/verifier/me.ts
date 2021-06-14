import Verifier from "@diplomas/server/models/Verifier";
import meFactory from '@diplomas/server/utils/meFactory';

export default {
  get: meFactory(Verifier)
}