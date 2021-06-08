import mongoose from "mongoose";
import KeysSchema from '@diplomas/core/models/Keys';
const HolderUserSchema = new mongoose.Schema({
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
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now()
  },
  publicKey: String,
  keys: KeysSchema
});

// export model user with HolderUserSchema
export default mongoose.model("HolderUser", HolderUserSchema);