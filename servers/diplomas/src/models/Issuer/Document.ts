import { getProfile } from "@diplomas/core/utils/auth";
import mongoose, {Schema} from "mongoose";

const DocumentSchema = new mongoose.Schema({
  title: String,
  type: String,
  department: String,
  issuer: {
    type: Schema.Types.ObjectId,
    ref: 'IssuerUser'
  },
  holderPub: String,
  grade: Number,
  degreeDate: Date,
  dean: String,
  certificateNumber: String,
  supervisors: String,
  award: String,
  status: String,
  createdAt: {
    type: Date,
    default: Date.now()
  }
},{
  toJSON: { virtuals: true }, // So `res.json()` and other `JSON.stringify()` functions include virtuals
  toObject: { virtuals: true } // So `toObject()` output includes virtuals
});
DocumentSchema.virtual('holder').get(async function(){
  return await getProfile(this.holderPub)
})

// export model Document with DocumentSchema
export default mongoose.model("Document", DocumentSchema);
mongoose.model('Document').updateOne()