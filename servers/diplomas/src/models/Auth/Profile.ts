import mongoose from "mongoose";

const ProfileSchema = new mongoose.Schema({
  title: {
    type: String
  },
  publicKey: {
    type: String
  },
  walletAddress: {
    type: String
  },
  service: {
    type: String
  },
  type: {
    type: String,
    enum: ['Holder', 'Issuer', 'Verifier']
  },
  contract: String,
  verified: {
    type: Boolean,
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// export model Document with ProfileSchema
export default mongoose.model("Profile", ProfileSchema);