import mongoose from "mongoose";
import KeysSchema from '@diplomas/server/models/Keys';

const VerifierUserSchema = new mongoose.Schema({
  title: String,
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
  publicKey: String,
  keys: KeysSchema
});

// export model user with VerifierUserSchema
const VerifierUser = mongoose.model("VerifierUser", VerifierUserSchema);
export default VerifierUser