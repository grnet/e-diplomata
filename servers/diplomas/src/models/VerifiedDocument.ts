import mongoose, {Schema} from "mongoose";

const VerifiedDocumentSchema = new mongoose.Schema({
  document: {
    type: Schema.Types.ObjectId,
    ref: 'Document'
  },
  holder: {
    type: Schema.Types.ObjectId,
    ref: 'Holder'
  },
  issuer: {
    type: Schema.Types.ObjectId,
    ref: 'Issuer'
  },
  verifier: {
    type: Schema.Types.ObjectId,
    ref: 'Verifier'
  },
  createdAt: {
    type: Date,
    default: Date.now()
  }
});

// export model Document with VerifiedDocumentSchema
export default mongoose.model("VerifiedDocument", VerifiedDocumentSchema);