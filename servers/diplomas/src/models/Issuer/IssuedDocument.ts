import mongoose, {Schema} from "mongoose";

const IssuedDocumentSchema = new mongoose.Schema({
  document: {
    type: Schema.Types.ObjectId,
    ref: 'Document'
  },
  holderPub: String,
  issuer: {
    type: Schema.Types.ObjectId,
    ref: 'Issuer'
  },
  c: {
    type: Map,
    of: Array
  },
  r: {
    type: String
  },
  signature: {
    type: String
  },
  status: {
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

// export model Document with IssuedDocumentSchema
export default mongoose.model("IssuedDocument", IssuedDocumentSchema);