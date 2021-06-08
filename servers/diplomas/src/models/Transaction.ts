import mongoose from "mongoose";


const TransactionSchema = new mongoose.Schema({
  hash: {
    type: String
  },
  status: {
    type: String
  }
})

export default TransactionSchema