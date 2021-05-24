const TransactionSchema = mongoose.Schema({
  hash: {
    type: String
  },
  status: {
    type: String
  }
})

export default TransactionSchema