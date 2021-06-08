import mongoose from "mongoose";

const PrivatePublic = new mongoose.Schema({
  private: {
    type: Array,
    of: String
  },
  public: {
    type: Array,
    of: String
  }
})


const KeysSchema = new mongoose.Schema({
  crypto: PrivatePublic,
  wallet: PrivatePublic,
});

// export model Document with DocumentSchema
export default KeysSchema