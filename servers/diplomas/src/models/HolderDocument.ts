import mongoose, {Schema} from "mongoose";

const HolderDocumentSchema = new mongoose.Schema({
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
  createdAt: {
    type: Date,
    default: Date.now()
  }
});

// export model Document with HolderDocumentSchema
export default mongoose.model("HolderDocument", HolderDocumentSchema);