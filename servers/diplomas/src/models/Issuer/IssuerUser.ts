import mongoose from "mongoose";
import KeysSchema from '@diplomas/server/models/Keys';
import Document from '@diplomas/server/models/Issuer/Document';
import ContractSchema from "../Contract";

const IssuerUserSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true
  },
  title: String,
  password: {
    type: String,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now()
  },
  publicKey: String,
  contract: ContractSchema,
  keys: KeysSchema
});

IssuerUserSchema.methods.createQualification = async function(data, holderPub){
  const qualification = await Document.create({
    ...data,
    holderPub,
    issuer: this._id
  })
  return qualification
}
// export model user with IssuerSchema
const IssuerUser =  mongoose.model("IssuerUser", IssuerUserSchema);

export default IssuerUser