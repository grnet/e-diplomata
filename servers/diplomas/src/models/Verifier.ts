import mongoose from "mongoose";
import KeysSchema from "./Keys";

const VerifierSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true
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

// export model user with VerifierSchema
export default mongoose.model("verifier", VerifierSchema);