import mongoose, {Schema} from "mongoose";

const AwardedDocumentSchema = new mongoose.Schema({
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
  c: {
    type: String
  },
  r: {
    type: String
  },
  signature: {
    type: String
  },
  transactionStatus: {
    type: String
  },
  transaction: {
    type: String
  },
  createdAt: {
    type: Date,
    default: Date.now()
  }
});

// export model Document with AwardedDocumentSchema
export default mongoose.model("AwardedDocument", AwardedDocumentSchema);