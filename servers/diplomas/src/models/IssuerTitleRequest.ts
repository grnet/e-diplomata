import mongoose, {Schema} from "mongoose";

const IssuerTitleRequestSchema = new mongoose.Schema({
  holder: {
    type: Schema.Types.ObjectId,
    ref: 'Holder'
  },
  issuer: {
    type: Schema.Types.ObjectId,
    ref: 'Issuer'
  },
  department: {
    type: String
  },
  year: {
    type: String
  },
  qualificationTitle: {
    type: String
  },
  qualificationType: {
    type: String
  },
  status: {
    type: String
  },
  document: {
    type: Schema.Types.ObjectId,
    ref: 'AwardedDocument'
  },
  createdAt: {
    type: Date,
    default: Date.now()
  }
});

// export model Document with HolderDocumentSchema
export default mongoose.model("IssuerTitleRequest", IssuerTitleRequestSchema);