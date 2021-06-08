import mongoose, {Schema} from "mongoose";

const HolderShareRequestSchema = new mongoose.Schema({
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
  titleType: {
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
export default mongoose.model("HolderTitleRequest", HolderShareRequestSchema);