import mongoose, {Schema} from "mongoose";

const DocumentSchema = new mongoose.Schema({
  title: String,
  type: String,
  department: String,
  issuer: {
    type: Schema.Types.ObjectId,
    ref: 'Issuer'
  },
  holder: {
    type: Schema.Types.ObjectId,
    ref: 'Holder'
  },
  grade: Number,
  degreeDate: Date,
  dean: String,
  certificateNumber: String,
  supervisors: String,
  createdAt: {
    type: Date,
    default: Date.now()
  }
});

// export model Document with DocumentSchema
const Document = mongoose.model("Document", DocumentSchema);
export default Document;