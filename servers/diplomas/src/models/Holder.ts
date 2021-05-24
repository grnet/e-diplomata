import mongoose from "mongoose";
import KeysSchema from './Keys';
const HolderSchema = new mongoose.Schema({
  firstName: {
    type: String
  },
  lastName: {
    type: String
  },
  fatherName: {
    type: String
  },
  email: {
    type: String,
    required: true
  },
  password: {
    type: String,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now()
  },
  keys: KeysSchema
});

// export model user with HolderSchema
export default mongoose.model("Holder", HolderSchema);