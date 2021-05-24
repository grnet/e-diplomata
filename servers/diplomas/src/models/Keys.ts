import mongoose from "mongoose";

const PrivatePublic = new mongoose.Schema({
  private: {
    type: String
  },
  public: {
    type: String
  }
})


const KeysSchema = new mongoose.Schema({
  nacl: PrivatePublic,
  wallet: PrivatePublic,
  elgamal: PrivatePublic
});

// export model Document with DocumentSchema
export default KeysSchema