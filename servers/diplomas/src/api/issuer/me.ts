import {IssuerUser} from "@diplomas/server/models";
import meFactory from '@diplomas/server/utils/meFactory';

export default {
  get: meFactory(IssuerUser)
}