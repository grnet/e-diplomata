import mongoose from "mongoose";

const PrivatePublicCrypto = new mongoose.Schema({
  private: {
    type: Array,
    of: String
  },
  public: {
    type: Array,
    of: String
  }
})
const PrivatePublicWallet = new mongoose.Schema({
  private: {
    type: String,
  },
  public: {
    type: String,
  }
})


const KeysSchema = new mongoose.Schema({
  crypto: PrivatePublicCrypto,
  wallet: PrivatePublicWallet,
});

// export model Document with DocumentSchema
export default KeysSchema