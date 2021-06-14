import mongoose from "mongoose";

const ContractSchema = new mongoose.Schema({
  provider: String,
  network: String,
  bytecode: String,
  abi: {
    type: Array,
  },
  address: String,
});

// export model Document with HolderDocumentSchema
export default ContractSchema;