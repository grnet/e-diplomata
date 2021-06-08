import { getProfile } from "@diplomas/core/utils/auth";
import mongoose, {Schema} from "mongoose";

const AwardedDocumentSchema = new mongoose.Schema({
  title: String,
  type: String,
  department: String,
  holder: {
    type: Schema.Types.ObjectId,
    ref: 'HolderUser'
  },
  documentId: String,
  holderPub: String,
  grade: Number,
  degreeDate: Date,
  dean: String,
  certificateNumber: String,
  supervisors: String,
  award: String,
  status: String,
  issuerPub: String,
  c: {
    type: Map,
    of: Array
  },
  signature: {
    type: String
  },
  transaction: {
    type: String
  },
});

AwardedDocumentSchema.virtual('issuer').get(async function(){
  return await getProfile(this.issuerPub)
})

// export model Document with AwardedDocumentSchema
export default mongoose.model("AwardedDocument", AwardedDocumentSchema);